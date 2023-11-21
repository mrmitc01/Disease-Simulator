from PyQt6.QtGui     import *
from PyQt6.QtWidgets import *
from skimage import io, color
from matplotlib import pyplot as plt
import numpy as np

#take image, remove opacities, make grayscale
imgky = io.imread('croppednewmap.png')
image = color.rgba2rgb(imgky)
plt.imshow(image)
plt.show()
#print(image[100,410])
white_color = [1.0, 1.0, 1.0]
orange_color = [0.90980392, 0.5254902, 0.10196078]
gray_color = [0.44313725, 0.65882353, 0.67843137]
yellow_color = [0.91372549, 0.85098039, 0.09019608]
light_red_color = [0.81960784, 0.32156863, 0.32156863]
pink_color = [0.76470588, 0.78823529, 0.95686275]
red_color = [0.42745098, 0.03529412, 0.03529412]
brown_color = [0.48627451, 0.46666667, 0.28627451]
blue_color = [0.0, 0.15294118, 0.89803922]
i = 1
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

    with open('region'+str(i)+'.png', 'w') as f:
        f.write(str(region))

    # Create a new figure for the white region
    plt.figure(figsize=(8, 8))

    # Display the white region
    plt.imshow(region)
    plt.axis('off')
    plt.show()
    return(region)

whiteRegion = getRegion(white_color)
i = i + 1
grayRegion = getRegion(gray_color)
i = i + 1
orange_region = getRegion(orange_color)
i = i + 1
yellow_region = getRegion(yellow_color)
i = i + 1
light_red_region = getRegion(light_red_color)
i = i + 1
pink_region = getRegion(pink_color)
i = i + 1
red_region = getRegion(red_color)
i = i + 1
brown_region = getRegion(brown_color)
i = i + 1
blue_region = getRegion(blue_color)