import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from make_spn import spn_value

SCREEN_SIZE = [600, 450]


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
        self.get_coords = QPushButton(self)
        self.get_coords.setText("Получить")
        self.get_coords.move(510, 0)
        self.get_coords.clicked.connect(self.to_get_coords)
        self.get_coords.resize(90, 20)
        self.image = QLabel(self)
        self.image.move(0, 20)
        self.image.resize(600, 430)
        self.spn = 0.5
        self.coords = ""

    def setImage(self, coords_text, spn):
        params = {
            "ll": coords_text,
            "l": "map",
            "spn": f"{spn},{spn}"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=params)
        print(response.url)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, e):
        if e.key() == 16777235:
            if self.spn > 0.0001:
                self.spn -= 0.01
        elif e.key() == 16777237:
            if self.spn < 2:
                self.spn += 0.1
        if self.coords:
            self.setImage(self.coords, round(float(self.spn), 2))

    def closeEvent(self, event):
        os.remove(self.map_file)

    def to_get_coords(self):
        text = self.coords_input.text()
        self.setImage(text, self.spn)
        self.coords = text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())