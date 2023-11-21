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
        infection_color = QColor(255, int(255 * (1 - infection_percentage)), int(255 * (1 - infection_percentage)))
        immunity_color = QColor(int(255 * immunity_percentage), int(255 * immunity_percentage), 255)
        mortality_color = QColor(int(255 * (1 - mortality_percentage)), int(255 * (1 - mortality_percentage)),
                                int(255 * (1 - mortality_percentage)))

        # Combine the colors based on the percentages
        final_color = QColor(
            int(original_color[0] * (1 - infection_percentage) * (1 - mortality_percentage) + infection_color.red() * (1 - mortality_percentage)),
            int(original_color[1] * (1 - infection_percentage) * (1 - mortality_percentage) + infection_color.green() * (1 - mortality_percentage)),
            int(original_color[2] * (1 - infection_percentage) * (1 - mortality_percentage) + infection_color.blue() * (1 - mortality_percentage)),
            original_color[3]
        )

        final_color = QColor(
            int(final_color.red() * (1 - immunity_percentage) + immunity_color.red() * immunity_percentage),
            int(final_color.green() * (1 - immunity_percentage) + immunity_color.green() * immunity_percentage),
            int(final_color.blue() * (1 - immunity_percentage) + immunity_color.blue() * immunity_percentage),
            original_color[3]  # Preserve the original alpha value
        )

        # Update the segment image
        image = self.segment_images[index].convert("RGBA")
        for x in range(image.width):
            for y in range(image.height):
                r, g, b, a = image.getpixel((x, y))
                if a > 0:
                    # Blend the original color with the final color based on the alpha value
                    blended_color = QColor(
                        int(r + (final_color.red() - r) * (a / 255)),
                        int(g + (final_color.green() - g) * (a / 255)),
                        int(b + (final_color.blue() - b) * (a / 255)),
                        a
                    )
                    image.putpixel((x, y), blended_color.getRgb())

        # Update the segment image
        self.segment_images[index] = image

        # Redraw the entire composite image
        self.redraw_all_segments()


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

def main():
    app = QApplication(sys.argv)

    # Replace the following with the actual paths to your segment images
    segment_paths = [
        'Disease-Simulator/output_regions/region_2.png',
        'Disease-Simulator/output_regions/region_3.png',
        'Disease-Simulator/output_regions/region_4.png',
        'Disease-Simulator/output_regions/region_5.png',
        'Disease-Simulator/output_regions/region_6.png',
        'Disease-Simulator/output_regions/region_7.png',
        'Disease-Simulator/output_regions/region_8.png',
        'Disease-Simulator/output_regions/region_9.png'
    ]

    viewer = ImageViewer(segment_paths)
    viewer.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
