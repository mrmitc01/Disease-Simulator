"""
Sets up a GUI using PyQt6 for a drawing application. Loads an image and provides functionality for
translating, rotating, shearing, and scaling a rectangle on a canvas.
"""

from Disease import *
from structure import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sys
from skimage import io, color
from matplotlib import pyplot as plt
import numpy as np

totalInfected = 0
totalDead = 0
totalRecovered = 0

#lightredregion = io.imread('region1.json')
imgky = io.imread('croppednewmap.png')
image = color.rgba2rgb(imgky)

# Represents a GUI application for a drawing app.
class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        statisticsXCoord = 10
        infectedLabelYCoord = 350
        deadLabelYCoord = 365
        recoveredLabelYCoord = 380

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

        #button_layout.addWidget(self.diseaseType0Button)
        button_layout.addWidget(self.diseaseType1Button)
        button_layout.addWidget(self.diseaseType2Button)
        button_layout.addWidget(self.diseaseType3Button)

        self.infectedLabel = QLabel("Total Infected: " + str(totalInfected), central_widget)
        self.infectedLabel.move(statisticsXCoord, infectedLabelYCoord)
        self.deadLabel = QLabel("Total Dead: " + str(totalDead), central_widget)
        self.deadLabel.move(statisticsXCoord, deadLabelYCoord)
        self.recoveredLabel = QLabel("Total Recovered: " + str(totalRecovered), central_widget)
        self.recoveredLabel.move(statisticsXCoord, recoveredLabelYCoord)

        # Create text box for input param
        label = QLabel("Enter Disease parameters:", central_widget)

        self.text_box = QLineEdit(central_widget)
        layout.addLayout(button_layout)

        layout.addWidget(label)
        layout.addWidget(self.text_box)

        central_widget.setLayout(layout)
        self.setGeometry(100, 100, 600, 600)


        text = self.text_box.text()
        if text:
            param = int(text)
        else:
            param = 0
        self.canvas.turnRed(self, region2, param)

    # Update totalInfected, totalDead, and totalRecovered by passing in additional numInfected,
    # numDead, and numRecovered. Update statistics labels with these new totals.
    def updateStatisticsLabels(self, numInfected, numDead, numRecovered):
        global totalInfected, totalDead, totalRecovered

        totalInfected += numInfected
        totalDead += numDead
        totalRecovered += numRecovered

        self.infectedLabel.setText("Total Infected: " + str(numInfected))
        self.deadLabel.setText("Total Dead: " + str(numDead))
        self.recoveredLabel.setText("Total Recovered: " + str(numRecovered))


class CanvasWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.rect_drawn = False
        self.points = []


    # Overrides the paintEvent method to handle the drawing on the canvas.
    def paintEvent(self, event):
        if self.rect_drawn:
            # After a button is clicked
            painter = QPainter(self)
        else:
            # Before a button is clicked
            painter = QPainter(self)
            pixmap = QPixmap("out_put_regions\\region_2.png")
            painter.drawPixmap(self.rect(), pixmap)


# Creates an instance of the DrawingApp class, shows the main window, and starts the application loop.
def main():
    app = QApplication(sys.argv)
    window = DrawingApp()
    window.show()

    # Need to put something here to call the "engine" program that runs the simulation

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
