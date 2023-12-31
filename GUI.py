import sys
from PIL import Image, ImageQt
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, \
    QHBoxLayout, QMessageBox
from structure import initialize_regions, run_simulation, COVID, start_infection, MEASLES, FLU, EBOLA


class ImageViewer(QMainWindow):
    def __init__(self, segment_paths, All_Regions):
        super().__init__()

        self.totalInfected = 0
        self.totalDead = 0
        self.totalRecovered = 0

        statisticsXCoord = 10
        infectedLabelYCoord = 160
        deadLabelYCoord = 180
        recoveredLabelYCoord = 200
        labelWidgetWidth = 200
        labelWidgetHeight = 250
        labelWidth = 150
        labelHeight = 20
        colorStyle = "color: white; background-color: black"

        self.segment_paths = segment_paths
        self.All_Regions = All_Regions
        self.infection_started = False  # Add a flag to track if infection has started
        self.segment_images = [Image.open(path) for path in segment_paths]
        self.original_images = [image.copy() for image in
                                self.segment_images]  # Save a copy of the original images for resetting
        self.infection_percentages = [0.0] * len(segment_paths)
        self.immunity_percentages = [0.0] * len(segment_paths)
        self.mortality_percentages = [0.0] * len(segment_paths)
        self.original_colors = [image.getpixel((0, 0)) for image in self.segment_images]

        self.legend_label = QLabel(
            "<span style='color:red'><span style='background-color:red;'>&nbsp;&nbsp;&nbsp;</span> Red: "
            "Infected</span><br>"
            "<span style='color:blue'><span style='background-color:blue;'>&nbsp;&nbsp;&nbsp;</span> Blue: "
            "Immune/Recovered</span><br>"
            "<span style='color:black'><span style='background-color:black;'>&nbsp;&nbsp;&nbsp;</span> Black: "
            "Mortality</span><br>"
        )

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Set a fixed window size
        self.setFixedSize(800, 500)

        self.layout = QVBoxLayout()

        # Create a horizontal layout for region and disease selection
        self.selection_layout = QHBoxLayout()

        # Dropdown for region selection
        self.region_dropdown = QComboBox(self)
        self.region_dropdown.addItems([region.name for region in self.All_Regions])
        default_region_index = 0  # Set the index of the default region (e.g., Region 2)
        self.region_dropdown.setCurrentIndex(default_region_index)

        # Dropdown for disease selection
        self.disease_dropdown = QComboBox(self)
        self.disease_dropdown.addItems(["COVID-19", "Measles", "Generic flu", "Ebola"])
        default_disease_index = 0  # Set the index of the default region (e.g., Custom)
        self.current_disease = COVID  # Initialize with the default disease
        self.disease_dropdown.currentIndexChanged.connect(self.change_disease)
        self.disease_dropdown.setCurrentIndex(default_disease_index)

        # Add a view stats button
        self.view_stats_button = QPushButton("View Stats", self)
        self.view_stats_button.clicked.connect(self.view_stats)

        self.selection_layout.addWidget(self.region_dropdown)
        self.selection_layout.addWidget(self.disease_dropdown)
        self.selection_layout.addWidget(self.view_stats_button)

        self.layout.addLayout(self.selection_layout)  # Add the selection layout

        label_combined_layout = QHBoxLayout()

        # Label widget with statistics
        self.label_widget = QWidget(self)
        self.label_widget.setGeometry(0, 0, labelWidgetWidth, labelWidgetHeight)

        self.infectedLabel = QLabel("Total Infected: " + str(self.totalInfected), self.label_widget)
        self.infectedLabel.setGeometry(statisticsXCoord, infectedLabelYCoord, labelWidth, labelHeight)
        self.infectedLabel.setStyleSheet(colorStyle)
        self.deadLabel = QLabel("Total Dead: " + str(self.totalDead), self.label_widget)
        self.deadLabel.setGeometry(statisticsXCoord, deadLabelYCoord, labelWidth, labelHeight)
        self.deadLabel.setStyleSheet(colorStyle)
        self.recoveredLabel = QLabel("Total Recovered: " + str(self.totalRecovered), self.label_widget)
        self.recoveredLabel.setGeometry(statisticsXCoord, recoveredLabelYCoord, labelWidth, labelHeight)
        self.recoveredLabel.setStyleSheet(colorStyle)

        self.combined_label = QLabel(self)

        label_combined_layout.addWidget(self.label_widget)  # Add the label widget to the layout
        label_combined_layout.addWidget(self.combined_label)  # Add the combined label to the layout

        self.layout.addWidget(self.legend_label)
        self.layout.addStretch()  # Add spacing between the legend and the map

        self.layout.addLayout(label_combined_layout)  # Add the QHBoxLayout to the main layout

        # Create a QVBoxLayout for organizing the buttons
        self.button_layout = QVBoxLayout()

        # Add buttons for controlling the simulation
        self.run_button = QPushButton("Run", self.central_widget)
        self.run_button.setIcon(QIcon('start_icon.png'))
        self.run_button.clicked.connect(self.start_simulation)

        self.stop_button = QPushButton("Stop", self.central_widget)
        self.stop_button.setIcon(QIcon('stop_icon.png'))
        self.stop_button.clicked.connect(self.stop_simulation)

        self.reset_button = QPushButton("Reset", self.central_widget)
        self.reset_button.setIcon(QIcon('reset_icon.png'))
        self.reset_button.clicked.connect(self.reset_simulation)

        # Organize buttons in rows of three using QHBoxLayout
        for buttons in [
            (self.run_button, self.stop_button, self.reset_button),
        ]:
            row_layout = QHBoxLayout()
            for button in buttons:
                row_layout.addWidget(button)
            self.button_layout.addLayout(row_layout)

        # Add the button layout to the main layout
        self.layout.addLayout(self.button_layout)

        # QTimer for simulating the days
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.simulate_day)
        self.days_elapsed = 0

        # Add Days Elapsed and Total Cases to the status bar
        self.statusBar = self.statusBar()
        self.days_elapsed = 0
        self.total_cases = 0
        self.statusBar.showMessage(f"Days Elapsed: {self.days_elapsed} - Total Cases: {self.total_cases}")
        self.disease_label = QLabel("Current Disease: " + self.current_disease.name)
        self.statusBar.addPermanentWidget(self.disease_label)

        self.central_widget.setLayout(self.layout)

        self.setWindowTitle('Disease Simulation')
        self.redraw_all_segments()

    def change_disease(self, index):
        if index == 0:
            self.current_disease = COVID
        elif index == 1:
            self.current_disease = MEASLES
        elif index == 2:
            self.current_disease = FLU
        elif index == 3:
            self.current_disease = EBOLA

        # Update the disease label text
        self.disease_label.setText("Current Disease: " + self.current_disease.name)

    def view_stats(self):
        selected_region_index = self.region_dropdown.currentIndex()
        selected_region = self.All_Regions[selected_region_index]

        # Show stats in a message box
        stats_message = (
            f"Region: {selected_region.name}\n"
            f"Population: {selected_region.population}\n"
            f"Infected Count: {selected_region.infected_count}\n"
            f"Recovered Count: {selected_region.recovered_count}\n"
            f"Dead Count: {selected_region.dead_count}\n"
            # f"Susceptible Count: {selected_region.susceptible_count}\n"
            # f"Population Density: {selected_region.population_density}\n"
        )
        QMessageBox.information(self, "Region Stats", stats_message)

    def reset_images(self):
        # Revert the images back to their original state
        self.segment_images = [image.copy() for image in self.original_images]
        self.redraw_all_segments()

    def get_region_statistics(self, region_index):
        selected_region = self.All_Regions[region_index]
        num_infected = selected_region.infected_count
        num_recovered = selected_region.recovered_count
        num_dead = selected_region.dead_count
        region_population = selected_region.population

        return num_infected, num_recovered, num_dead, region_population

    def apply_changes(self):
        # Get selected region and percentage inputs
        for selected_region_index in range(0, 8):

            # Retrieve statistics for the selected region
            num_infected, num_recovered, num_dead, region_population = self.get_region_statistics(selected_region_index)

            # Calculate percentages
            infection_percentage = (num_infected / region_population) * 100
            recovery_percentage = (num_recovered / region_population) * 100
            mortality_percentage = (num_dead / region_population) * 100

            # Validate percentages
            if 0 <= infection_percentage <= 100 and 0 <= recovery_percentage <= 100 and 0 <= mortality_percentage <= 100:
                # Update the percentages for the selected region
                self.infection_percentages[selected_region_index] = infection_percentage
                self.immunity_percentages[selected_region_index] = recovery_percentage
                self.mortality_percentages[selected_region_index] = mortality_percentage

                # Update the label with the modified image
                self.update_color(selected_region_index)
            else:
                print("Percentages must be between 0 and 100.")

    def update_color(self, index):
        # Get the original color of the segment
        original_color = self.original_colors[index]

        # Calculate the color based on infection, immunity, and mortality percentages
        infection_percentage = self.infection_percentages[index]
        immunity_percentage = self.immunity_percentages[index]
        mortality_percentage = self.mortality_percentages[index]

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

    def start_simulation(self):
        if not self.infection_started:
            start_infection(self.All_Regions)  # Start the infection once at the beginning
            self.infection_started = True  # Update the flag to indicate infection started
        self.timer.start(1000)  # Adjust the interval (in milliseconds) as needed
        print("Simulation started.")

    def stop_simulation(self):
        self.timer.stop()
        print("Simulation stopped.")

    def reset_simulation(self):
        self.timer.stop()  # Stop the simulation timer if it's running
        self.days_elapsed = 0  # Reset the days elapsed counter

        # Reset all counts and statistics for each region
        for region in self.All_Regions:
            region.infected_count = 0
            region.dead_count = 0
            region.recovered_count = 0
            region.susceptible_count = region.population
            region.update_percentages()  # Update the percentages based on the reset counts

        # Reset the total counts in the GUI
        self.totalInfected = 0
        self.totalDead = 0
        self.totalRecovered = 0
        self.total_cases = 0

        # Update the labels to display the reset counts
        self.infectedLabel.setText("Total Infected: " + str(self.totalInfected))
        self.deadLabel.setText("Total Dead: " + str(self.totalDead))
        self.recoveredLabel.setText("Total Recovered: " + str(self.totalRecovered))

        # Ensure the simulation starts with a fresh state
        self.infection_started = False  # Update the flag to indicate infection start

        # Reset the images
        self.reset_images()

        # Reset the status bar
        self.statusBar.showMessage(f"Days Elapsed: {self.days_elapsed} - Total Cases: {self.total_cases}")

        print("Simulation reset.")

    def simulate_day(self):
        # Simulation logic for each day goes here
        self.days_elapsed += 1
        self.statusBar.showMessage(f"Days Elapsed: {self.days_elapsed} - Total Cases: {self.total_cases}")
        print(f"Day {self.days_elapsed} simulated.")
        # Run simulation and get statistics updates
        numInfected, numDead, numRecovered = self.run_simulation_day()

        # Update statistics labels in GUI
        self.updateStatisticsLabels(numInfected, numDead, numRecovered)
        self.apply_changes()

    def run_simulation_day(self):
        # Simulation logic for each day goes here
        run_simulation(self.All_Regions, self.current_disease, 1)

        # Calculate statistics from the simulation results
        numInfected = sum(region.infected_count for region in self.All_Regions)
        numDead = sum(region.dead_count for region in self.All_Regions)
        numRecovered = sum(region.recovered_count for region in self.All_Regions)

        return numInfected, numDead, numRecovered

    def updateStatisticsLabels(self, numInfected, numDead, numRecovered):
        self.totalInfected += numInfected
        self.totalDead += numDead
        self.totalRecovered += numRecovered
        self.total_cases = self.totalInfected + self.totalDead + self.totalRecovered

        self.infectedLabel.setText("Total Infected: " + str(self.totalInfected))
        self.deadLabel.setText("Total Dead: " + str(self.totalDead))
        self.recoveredLabel.setText("Total Recovered: " + str(self.totalRecovered))

        # Update the status bar to include total cases
        self.statusBar.showMessage(f"Days Elapsed: {self.days_elapsed} - Total Cases: {self.total_cases}")

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

    # Initialize regions
    All_Regions = initialize_regions()

    viewer = ImageViewer(segment_paths, All_Regions)
    viewer.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
