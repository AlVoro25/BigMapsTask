import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from make_spn import spn_value

SCREEN_SIZE = [600, 550]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.ind = 0
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.coords_input = QLineEdit(self)
        self.coords_input.move(0, 0)
        self.coords_input.resize(510, 20)
        self.coords_input.setText("48.291432,42.065616")
        self.get_coords = QPushButton(self)
        self.get_coords.setText("Получить")
        self.get_coords.move(510, 0)
        self.get_coords.clicked.connect(self.to_get_coords)
        self.get_coords.resize(90, 21)
        self.key_down = QPushButton(self)
        self.key_down.setText("↓")
        self.key_down.move(280, 510)
        self.key_down.clicked.connect(self.move_map)
        self.key_down.resize(30, 30)
        self.key_up = QPushButton(self)
        self.key_up.setText("↑")
        self.key_up.move(280, 480)
        self.key_up.clicked.connect(self.move_map)
        self.key_up.resize(30, 30)
        self.key_left = QPushButton(self)
        self.key_left.setText("←")
        self.key_left.move(250, 495)
        self.key_left.clicked.connect(self.move_map)
        self.key_left.resize(30, 30)
        self.key_right = QPushButton(self)
        self.key_right.setText("→")
        self.key_right.move(310, 495)
        self.key_right.clicked.connect(self.move_map)
        self.key_right.resize(30, 30)
        self.key_map = QPushButton(self)
        self.key_map.setText("map")
        self.key_map.move(350, 495)
        self.key_map.clicked.connect(self.move_map)
        self.key_map.resize(35, 30)
        self.key_sat = QPushButton(self)
        self.key_sat.setText("sat")
        self.key_sat.move(385, 495)
        self.key_sat.clicked.connect(self.move_map)
        self.key_sat.resize(35, 30)
        self.key_skl = QPushButton(self)
        self.key_skl.setText("skl")
        self.key_skl.move(420, 495)
        self.key_skl.clicked.connect(self.move_map)
        self.key_skl.resize(35, 30)
        self.reset_sr = QPushButton(self)
        self.reset_sr.setText("Сбросить п.р")
        self.reset_sr.move(455, 495)
        self.reset_sr.clicked.connect(self.move_map)
        self.reset_sr.resize(80, 30)
        self.image = QLabel(self)
        self.image.move(0, 20)
        self.image.resize(600, 430)
        self.spn = 0.1
        self.coords = ""
        self.map_type = "map"
        self.pt_coordinates = ""

    def setImage(self, coords_text, spn, map_type):
        params = {
            "ll": coords_text,
            "l": map_type,
            "spn": f"{spn},{spn}",
            "pt": self.pt_coordinates
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=params)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
    
    def to_get_coords(self):
        text = self.coords_input.text()
        self.coords = text
        self.pt_coordinates = text
        self.setImage(text, self.spn, self.map_type)

    def move_map(self):
        if self.coords != "":
            if self.sender().text() == "↓":
                coordinate = float(self.coords.split(",")[1]) - 0.2
                self.coords = f"{self.coords.split(',')[0]},{coordinate}"
            elif self.sender().text() == "↑":
                coordinate = float(self.coords.split(",")[1]) + 0.2
                self.coords = f"{self.coords.split(',')[0]},{coordinate}"
            elif self.sender().text() == "←":
                coordinate = float(self.coords.split(",")[0]) - 0.2
                self.coords = f"{coordinate},{self.coords.split(',')[1]}"
            elif self.sender().text() == "→":
                coordinate = float(self.coords.split(",")[0]) + 0.2
                self.coords = f"{coordinate},{self.coords.split(',')[1]}"
            elif self.sender().text() == "map":
                self.map_type = "map"
            elif self.sender().text() == "sat":
                self.map_type = "sat"
            elif self.sender().text() == "skl":
                self.map_type = "skl"
            elif self.sender().text() == "Сбросить п.р":
                self.pt_coordinates = ""
            self.setImage(self.coords, round(float(self.spn), 2), self.map_type)

    def closeEvent(self, event):
        if self.coords != "":
            os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())