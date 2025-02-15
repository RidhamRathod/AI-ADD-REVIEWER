import cv2
import numpy as np

def calculate_rms_contrast(image_path):
    """Calculate RMS contrast for each RGB channel separately and return the average contrast."""
    
    # Load the image in color (ensuring it has 3 channels)
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)  
    if image is None:
        raise ValueError("Error: Unable to load image. Check the file path.")

    # Convert from BGR (OpenCV default) to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Compute RMS contrast for each channel (R, G, B)
    rms_contrast = []
    for i in range(3):  # Loop through R, G, B channels
        channel = image[:, :, i]  # Extract channel
        mean_intensity = np.mean(channel)
        rms = np.sqrt(np.mean((channel - mean_intensity) ** 2))  # RMS formula
        rms_contrast.append(rms)

    # Average the RMS contrast of all three channels
    avg_rms_contrast = np.mean(rms_contrast)

    return avg_rms_contrast

# Example Usage
'''image_path = "D:/PYTHON/Sem6Project/Test_imgs/p4.png"  # Update with your image path
rms_contrast_value = calculate_rms_contrast(image_path)

# Print contrast value
print(f"✅ RMS Contrast: {rms_contrast_value:.2f}")
'''