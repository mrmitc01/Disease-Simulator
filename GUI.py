from Disease import *
from PyQt6.QtGui     import *
from PyQt6.QtWidgets import *
import sys
from skimage import io, color, filters, morphology, measure, segmentation
from skimage import data
from skimage.color import rgb2gray, rgba2rgb
from matplotlib import pyplot as plt
from skimage.morphology import closing, square
from skimage.segmentation import clear_border
import cv2
import numpy as np

#take image, remove opacities, make grayscale
imgky = io.imread('croppednewmap.png')
image = color.rgba2rgb(imgky)
print(image[200, 200])
plt.imshow(image)
plt.show()
#target_color =[0.443, 0.659, 0.678]
white_color = [1.0, 1.0, 1.0]

orange_color = [0.90980392, 0.5254902, 0.10196078]
pennyroyal = [0.443, 0.659, 0.678]


def getRegion(color):
    region = []
    for row in image:
        row_result = []
        for pixel in row:
            if np.allclose(pixel, color):
                row_result.append([1.0, 1.0, 1.0])
            else:
                row_result.append([0.0, 0.0, 0.0])
        region.append(row_result)
    with open('orangeregion.txt', 'w') as f:
        for row in region:
            f.write(str(row) + '\n')
    return(region)

orangeRegion = getRegion(orange_color)


# Convert the list to a NumPy array
orangeRegion = np.array(orangeRegion)

# Create a new figure for the white region
plt.figure(figsize=(8, 8))

# Display the white region
plt.imshow(orangeRegion)
plt.title('White Region')
plt.axis('off')
plt.show()

class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        #Initializing widget stuff
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.canvas = CanvasWidget(central_widget)
        layout.addWidget(self.canvas)

        button_layout = QHBoxLayout()

        #Create buttons with their functions
        self.diseaseType0Button = QPushButton("DiseaseType0", central_widget)
        #self.translate_button.clicked.connect(self.translation)

        self.diseaseType1Button = QPushButton("DiseaseType1", central_widget)
        #self.rotate_button.clicked.connect(self.rotation)

        self.diseaseType2Button = QPushButton("DiseaseType3", central_widget)
        #self.shear_button.clicked.connect(self.shear)

        self.diseaseType3Button = QPushButton("DiseaseType4", central_widget)
        #self.scale_button.clicked.connect(self.scale)

        button_layout.addWidget(self.diseaseType0Button)
        button_layout.addWidget(self.diseaseType1Button)
        button_layout.addWidget(self.diseaseType2Button)
        button_layout.addWidget(self.diseaseType3Button)

        #Create text box for input param
        label = QLabel("Enter Disease parameters:", central_widget)

        self.text_box = QLineEdit(central_widget)

        layout.addLayout(button_layout)
        layout.addWidget(label)
        layout.addWidget(self.text_box)

        central_widget.setLayout(layout)
        self.setGeometry(100, 100, 600, 600)


    #Define what you want buttons to do
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

class CanvasWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.rect_drawn = False
        self.points = []

    def setPoints(self, points):
        self.points = points
        self.rect_drawn = True
        self.update()

    def paintEvent(self, event):
        if self.rect_drawn:
            #After a button is clicked
            painter = QPainter(self)

        else:
            #Before a button is clicked
            painter = QPainter(self)
            pixmap = QPixmap("croppednewmap.png")
            painter.drawPixmap(self.rect(), pixmap)
            

def main():
    app = QApplication(sys.argv)
    window = DrawingApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()