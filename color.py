import cv2
import numpy as np
import openpyxl
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from webcolors import CSS3_NAMES_TO_HEX

def extract_dominant_colors(image_path, n_colors=5):
    # Load the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Reshape the image to be a list of pixels
    pixels = image.reshape(-1, 3)

    # Use KMeans to find dominant colors
    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(pixels)

    return kmeans.cluster_centers_, kmeans.labels_

def plot_colors(dominant_colors):
    # Create a pie chart of the dominant colors
    colors = [color / 255 for color in dominant_colors]
    plt.figure(figsize=(8, 4))
    plt.pie(
        [1] * len(colors),
        colors=colors,
        labels=[f"RGB({int(c[0])},{int(c[1])},{int(c[2])})" for c in dominant_colors],
        autopct="%1.1f%%",
    )
    plt.axis("equal")
    plt.show()

def closest_color_name(rgb):
    # Reverse CSS3_NAMES_TO_HEX to get HEX-to-name mapping
    hex_to_name = {v: k for k, v in CSS3_NAMES_TO_HEX.items()}
    
    # Convert RGB to HEX format
    rgb_hex = '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    
    try:
        # Direct match for the color name
        return hex_to_name[rgb_hex]
    except KeyError:
        # Find the closest matching color
        closest_hex = min(
            hex_to_name.keys(),
            key=lambda hex_color: np.linalg.norm(
                np.array(tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))) - np.array(rgb)
            )
        )
        return hex_to_name[closest_hex]


def color_psychology(dominant_colors):
    # Basic color psychology associations
    psychology = {
        "red": "Energy, passion, danger",
        "green": "Growth, harmony, freshness",
        "blue": "Calmness, stability, trust",
        "yellow": "Happiness, optimism, energy",
        "orange": "Creativity, enthusiasm, success",
        "purple": "Luxury, mystery, imagination",
        "pink": "Love, compassion, gentleness",
        "brown": "Stability, reliability, comfort",
        "white": "Purity, cleanliness, simplicity",
        "black": "Power, elegance, sophistication",
        "gray": "Neutrality, balance, sophistication",
    }

    results = []
    for color in dominant_colors:
        r, g, b = color
        if r > g and r > b:
            label = "red"
        elif g > r and g > b:
            label = "green"
        elif b > r and b > g:
            label = "blue"
        elif r > 200 and g > 200 and b < 100:
            label = "yellow"
        elif r > 200 and g > 100 and b < 100:
            label = "orange"
        elif r > 150 and b > 150:
            label = "purple"
        elif r > 200 and g < 150 and b < 150:
            label = "pink"
        elif r > 100 and g > 50 and b < 50:
            label = "brown"
        elif r > 200 and g > 200 and b > 200:
            label = "white"
        elif r < 50 and g < 50 and b < 50:
            label = "black"
        elif r > 150 and g > 150 and b > 150:
            label = "gray"
        else:
            label = "other"

        meaning = psychology.get(label, "Complex/mixed color psychology")
        color_name = closest_color_name(color)
        results.append((color, color_name, label, meaning))

    return results

#Saving the final results into an excel file
def save_mood_to_excel(file_name, image_name, mood):
    """
    Save the image name and final mood to an Excel file.

    Args:
        file_name (str): The name of the Excel file (e.g., 'color_mood_analysis.xlsx').
        image_name (str): The name of the image being analyzed.
        mood (str): The mood to save in the Excel file.
    """
    try:
        # Try to open the workbook if it exists
        workbook = openpyxl.load_workbook(file_name)
        sheet = workbook.active
    except FileNotFoundError:
        # If file doesn't exist, create a new workbook and sheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Mood Analysis"
        # Add headers
        sheet.append(["Image_Name", "Final Mood"])

    # Append the image name and mood to the sheet
    sheet.append([image_name, mood])
    workbook.save(file_name)
    print(f"Final mood '{mood}' for image '{image_name}' saved to '{file_name}'.")

# Example dominant_colors list
dominant_colors = [
    {"name": "Sky Blue", "hex": "#87CEEB", "meaning": "Calmness, trust, serenity", "proportion": 40},
    {"name": "Sunset Orange", "hex": "#FF4500", "meaning": "Warmth, energy, excitement", "proportion": 35},
    {"name": "Soft Yellow", "hex": "#FFD700", "meaning": "Optimism, creativity, happiness", "proportion": 25},
]

# Display the mood of the image
def display_mood(dominant_colors):
    """
    Generate a mood summary based on the psychological meanings of dominant colors.

    Args:
        dominant_colors (list of dict): A list of dictionaries with the following keys:
            - 'name': The name of the color (e.g., "Sky Blue").
            - 'hex': The HEX code of the color (e.g., "#87CEEB").
            - 'meaning': The psychological meaning of the color (e.g., "Calmness, trust, serenity").
            - 'proportion': The proportion of the color in the image (e.g., 40).

    Returns:
        str: A mood summary based on the colors.
    """
    warm_colors = {"Red", "Orange", "Yellow"}
    cool_colors = {"Blue", "Green", "Purple"}
    neutral_colors = {"White", "Black", "Gray", "Brown"}

    warm_proportion = 0
    cool_proportion = 0
    neutral_proportion = 0

    print("=== Color Psychology Analysis ===\n")
    
    for color in dominant_colors:
        print(f"Color: {color['name']} (HEX: {color['hex']})")
        print(f"Meaning: {color['meaning']}")
        print(f"Proportion: {color['proportion']}%\n")

        # Categorize the color
        if color['name'] in warm_colors:
            warm_proportion += color['proportion']
        elif color['name'] in cool_colors:
            cool_proportion += color['proportion']
        elif color['name'] in neutral_colors:
            neutral_proportion += color['proportion']

    # Determine the overall mood
    mood = ""
    if warm_proportion > cool_proportion and warm_proportion > neutral_proportion:
        mood = "Energetic and Exciting"
    elif cool_proportion > warm_proportion and cool_proportion > neutral_proportion:
        mood = "Calm and Relaxing"
    elif neutral_proportion > warm_proportion and neutral_proportion > cool_proportion:
        mood = "Minimalistic and Neutral"
    else:
        mood = "Balanced and Harmonious"

    print("=== Overall Mood Summary ===")
    print(f"Mood: {mood}")
    print(f"Warm Colors: {warm_proportion}%")
    print(f"Cool Colors: {cool_proportion}%")
    print(f"Neutral Colors: {neutral_proportion}%")
    print("\nThis analysis is based on the proportions of the colors in the image.")

    return mood


# Determine the mood
image_name = "p1.jpg"  # Replace with the actual image name
final_mood = display_mood(dominant_colors)

# Save the mood to Excel
save_mood_to_excel("color_mood_analysis.xlsx",image_name, final_mood)

# Example usage
dominant_colors = [
    {"name": "Sky Blue", "hex": "#87CEEB", "meaning": "Calmness, trust, serenity", "proportion": 40},
    {"name": "Sunset Orange", "hex": "#FF4500", "meaning": "Warmth, energy, excitement", "proportion": 35},
    {"name": "Soft Yellow", "hex": "#FFD700", "meaning": "Optimism, creativity, happiness", "proportion": 25},
]


# Main function
def analyze_image(image_path):
    dominant_colors, _ = extract_dominant_colors(image_path)
    print("Dominant Colors (RGB):")
    for color in dominant_colors:
        print(f"RGB({int(color[0])}, {int(color[1])}, {int(color[2])})")

    plot_colors(dominant_colors)

    print("\nColor Psychology Analysis:")
    analysis = color_psychology(dominant_colors)
    for color, color_name, label, meaning in analysis:
        print(f"RGB({int(color[0])}, {int(color[1])}, {int(color[2])}): {color_name.capitalize()} - {label.capitalize()} - {meaning}")

# Example usage
if __name__ == "__main__":
    image_path = "D:\PYTHON\Sem6Project\VGG16-19\p1.jpg"  # Replace with your image path
    analyze_image(image_path)
