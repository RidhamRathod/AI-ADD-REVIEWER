import cv2
import numpy as np

def detect_blurriness(image_path, threshold=100):
    """
    Detects blurriness in an image using the Laplacian Variance method.
    
    Parameters:
        image_path (str): Path to the image file.
        threshold (int): Variance threshold to determine blurriness. Lower = blurrier.
    
    Returns:
        str: A message indicating whether the image is blurry or sharp.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        return "Error: Image not found."
    
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Compute the Laplacian and variance
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Print result based on threshold
    if variance < 50:
        return "Score: {variance:.2f} - ❌ Very blurry. Try stabilizing your camera or increasing lighting."
    elif variance < 100:
        return "Score: {variance:.2f} - ⚠️ Slightly blurry. Some details are visible, but the image could be sharper."
    elif variance < 200:
        return "Score: {variance:.2f} - ✅ Sharp image. The focus is good, and details are clear."
    else:
        return "Score: {variance:.2f} - 🌟 Very sharp! Excellent focus and high clarity."


# Example usage
'''image_path = "D:\PYTHON\Sem6Project\Test_imgs\p21.png"  # Replace with your image path
detect_blurriness(image_path)'''

