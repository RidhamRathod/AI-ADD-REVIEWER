import cv2
import numpy as np
import matplotlib.pyplot as plt

def calculate_rms_contrast(image):
    """
    Calculate the RMS contrast of the image.
    """
    return np.std(image)

def interpret_rms_contrast(rms_value, intensity_range):
    """
    Provide an explanation for the RMS contrast value.
    """
    # Define thresholds based on intensity range
    if intensity_range == 255:  # For images with pixel range [0, 255]
        if rms_value < 10:
            return "Low contrast: The image appears very flat or uniform with minimal brightness variation."
        elif rms_value < 40:
            return "Moderate contrast: The image has some brightness variation but lacks significant intensity differences."
        elif rms_value < 70:
            return "High contrast: The image has significant brightness variation with noticeable intensity differences."
        else:
            return "Extremely high contrast: The image has stark brightness variations, likely containing sharp edges or binary patterns."
    elif intensity_range == 1:  # For normalized images with pixel range [0, 1]
        if rms_value < 0.1:
            return "Low contrast: The image appears very flat or uniform with minimal brightness variation."
        elif rms_value < 0.4:
            return "Moderate contrast: The image has some brightness variation but lacks significant intensity differences."
        elif rms_value < 0.7:
            return "High contrast: The image has significant brightness variation with noticeable intensity differences."
        else:
            return "Extremely high contrast: The image has stark brightness variations, likely containing sharp edges or binary patterns."
    else:
        return "Unknown intensity range. Unable to interpret RMS contrast."

# Load the image
image_path = "D:\PYTHON\Sem6Project\VGG16-19\posters_food\p2.png"  # Replace with your file path
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Ensure the image is valid
if image is None:
    raise FileNotFoundError(f"Image not found at {image_path}")

# Calculate RMS contrast
rms_contrast = calculate_rms_contrast(image)

# Determine intensity range (for 8-bit grayscale, it's 255)
intensity_range = np.max(image) - np.min(image)

# Get explanation for RMS contrast
explanation = interpret_rms_contrast(rms_contrast, 255)  # Adjust range if normalized

# Print results
print(f"RMS Contrast: {rms_contrast}")
print(f"Explanation: {explanation}")

