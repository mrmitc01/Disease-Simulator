"""
Sets up a GUI using PyQt6 for a drawing application. Loads an image and provides functionality for
translating, rotating, shearing, and scaling a rectangle on a canvas.
"""

from Disease import *
from PyQt6.QtGui import *
from structure import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sys
import os
from skimage import io, color
import numpy as np

totalInfected = 0
totalDead = 0
totalRecovered = 0

class KentuckyViewer(QMainWindow):
    def __init__(self, segments):
        super().__init__()

        self.segments = segments
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.canvas_label = QLabel(self)
        self.layout.addWidget(self.canvas_label)

        self.buttons_layout = QVBoxLayout()

        self.region_widgets = []

        for i, segment in enumerate(self.segments):
            region_widget = QPushButton(f"Region {i + 1}", self)
            region_widget.clicked.connect(lambda _, idx=i: self.update_color(idx))
            self.region_widgets.append(region_widget)
            self.buttons_layout.addWidget(region_widget)

        self.layout.addLayout(self.buttons_layout)

        self.central_widget.setLayout(self.layout)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Kentucky Map Viewer')

        self.update_canvas()

    def update_color(self, region_index):
        # Update the color of the specific region dynamically
        region = self.segments[region_index]
        region[:, :, :3] = np.array([255, 0, 0])  # Set color to red
        io.imsave(f'region_{region_index + 1}.png', region)

        # Update the canvas to reflect the changes
        self.update_canvas()

    def update_canvas(self):
        # Combine the regions into the full image of Kentucky
        composite_image = np.zeros_like(self.segments[0])
        for region in self.segments:
            composite_image += region

        # Display the composite image
        io.imsave('combined_kentucky.png', composite_image)
        pixmap = QPixmap('combined_kentucky.png')
        self.canvas_label.setPixmap(pixmap)

# Creates an instance of the DrawingApp class, shows the main window, and starts the application loop.
def main():
    app = QApplication([])

    # Replace 'path_to_segments' with the actual path to your segment images directory
    segment_directory = 'output_regions'

    # Get a list of segment paths
    segment_paths = [os.path.join(segment_directory, filename) for filename in os.listdir(segment_directory) if filename.endswith('.png')]

    # Load segments
    segments = [io.imread(segment_path) for segment_path in segment_paths]

    window = KentuckyViewer(segments)
    window.show()

    app.exec()

if __name__ == '__main__':
    main()