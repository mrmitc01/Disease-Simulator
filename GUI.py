from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QLineEdit
from PyQt6.QtGui import QPixmap, QImage, QColor
import sys
from PIL import Image, ImageQt

class ImageViewer(QMainWindow):
    def __init__(self, segment_paths):
        super().__init__()

        self.segment_paths = segment_paths
        self.segment_images = [Image.open(path) for path in segment_paths]
        self.infection_percentages = [0.0] * len(segment_paths)
        self.immunity_percentages = [0.0] * len(segment_paths)
        self.mortality_percentages = [0.0] * len(segment_paths)
        self.original_colors = [image.getpixel((0, 0)) for image in self.segment_images]

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.input_layout = QVBoxLayout()

        # Dropdown for region selection
        self.region_dropdown = QComboBox(self)
        self.region_dropdown.addItems([f"Region {i+2}" for i in range(len(segment_paths))])
        self.input_layout.addWidget(self.region_dropdown)

        # LineEdits for percentage inputs
        self.infection_input = QLineEdit(self)
        self.infection_input.setPlaceholderText("Enter Infection Percentage (0-100)")
        self.input_layout.addWidget(self.infection_input)

        self.immunity_input = QLineEdit(self)
        self.immunity_input.setPlaceholderText("Enter Immunity Percentage (0-100)")
        self.input_layout.addWidget(self.immunity_input)

        self.mortality_input = QLineEdit(self)
        self.mortality_input.setPlaceholderText("Enter Mortality Percentage (0-100)")
        self.input_layout.addWidget(self.mortality_input)

        # Button to apply changes
        apply_button = QPushButton("Apply Changes", self)
        apply_button.clicked.connect(self.apply_changes)
        self.input_layout.addWidget(apply_button)

        self.layout.addLayout(self.input_layout)

        self.combined_label = QLabel(self)
        self.layout.addWidget(self.combined_label)

        self.central_widget.setLayout(self.layout)

        self.setWindowTitle('Disease Simulation')
        self.redraw_all_segments()

    def apply_changes(self):
        # Get selected region and percentage inputs
        selected_region_index = self.region_dropdown.currentIndex()
        infection_text = self.infection_input.text()
        immunity_text = self.immunity_input.text()
        mortality_text = self.mortality_input.text()

        try:
            # Convert percentages to float
            infection_percentage = float(infection_text)
            immunity_percentage = float(immunity_text)
            mortality_percentage = float(mortality_text)

            # Validate percentages
            if 0 <= infection_percentage <= 100 and 0 <= immunity_percentage <= 100 and 0 <= mortality_percentage <= 100:
                # Update the percentages for the selected region
                self.infection_percentages[selected_region_index] = infection_percentage
                self.immunity_percentages[selected_region_index] = immunity_percentage
                self.mortality_percentages[selected_region_index] = mortality_percentage

                # Update the label with the modified image
                self.update_color(selected_region_index)
            else:
                print("Percentages must be between 0 and 100.")
        except ValueError:
            print("Invalid percentage. Please enter a number between 0 and 100.")

    def update_color(self, index):
        # Get the original color of the segment
        original_color = self.original_colors[index]

        # Calculate the color based on infection, immunity, and mortality percentages
        infection_percentage = self.infection_percentages[index] / 100
        immunity_percentage = self.immunity_percentages[index] / 100
        mortality_percentage = self.mortality_percentages[index] / 100

        # Calculate colors based on percentages
        infection_color = (255, 0, 0)
        immunity_color = (0, 0, 255)
        mortality_color = (0, 0, 0)

        # Adjust the colors based on percentages
        final_color = (
            int(original_color[0] + (infection_color[0] - original_color[0]) * infection_percentage),
            int(original_color[1] + (infection_color[1] - original_color[1]) * infection_percentage),
            int(original_color[2] + (infection_color[2] - original_color[2]) * infection_percentage),
            original_color[3]
        )

        final_color = (
            int(final_color[0] + (immunity_color[0] - final_color[0]) * immunity_percentage),
            int(final_color[1] + (immunity_color[1] - final_color[1]) * immunity_percentage),
            int(final_color[2] + (immunity_color[2] - final_color[2]) * immunity_percentage),
            final_color[3]
        )

        final_color = (
            int(final_color[0] + (mortality_color[0] - final_color[0]) * mortality_percentage),
            int(final_color[1] + (mortality_color[1] - final_color[1]) * mortality_percentage),
            int(final_color[2] + (mortality_color[2] - final_color[2]) * mortality_percentage),
            final_color[3]
        )

        # Update the segment image
        image = self.segment_images[index].convert("RGBA")
        for x in range(image.width):
            for y in range(image.height):
                r, g, b, a = image.getpixel((x, y))
                if a > 0:
                    # Blend the original color with the final color based on the alpha value
                    blended_color = (
                        int(r + (final_color[0] - r) * (a / 255)),
                        int(g + (final_color[1] - g) * (a / 255)),
                        int(b + (final_color[2] - b) * (a / 255)),
                        a
                    )
                    image.putpixel((x, y), blended_color)

        # Update the segment image
        self.segment_images[index] = image

        # Redraw the entire composite image
        self.redraw_all_segments()


    def updateStatisticsLabels(self, numInfected, numDead, numRecovered):
        global totalInfected, totalDead, totalRecovered
    
    def redraw_all_segments(self):
        # Create a blank white image to serve as the base
        combined_image = Image.new('RGBA', self.segment_images[0].size, (255, 255, 255, 0))

        # Paste each segment onto the blank image
        for segment_image in self.segment_images:
            combined_image.paste(segment_image, (0, 0), segment_image)

        # Update the label with the modified image
        qimage = ImageQt.ImageQt(combined_image)
        pixmap = QPixmap.fromImage(qimage)
        self.combined_label.setPixmap(pixmap)
'''
totalInfected = 0
totalDead = 0
totalRecovered = 0

class KentuckyViewer(QMainWindow):
    def __init__(self, segments):
        super().__init__()

        self.segments = segments
        self.initUI()

    def initUI(self):
        statisticsXCoord = 20
        infectedLabelYCoord = 40
        deadLabelYCoord = 60
        recoveredLabelYCoord = 80
        colorStyle = "color: white; background-color: black"

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
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

        self.setGeometry(100, 100, 1000, 600)
        self.setWindowTitle('Kentucky Map Viewer')

        self.update_canvas()

        self.infectedLabel = QLabel("Total Infected: " + str(totalInfected), self.central_widget)
        self.infectedLabel.move(statisticsXCoord, infectedLabelYCoord)
        self.infectedLabel.setStyleSheet(colorStyle)
        self.deadLabel = QLabel("Total Dead: " + str(totalDead), self.central_widget)
        self.deadLabel.move(statisticsXCoord, deadLabelYCoord)
        self.deadLabel.setStyleSheet(colorStyle)
        self.recoveredLabel = QLabel("Total Recovered: " + str(totalRecovered), self.central_widget)
        self.recoveredLabel.move(statisticsXCoord, recoveredLabelYCoord)
        self.recoveredLabel.setStyleSheet(colorStyle)

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
        totalInfected += numInfected
        totalDead += numDead
        totalRecovered += numRecovered

        self.infectedLabel.setText("Total Infected: " + str(numInfected))
        self.deadLabel.setText("Total Dead: " + str(numDead))
        self.recoveredLabel.setText("Total Recovered: " + str(numRecovered))
        '''
# Creates an instance of the DrawingApp class, shows the main window, and starts the application loop.
def main():
    app = QApplication(sys.argv)

    # Replace the following with the actual paths to your segment images
    segment_paths = [
        'output_regions/region_2.png',
        'output_regions/region_3.png',
        'output_regions/region_4.png',
        'output_regions/region_5.png',
        'output_regions/region_6.png',
        'output_regions/region_7.png',
        'output_regions/region_8.png',
        'output_regions/region_9.png'
    ]

    viewer = ImageViewer(segment_paths)
    viewer.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
