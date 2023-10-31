from Disease import *
from PyQt6.QtGui     import *
from PyQt6.QtWidgets import *
import sys
from skimage import io
from skimage import data
from skimage.color import rgb2gray
from matplotlib import pyplot as plt

imgky = io.imread('croppednewmap.png')
#grayky = rgb2gray(imgky)
print(type(imgky))
print(imgky.size)
print(imgky.shape)
io.imshow(imgky)
plt.show()

rect_width = 60
rect_height = 40

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
        self.translate_button = QPushButton("PlaceHolder0", central_widget)
        #self.translate_button.clicked.connect(self.translation)

        self.rotate_button = QPushButton("PlaceHolder1", central_widget)
        #self.rotate_button.clicked.connect(self.rotation)

        self.shear_button = QPushButton("PlaceHolder2", central_widget)
        #self.shear_button.clicked.connect(self.shear)

        self.scale_button = QPushButton("PlaceHolder3", central_widget)
        #self.scale_button.clicked.connect(self.scale)

        button_layout.addWidget(self.translate_button)
        button_layout.addWidget(self.rotate_button)
        button_layout.addWidget(self.shear_button)
        button_layout.addWidget(self.scale_button)

        #Create text box for input param
        label = QLabel("Enter Disease parameters:", central_widget)

        self.text_box = QLineEdit(central_widget)

        layout.addLayout(button_layout)
        layout.addWidget(label)
        layout.addWidget(self.text_box)

        central_widget.setLayout(layout)
        self.setGeometry(100, 100, 600, 400)

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