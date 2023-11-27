from skimage import io
from sklearn.cluster import KMeans
import numpy as np
import os

def make_regions_black(region_img):
    """
    Takes an image of a region and turns all non-background pixels to black.
    Handles both RGB and RGBA images.

    Args:
    region_img (numpy array): The image of the region.

    Returns:
    numpy array: The modified image with the region turned black.
    """
    # Check if the image has an alpha channel
    has_alpha = region_img.shape[-1] == 4

    # Create a black pixel (RGBA or RGB)
    black_pixel = (0, 0, 0, 255) if has_alpha else (0, 0, 0)

    # Initialize a black image
    black_img = np.zeros_like(region_img)

    # Set all non-zero pixels to black
    black_img[region_img.any(axis=-1)] = black_pixel

    return black_img


def segment_and_save(image_path, num_regions, output_dir):
    """
    Segments an image into a specified number of regions using K-Means clustering,
    turns each region black, and saves each as a separate image.

    Args:
    image_path (str): Path to the input image.
    num_regions (int): Number of regions to segment the image into.
    output_dir (str): Directory where segmented images will be saved.
    """
    # Load the image
    img = io.imread(image_path)

    # Flatten the image
    height, width, _ = img.shape
    img_flatten = img.reshape((height * width, -1))

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=num_regions, random_state=0).fit(img_flatten)
    labels = kmeans.labels_

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save each region as a separate image
    for i in range(num_regions):
        # Initialize an image for the region
        region_img = np.zeros_like(img_flatten)
        # Assign the mean color to the pixels in this region
        region_img[labels == i] = np.mean(img_flatten[labels == i], axis=0)
        region_img = region_img.reshape((height, width, -1))

        # Make the region black
        black_region_img = make_regions_black(region_img)

        # Save the blackened region image
        region_filename = os.path.join(output_dir, f"region_{i + 1}.png")
        io.imsave(region_filename, black_region_img)

# Example usage
segment_and_save('croppednewmap.png', num_regions=45, output_dir='output_regions')
