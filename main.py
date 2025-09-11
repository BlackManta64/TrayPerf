import sys
import psutil
import GPUtil
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import QTimer, Qt

app = QApplication(sys.argv)

ICON_SIZE = 64  # 個別アイコンのサイズ

# トレイアイコンを3つ作る
tray_cpu = QSystemTrayIcon(app)
tray_gpu = QSystemTrayIcon(app)
tray_ram = QSystemTrayIcon(app)

# メニュー作成関数を修正
def create_menu(tray, label):
    menu = QMenu()
    usage_action = QAction(f"{label}: 0%")
    usage_action.setEnabled(False)
    menu.addAction(usage_action)
    menu.addSeparator()
    quit_action = QAction("終了")
    quit_action.triggered.connect(app.quit)
    menu.addAction(quit_action)

    tray.setContextMenu(menu)
    return usage_action


cpu_action = create_menu(tray_cpu, "CPU")
gpu_action = create_menu(tray_gpu, "GPU")
ram_action = create_menu(tray_ram, "RAM")

# 初期アイコン表示
def create_initial_icon(tray):
    pixmap = QPixmap(ICON_SIZE, ICON_SIZE)
    pixmap.fill(QColor("transparent"))
    tray.setIcon(QIcon(pixmap))
    tray.show()

create_initial_icon(tray_cpu)
create_initial_icon(tray_gpu)
create_initial_icon(tray_ram)

# 更新関数
def update_icons():
    cpu_percent = int(psutil.cpu_percent(interval=None))
    mem_percent = int(psutil.virtual_memory().percent)
    gpus = GPUtil.getGPUs()
    gpu_percent = int(gpus[0].load*100) if gpus else 0

    def draw_icon(tray, percent, color, label):
        pixmap = QPixmap(ICON_SIZE, ICON_SIZE)
        pixmap.fill(QColor("transparent"))
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(color))
        painter.drawRect(0, ICON_SIZE - int(ICON_SIZE * percent / 100), ICON_SIZE, int(ICON_SIZE * percent / 100))
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Arial", int(ICON_SIZE*0.35), QFont.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, f"{label}\n{percent}%")
        painter.end()
        tray.setIcon(QIcon(pixmap))

    draw_icon(tray_cpu, cpu_percent, "green", "CPU")
    draw_icon(tray_gpu, gpu_percent, "orange", "GPU")
    draw_icon(tray_ram, mem_percent, "blue", "RAM")

    # メニューも更新
    cpu_action.setText(f"CPU: {cpu_percent}%")
    gpu_action.setText(f"GPU: {gpu_percent}%")
    ram_action.setText(f"RAM: {mem_percent}%")

timer = QTimer()
timer.timeout.connect(update_icons)
timer.start(1000)

sys.exit(app.exec_())
