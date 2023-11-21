from skimage import io, color, segmentation, morphology
from sklearn.cluster import KMeans
import numpy as np
import os

def clean_up_regions(region_img):
    # Convert the region image to binary (1 for region pixels, 0 for background)
    binary_img = region_img.any(axis=-1).astype(int)

    # Perform binary dilation and erosion
    cleaned_img = morphology.binary_erosion(morphology.binary_dilation(binary_img))

    # Apply the cleaned mask to the original region image
    cleaned_region_img = region_img.copy()
    cleaned_region_img[~cleaned_img] = 0

    return cleaned_region_img

def segment_and_save(image_path, num_regions, output_dir):
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
        region_img = np.zeros_like(img_flatten)
        region_img[labels == i] = np.mean(img_flatten[labels == i], axis=0)
        region_img = region_img.reshape((height, width, -1))

        # Clean up the region image
        cleaned_region_img = clean_up_regions(region_img)

        # Save the segmented and cleaned region for indices 0 to 9
        if i < 9:
            region_filename = os.path.join(output_dir, f"region_{i + 1}.png")
            io.imsave(region_filename, cleaned_region_img)

# Example usage
segment_and_save('croppednewmap.png', num_regions=45, output_dir='output_regions')