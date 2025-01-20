import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_contrast(image):
    """
    Calculate the Michelson contrast of the image.
    Handles uniform images and ensures proper data types.
    """
    I_min = np.min(image)
    I_max = np.max(image)
    epsilon = 1e-10  # Small value to prevent division by zero

    # Check if the image is uniform
    if I_max == I_min:
        print("The image is uniform (all pixels have the same intensity).")
        return 0  # Contrast is zero for uniform images

    # Debug: Print min and max intensity values
    print(f"I_min: {I_min}, I_max: {I_max}")

    # Calculate Michelson contrast
    contrast = (I_max - I_min) / (I_max + I_min + epsilon)
    return contrast

def calculate_rms_contrast(image):
    """
    Calculate RMS contrast of the image.
    """
    return np.std(image)

# List of image paths
image_paths = [
    "D:\PYTHON\Sem6Project\VGG16-19\gptimage.webp",  # Replace with your image file paths
    "D:\PYTHON\Sem6Project\VGG16-19\posters_food\p16.png",
    "D:\PYTHON\Sem6Project\VGG16-19\posters_food\p5.png"
]

# Process each image
for image_path in image_paths:
    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        continue

    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Failed to load image: {image_path}")
        continue

    # Visualize the histogram of pixel intensities
    plt.hist(image.ravel(), bins=256, range=[0, 256])
    plt.title(f"Histogram for {os.path.basename(image_path)}")
    plt.show()

    # Calculate Michelson contrast
    michelson_contrast = calculate_contrast(image)
    print(f"Michelson Contrast for {os.path.basename(image_path)}: {michelson_contrast}")

    # Calculate RMS contrast
    rms_contrast = calculate_rms_contrast(image)
    print(f"RMS Contrast for {os.path.basename(image_path)}: {rms_contrast}")
