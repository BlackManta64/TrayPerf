import sys
import psutil
import GPUtil
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QColorDialog
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QAction
from PySide6.QtCore import QTimer, Qt

ICON_SIZE = 64

colorCPU = QColor("green")
colorRAM = QColor("blue")
colorGPU = QColor("orange")

translations = {
    "ja": {
        "cpu": "CPU",
        "ram": "RAM",
        "gpu": "GPU",
        "change_color": "{}カラーを変更",
        "quit": "終了",
        "language": "言語",
        "japanese": "日本語",
        "english": "English",
    },
    "en": {
        "cpu": "CPU",
        "ram": "RAM",
        "gpu": "GPU",
        "change_color": "Change {} Color",
        "quit": "Quit",
        "language": "Language",
        "japanese": "日本語",
        "english": "English",
    }
}

current_lang = "en"

def tr(key, *args):
    text = translations[current_lang][key]
    return text.format(*args)

def draw_icon(percent, color, label):
    if not isinstance(color, QColor):
        color = QColor("gray")

    pixmap = QPixmap(ICON_SIZE, ICON_SIZE)
    pixmap.fill(QColor("transparent"))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(color)
    painter.drawRect(0, ICON_SIZE - int(ICON_SIZE * percent / 100), ICON_SIZE, int(ICON_SIZE * percent / 100))
    painter.setPen(QColor("white"))
    painter.setFont(QFont("Arial", int(ICON_SIZE*0.35), QFont.Bold))
    painter.drawText(pixmap.rect(), Qt.AlignCenter, f"{label}\n{percent}%")
    painter.end()
    return QIcon(pixmap)

def main():
    global current_lang
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    tray_cpu = QSystemTrayIcon(app)
    menu_cpu = QMenu()
    action_cpu = QAction(f"{tr('cpu')}: 0%")
    action_cpu.setEnabled(False)
    menu_cpu.addAction(action_cpu)
    menu_cpu.addSeparator()
    color_edit_cpu = QAction(tr("change_color", tr("cpu")))
    def change_cpu_color():
        global colorCPU
        dialog = QColorDialog(colorCPU)
        dialog.setWindowIcon(QIcon("icon.ico"))
        if dialog.exec():
            selected = dialog.selectedColor()
            if selected.isValid():
                colorCPU = selected
                tray_cpu.setIcon(draw_icon(int(psutil.cpu_percent()), colorCPU, tr("cpu")))
    color_edit_cpu.triggered.connect(change_cpu_color)
    quit_cpu = QAction(tr("quit"))
    quit_cpu.triggered.connect(app.quit)
    menu_cpu.addAction(color_edit_cpu)
    menu_cpu.addAction(quit_cpu)
    tray_cpu.setContextMenu(menu_cpu)
    tray_cpu.setIcon(draw_icon(0, colorCPU, tr("cpu")))
    tray_cpu.show()

    tray_ram = QSystemTrayIcon(app)
    menu_ram = QMenu()
    action_ram = QAction(f"{tr('ram')}: 0%")
    action_ram.setEnabled(False)
    menu_ram.addAction(action_ram)
    menu_ram.addSeparator()
    color_edit_ram = QAction(tr("change_color", tr("ram")))
    def change_ram_color():
        global colorRAM
        dialog = QColorDialog(colorRAM)
        dialog.setWindowIcon(QIcon("icon.ico"))
        if dialog.exec():
            selected = dialog.selectedColor()
            if selected.isValid():
                colorRAM = selected
                tray_ram.setIcon(draw_icon(int(psutil.cpu_percent()), colorRAM, tr("ram")))
    color_edit_ram.triggered.connect(change_ram_color)
    quit_ram = QAction(tr("quit"))
    quit_ram.triggered.connect(app.quit)
    menu_ram.addAction(color_edit_ram)
    menu_ram.addAction(quit_ram)
    tray_ram.setContextMenu(menu_ram)
    tray_ram.setIcon(draw_icon(0, colorRAM, tr("ram")))
    tray_ram.show()

    tray_gpu = QSystemTrayIcon(app)
    menu_gpu = QMenu()
    action_gpu = QAction(f"{tr('gpu')}: 0%")
    action_gpu.setEnabled(False)
    menu_gpu.addAction(action_gpu)
    menu_gpu.addSeparator()
    color_edit_gpu = QAction(tr("change_color", tr("gpu")))
    def change_gpu_color():
        global colorGPU
        dialog = QColorDialog(colorGPU)
        dialog.setWindowIcon(QIcon("icon.ico"))
        if dialog.exec():
            selected = dialog.selectedColor()
            if selected.isValid():
                colorGPU = selected
                tray_gpu.setIcon(draw_icon(int(psutil.cpu_percent()), colorGPU, tr("gpu")))
    color_edit_gpu.triggered.connect(change_gpu_color)
    quit_gpu = QAction(tr("quit"))
    quit_gpu.triggered.connect(app.quit)
    menu_gpu.addAction(color_edit_gpu)
    menu_gpu.addAction(quit_gpu)
    tray_gpu.setContextMenu(menu_gpu)
    tray_gpu.setIcon(draw_icon(0, colorGPU, tr("gpu")))
    tray_gpu.show()

    def switch_language(lang):
        global current_lang
        current_lang = lang
        action_cpu.setText(f"{tr('cpu')}: 0%")
        color_edit_cpu.setText(tr("change_color", tr("cpu")))
        quit_cpu.setText(tr("quit"))
        action_ram.setText(f"{tr('ram')}: 0%")
        color_edit_ram.setText(tr("change_color", tr("ram")))
        quit_ram.setText(tr("quit"))
        action_gpu.setText(f"{tr('gpu')}: 0%")
        color_edit_gpu.setText(tr("change_color", tr("gpu")))
        quit_gpu.setText(tr("quit"))

        lang_menu.setTitle(tr("language"))
        lang_jp.setText(tr("japanese"))
        lang_en.setText(tr("english"))

        tray_cpu.setIcon(draw_icon(0, colorCPU, tr("cpu")))
        tray_ram.setIcon(draw_icon(0, colorRAM, tr("ram")))
        tray_gpu.setIcon(draw_icon(0, colorGPU, tr("gpu")))


    lang_menu = QMenu(tr("language"))
    lang_jp = QAction(tr("japanese"))
    lang_en = QAction(tr("english"))
    lang_jp.triggered.connect(lambda: switch_language("ja"))
    lang_en.triggered.connect(lambda: switch_language("en"))
    lang_menu.addAction(lang_jp)
    lang_menu.addAction(lang_en)

    menu_cpu.addSeparator()
    menu_cpu.addMenu(lang_menu)
    menu_ram.addSeparator()
    menu_ram.addMenu(lang_menu)
    menu_gpu.addSeparator()
    menu_gpu.addMenu(lang_menu)

    def update():
        try:
            cpu_percent = int(psutil.cpu_percent(interval=None))
            tray_cpu.setIcon(draw_icon(cpu_percent, colorCPU, tr("cpu")))
            action_cpu.setText(f"{tr('cpu')}: {cpu_percent}%")

            ram_percent = int(psutil.virtual_memory().percent)
            tray_ram.setIcon(draw_icon(ram_percent, colorRAM, tr("ram")))
            action_ram.setText(f"{tr('ram')}: {ram_percent}%")

            gpus = GPUtil.getGPUs()
            gpu_percent = int(gpus[0].load * 100) if gpus else 0
            tray_gpu.setIcon(draw_icon(gpu_percent, colorGPU, tr("gpu")))
            action_gpu.setText(f"{tr('gpu')}: {gpu_percent}%")
        except Exception as e:
            print("Update error:", e)

    timer = QTimer()
    timer.timeout.connect(update)
    timer.start(1000)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
