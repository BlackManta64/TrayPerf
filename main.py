import sys
import psutil
import GPUtil
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QAction
from PySide6.QtCore import QTimer, Qt

ICON_SIZE = 64

def draw_icon(percent, color, label):
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
    return QIcon(pixmap)

def main():
    app = QApplication(sys.argv)

    # CPUアイコン
    tray_cpu = QSystemTrayIcon(app)
    menu_cpu = QMenu()
    action_cpu = QAction("CPU: 0%")
    action_cpu.setEnabled(False)
    menu_cpu.addAction(action_cpu)
    menu_cpu.addSeparator()
    quit_action = QAction("終了")
    quit_action.triggered.connect(app.quit)
    menu_cpu.addAction(quit_action)
    tray_cpu.setContextMenu(menu_cpu)
    tray_cpu.setIcon(draw_icon(0, "green", "CPU"))
    tray_cpu.show()

    tray_ram = QSystemTrayIcon(app)
    menu_ram = QMenu()
    action_ram = QAction("RAM: 0%")
    action_ram.setEnabled(False)
    menu_ram.addAction(action_ram)
    menu_ram.addSeparator()
    menu_ram.addAction(quit_action)
    tray_ram.setContextMenu(menu_ram)
    tray_ram.setIcon(draw_icon(0, "blue", "RAM"))
    tray_ram.show()

    tray_gpu = QSystemTrayIcon(app)
    menu_gpu = QMenu()
    action_gpu = QAction("GPU: 0%")
    action_gpu.setEnabled(False)
    menu_gpu.addAction(action_gpu)
    menu_gpu.addSeparator()
    menu_gpu.addAction(quit_action)
    tray_gpu.setContextMenu(menu_gpu)
    tray_gpu.setIcon(draw_icon(0, "orange", "GPU"))
    tray_gpu.show()

    def update():
        cpu_percent = int(psutil.cpu_percent(interval=None))
        tray_cpu.setIcon(draw_icon(cpu_percent, "green", "CPU"))
        action_cpu.setText(f"CPU: {cpu_percent}%")

        ram_percent = int(psutil.virtual_memory().percent)
        tray_ram.setIcon(draw_icon(ram_percent, "blue", "RAM"))
        action_ram.setText(f"RAM: {ram_percent}%")

        gpus = GPUtil.getGPUs()
        gpu_percent = int(gpus[0].load * 100) if gpus else 0
        tray_gpu.setIcon(draw_icon(gpu_percent, "orange", "GPU"))
        action_gpu.setText(f"GPU: {gpu_percent}%")

    timer = QTimer()
    timer.timeout.connect(update)
    timer.start(1000)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
