import sys
import psutil
import GPUtil
import json
import os
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QColorDialog
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QAction
from PySide6.QtCore import QTimer, Qt

ICON_SIZE = 64
SETTINGS_FILE = "settings.json"

default_colors = {
    "CPU": "green",
    "RAM": "blue",
    "GPU": "orange",
    "DISK": "purple",
    "NET": "red"
}

if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
else:
    settings = {"colors": default_colors, "lang": "en"}

current_lang = settings.get("lang", "en")
colors = {k: QColor(v) for k, v in settings.get("colors", default_colors).items()}

translations = {
    "ja": {"cpu":"CPU","ram":"RAM","gpu":"GPU","disk":"DISK","net":"NET","change_color":"{}カラーを変更","quit":"終了","language":"言語","japanese":"日本語","english":"English"},
    "en": {"cpu":"CPU","ram":"RAM","gpu":"GPU","disk":"DISK","net":"NET","change_color":"Change {} Color","quit":"Quit","language":"Language","japanese":"日本語","english":"English"}
}

def tr(key, *args):
    text = translations[current_lang][key]
    return text.format(*args)

def draw_icon(percent, color, label):
    pixmap = QPixmap(ICON_SIZE, ICON_SIZE)
    pixmap.fill(QColor("transparent"))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(color)
    painter.drawRect(0, ICON_SIZE - int(ICON_SIZE * percent / 100), ICON_SIZE, int(ICON_SIZE * percent / 100))
    painter.setPen(QColor("white"))
    painter.setFont(QFont("Arial", int(ICON_SIZE*0.3), QFont.Bold))
    painter.drawText(pixmap.rect(), Qt.AlignCenter, f"{label}\n{percent}%")
    painter.end()
    return QIcon(pixmap)

def save_settings():
    data = {"colors": {k: colors[k].name() for k in colors}, "lang": current_lang}
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f)

def create_tray(app, label):
    tray = QSystemTrayIcon(app)
    menu = QMenu()

    action = QAction(f"{tr(label.lower())}: 0%")
    action.setEnabled(False)
    menu.addAction(action)
    menu.addSeparator()

    color_action = QAction(tr("change_color", tr(label.lower())))
    def change_color():
        color = QColorDialog.getColor(colors[label], None, tr("change_color", tr(label.lower())))
        if color.isValid():
            colors[label] = color
            tray.setIcon(draw_icon(0, colors[label], tr(label.lower())))
            save_settings()
    color_action.triggered.connect(change_color)
    menu.addAction(color_action)

    quit_action = QAction(tr("quit"))
    quit_action.triggered.connect(app.quit)
    menu.addAction(quit_action)

    tray.setContextMenu(menu)
    tray.setIcon(draw_icon(0, colors[label], tr(label.lower())))
    tray.show()

    return tray, action, color_action, quit_action

def main():
    global current_lang
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    trays = {}
    actions = {}
    color_actions = {}
    quit_actions = {}
    for label in ["CPU","RAM","GPU","DISK","NET"]:
        tray, action, color_action, quit_action = create_tray(app, label)
        trays[label] = tray
        actions[label] = action
        color_actions[label] = color_action
        quit_actions[label] = quit_action

    lang_menu = QMenu(tr("language"))
    lang_jp = QAction(tr("japanese"))
    lang_en = QAction(tr("english"))
    lang_jp.triggered.connect(lambda: switch_language("ja", trays, actions, color_actions, quit_actions))
    lang_en.triggered.connect(lambda: switch_language("en", trays, actions, color_actions, quit_actions))
    lang_menu.addAction(lang_jp)
    lang_menu.addAction(lang_en)

    for tray in trays.values():
        tray.contextMenu().addSeparator()
        tray.contextMenu().addMenu(lang_menu)

    net_prev = psutil.net_io_counters()
    
    def update():
        nonlocal net_prev
        try:
            cpu_percent = int(psutil.cpu_percent(interval=None))
            trays["CPU"].setIcon(draw_icon(cpu_percent, colors["CPU"], tr("cpu")))
            actions["CPU"].setText(f"{tr('cpu')}: {cpu_percent}%")

            ram_percent = int(psutil.virtual_memory().percent)
            trays["RAM"].setIcon(draw_icon(ram_percent, colors["RAM"], tr("ram")))
            actions["RAM"].setText(f"{tr('ram')}: {ram_percent}%")

            gpus = GPUtil.getGPUs()
            gpu_percent = int(gpus[0].load*100) if gpus else 0
            trays["GPU"].setIcon(draw_icon(gpu_percent, colors["GPU"], tr("gpu")))
            actions["GPU"].setText(f"{tr('gpu')}: {gpu_percent}%")

            disk_percent = int(psutil.disk_usage("/").percent)
            trays["DISK"].setIcon(draw_icon(disk_percent, colors["DISK"], tr("disk")))
            actions["DISK"].setText(f"{tr('disk')}: {disk_percent}%")

            net_now = psutil.net_io_counters()
            sent = (net_now.bytes_sent - net_prev.bytes_sent)//1024
            recv = (net_now.bytes_recv - net_prev.bytes_recv)//1024
            net_prev = net_now
            net_speed = max(sent, recv)
            trays["NET"].setIcon(draw_icon(min(net_speed,100), colors["NET"], tr("net")))
            actions["NET"].setText(f"{tr('net')}: {net_speed} kB/s")

        except Exception as e:
            print("Update error:", e)

    timer = QTimer()
    timer.timeout.connect(update)
    timer.start(1000)

    sys.exit(app.exec())

def switch_language(lang, trays, actions, color_actions, quit_actions):
    global current_lang
    current_lang = lang
    save_settings()
    for label in actions:
        actions[label].setText(f"{tr(label.lower())}: 0%")
        color_actions[label].setText(tr("change_color", tr(label.lower())))
        quit_actions[label].setText(tr("quit"))

if __name__ == "__main__":
    main()
