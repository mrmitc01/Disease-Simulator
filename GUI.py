"""
Sets up a GUI using PyQt6 for a drawing application. Loads an image and provides functionality for
translating, rotating, shearing, and scaling a rectangle on a canvas.
"""

from Disease import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sys
from skimage import io, color
from matplotlib import pyplot as plt
import numpy as np
import json


#lightredregion = io.imread('region1.json')
imgky = io.imread('croppednewmap.png')
image = color.rgba2rgb(imgky)

with open('region1.json', "r") as json_file:
    data = json.load(json_file)

plt.imshow(data)



# Represents a GUI application for a drawing app.
class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initializing widget stuff
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.canvas = CanvasWidget(central_widget)
        layout.addWidget(self.canvas)

        button_layout = QHBoxLayout()

        # Create buttons with their functions
        self.diseaseType0Button = QPushButton("DiseaseType0", central_widget)
        # self.translate_button.clicked.connect(self.translation)

        self.diseaseType1Button = QPushButton("DiseaseType1", central_widget)
        # self.rotate_button.clicked.connect(self.rotation)

        self.diseaseType2Button = QPushButton("DiseaseType3", central_widget)
        # self.shear_button.clicked.connect(self.shear)

        self.diseaseType3Button = QPushButton("DiseaseType4", central_widget)
        # self.scale_button.clicked.connect(self.scale)

        button_layout.addWidget(self.diseaseType0Button)
        button_layout.addWidget(self.diseaseType1Button)
        button_layout.addWidget(self.diseaseType2Button)
        button_layout.addWidget(self.diseaseType3Button)

        # Create text box for input param
        label = QLabel("Enter Disease parameters:", central_widget)

        self.text_box = QLineEdit(central_widget)

        layout.addLayout(button_layout)
        layout.addWidget(label)
        layout.addWidget(self.text_box)

        central_widget.setLayout(layout)
        self.setGeometry(100, 100, 600, 600)


    # Provides methods for handling button clicks to perform translation, rotation, shear, and scale transformations.

    def translation(self):
        text = self.text_box.text()
        if text:
            param = int(text)
        else:
            param = 0
        disease = Disease('translation', param, rect_width, rect_height)
        points = disease.translate()
        self.canvas.setPoints(points)

    def rotation(self):
        text = self.text_box.text()
        if text:
            param = int(text)
        else:
            param = 0
        Disease = Disease('rotation', param, rect_width, rect_height)
        points = Disease.rotate()
        self.canvas.setPoints(points)

    def shear(self):
        text = self.text_box.text()
        if text:
            param = int(text)
        else:
            param = 0
        Disease = Disease('shear', param, rect_width, rect_height)
        points = Disease.shear()
        self.canvas.setPoints(points)

    def scale(self):
        text = self.text_box.text()
        if text:
            param = int(text)
        else:
            param = 0
        Disease = Disease('scale', param, rect_width, rect_height)
        points = Disease.scale()
        self.canvas.setPoints(points)

class CanvasWidget(QWidget):
    #Keep a list of points so that they can be updated
    def __init__(self, parent):
        super().__init__(parent)
        self.rect_drawn = False
        self.points = []

    #Send points to be drawn
    def setPoints(self, points):
        self.points = points
        self.rect_drawn = True
        self.update()

# Represents a canvas where drawings can be displayed.
class CanvasWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.rect_drawn = False
        self.points = []

    # Provides a method to set and update points to be drawn.
    def setPoints(self, points):
        self.points = points
        self.rect_drawn = True
        self.update()

    # Overrides the paintEvent method to handle the drawing on the canvas.
    def paintEvent(self, event):
        if self.rect_drawn:
            # After a button is clicked
            painter = QPainter(self)
        else:
            # Before a button is clicked
            painter = QPainter(self)
            pixmap = QPixmap("croppednewmap.png")
            painter.drawPixmap(self.rect(), pixmap)


# Creates an instance of the DrawingApp class, shows the main window, and starts the application loop.
def main():
    app = QApplication(sys.argv)
    window = DrawingApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
