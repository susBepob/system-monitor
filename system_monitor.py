import sys
import psutil

from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame
)




class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()

        # ---- Window behavior (WIDGET MODE) ----
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setWindowOpacity(0.95)
        self.setWindowIcon(QIcon("icon.ico"))
        self.resize(220, 160)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        title = QLabel("SYSTEM")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")
        main_layout.addWidget(title)

        cards_layout = QHBoxLayout()
        main_layout.addLayout(cards_layout)

        self.cpu_card = self.create_card("CPU")
        self.ram_card = self.create_card("RAM")
        self.temp_card = self.create_card("TEMP")

        cards_layout.addWidget(self.cpu_card)
        cards_layout.addWidget(self.ram_card)
        cards_layout.addWidget(self.temp_card)

        # ---- Timer update ----
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

        self.apply_style()
        self.snap_to_edge()

    # ---------- UI ----------
    def create_card(self, name):
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout()

        label_title = QLabel(name)
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setObjectName("cardTitle")

        label_value = QLabel("...")
        label_value.setAlignment(Qt.AlignCenter)
        label_value.setObjectName("cardValue")

        layout.addWidget(label_title)
        layout.addWidget(label_value)
        card.setLayout(layout)

        card.value_label = label_value
        return card

    # ---------- Data ----------
    def update_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        temp = "N/A"
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name in temps:
                    temp = f"{temps[name][0].current:.1f}°C"
                    break
        except Exception:
            pass

        self.cpu_card.value_label.setText(f"{cpu}%")
        self.ram_card.value_label.setText(f"{ram}%")
        self.temp_card.value_label.setText(temp)

    # ---------- Styling -----
    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 210);
                color: white;
                font-family: Segoe UI;
                border-radius: 14px;
            }
            #title {
                font-size: 14px;
                font-weight: bold;
                padding-bottom: 6px;
            }
            #card {
                background-color: rgba(50, 50, 50, 200);
                border-radius: 10px;
                padding: 6px;
            }
            #cardTitle {
                font-size: 10px;
                color: #aaaaaa;
            }
            #cardValue {
                font-size: 16px;
                font-weight: bold;
            }
        """)

    # -- Position ----------
    def snap_to_edge(self):
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - 10
        y = 120
        self.move(x, y)

    # ---------- Dragging ----------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()


app = QApplication(sys.argv)
window = SystemMonitor()
window.show()
sys.exit(app.exec())