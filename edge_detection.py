"""
This iterative code shows the difference in the output image when a 
edge detection filter is applied depending on the filter values
and if a gaussian blur is applied before the edge detection.

Usually applying a blur before the edge detection is a good practive
because it removes the high frequency details of the image, making it
easier to find real edges
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Load an image from a given path
image_path = "test_images/embraer.jpg"  # Replace with the path to your image
original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Create a figure for displaying the image, filter, and output
fig, (ax_image, ax_filter, ax_output) = plt.subplots(1, 3, figsize=(12, 4))

# Initialize filter values
filter_values = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

# Initialize blur flag and button color
apply_blur = False
button_color = 'lightgoldenrodyellow'

# Apply the Sobel operator filter
def apply_filter():
    if apply_blur:
        image = cv2.GaussianBlur(original_image, (5, 5), 0)
    else:
        image = original_image

    filtered_image = cv2.filter2D(image, -1, filter_values)
    ax_output.imshow(filtered_image, cmap="gray")
    ax_output.set_title("Filtered Image")
    plt.draw()

# Display the original image
ax_image.imshow(original_image, cmap="gray")
ax_image.set_title("Original Image")

# Display the filter values
ax_filter.imshow(filter_values, cmap="gray")
ax_filter.set_title("Filter Values")

# Create sliders for filter values
filter_slider_ax = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
filter_slider = Slider(filter_slider_ax, 'Filter', -10, 10, valinit=0)

# Update filter_values and filtered image when slider value changes
def update(val):
    global filter_values
    filter_values = val * np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    ax_filter.imshow(filter_values, cmap="gray")
    ax_filter.set_title("Filter Values")
    apply_filter()

filter_slider.on_changed(update)

# Create a button to toggle blur
blur_button_ax = plt.axes([0.2, 0.1, 0.1, 0.04])
blur_button = Button(blur_button_ax, 'Blur', color=button_color)

# Function to toggle blur and update button color
def toggle_blur(event):
    global apply_blur, button_color
    apply_blur = not apply_blur
    if apply_blur:
        button_color = 'lightcoral'  # Change color to red when toggled on
    else:
        button_color = 'lightgoldenrodyellow'  # Change color to yellow when toggled off
    blur_button.color = button_color  # Update button color
    apply_filter()

blur_button.on_clicked(toggle_blur)

# Show the plot
plt.subplots_adjust(bottom=0.2)
plt.show()
