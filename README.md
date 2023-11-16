# Disease-Simulator

## Overview

Welcome to the Disease Spread Simulation project! This repository contains a Python-based simulation and visualization tool designed to model the transmission of diseases within various geographical regions. The system incorporates multiple components, each contributing to an interactive graphical user interface (GUI) that enables users to explore and comprehend the dynamics of disease spread.

## Project Components

### 1. structure.py

   - **Disease Class:**
     - Represents a disease with attributes such as infection probability, recovery duration, mortality probability, and name.
   
   - **State Enum:**
     - Enumerates different states an individual can be in, including SUSCEPTIBLE, INFECTED, RECOVERED, and DEAD.

   - **Region Class:**
     - Represents a geographical region with attributes like name, population, land area, and population density.
     - Contains an instance of the Statistics class.

   - **Statistics Class:**
     - Inherits from Region.
     - Provides statistics for a region, including counts of susceptible, infected, recovered, and dead individuals, along with percentages.
     - Updates percentage values based on the current counts.

   - **Main Block:**
     - Reads population data from a CSV file.

### 2. disease.py

   - **Disease Class:**
     - Represents a disease with transformation parameters for translation, rotation, shear, and scale.
     - Contains methods for translating, rotating, shearing, and scaling.

### 3. GUI.py

   - **Imports:**
     - Imports necessary modules and classes from Disease, PyQt6, sys, and skimage.

   - **Image Loading:**
     - Loads an image using skimage and provides information about the image.

   - **DrawingApp Class:**
     - Inherits from QMainWindow and sets up the main application window.
     - Initializes buttons for different disease types and a text box for input parameters.
     - Provides methods for handling button clicks to perform translation, rotation, shear, and scale transformations.

   - **CanvasWidget Class:**
     - Inherits from QWidget.
     - Represents a canvas where drawings can be displayed.
     - Provides a method to set and update points to be drawn.
     - Overrides the `paintEvent` method to handle drawing on the canvas.

   - **Main Block:**
     - Creates an instance of the DrawingApp class, shows the main window, and starts the application loop.

     
# Setup

## Install Dependencies
Run the following command to install the necessary dependencies:

```bash
python -m pip install pyqt6 scikit-image matplotlib
```

## How to Run
Enter the following command:
```bash
python GUI.py
```

## GitHub Workflow

1. Clone this repository
2. Make changes locally
3. Push to a branch that is not main
4. Make a pull request to main, review code, and accept
