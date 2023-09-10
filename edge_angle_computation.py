import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb

# Creation of a HSV color wheel
rho = np.linspace(0, 1, 100)  # Radius of 1, distance from center to outer edge
phi = np.linspace(-np.pi, np.pi, 1000)  # in radians, one full circle

RHO, PHI = np.meshgrid(rho, phi)  # get every combination of rho and phi

h = (PHI - PHI.min()) / (PHI.max() - PHI.min())  # use angle to determine hue, normalized from 0-1
h = np.flip(h)
s = RHO  # saturation is set as a function of radias
v = np.ones_like(RHO)  # value is constant

# convert the np arrays to lists. This actually speeds up the colorsys call
h, s, v = h.flatten().tolist(), s.flatten().tolist(), v.flatten().tolist()
c = hsv_to_rgb([list(x) for x in zip(h, s, v)])
c = np.array(c)

# Load an image from a given path
image_path = "test_images/flower2.jpg"  # Replace with the path to your image
original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Apply Gaussian blur to the original image
blurred_image = cv2.GaussianBlur(original_image, (5, 5), 0)

# Apply Sobel operators for horizontal and vertical edge detection
sobelx = cv2.Sobel(blurred_image, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(blurred_image, cv2.CV_64F, 0, 1, ksize=3)

# Calculate the magnitude and direction of the edge
magnitude = np.sqrt(sobelx**2 + sobely**2)
direction = np.arctan2(sobely, sobelx)

# Normalize direction values to [0, 1]
direction_normalized = (direction + np.pi) / (2 * np.pi)
direction_normalized = np.flip(direction_normalized)  

# Create a color map based on the edge direction in the HSV color space
color_map = np.zeros((direction.shape[0], direction.shape[1], 3), dtype=np.uint8)
color_map[..., 0] = (direction_normalized * 255).astype(np.uint8)
color_map[..., 1] = 255
color_map[..., 2] = 255

# Convert HSV to BGR for display
colored_edges = cv2.cvtColor(color_map, cv2.COLOR_HSV2RGB)

# Define a threshold value
threshold = 70  # Adjust this value as needed

# Create a binary mask based on the threshold
edge_mask = (magnitude > threshold).astype(np.uint8) * 255

# Apply the color map to the thresholded image
colored_output = cv2.bitwise_and(colored_edges, colored_edges, mask=edge_mask)

# Create the HSV color circle using a polar projection
fig = plt.figure(figsize=(16, 4))

ax_original = fig.add_subplot(141)
ax_edge = fig.add_subplot(142)
ax_colored = fig.add_subplot(143)
ax_color_circle = fig.add_subplot(144, projection='polar')

# Display the original image, edge magnitude, color-coded result, and the HSV color circle
ax_original.imshow(original_image, cmap="gray")
ax_original.set_title("Original Image")

ax_edge.imshow(edge_mask, cmap="gray")
ax_edge.set_title("Edge Magnitude")

#ax_colored.imshow(cv2.cvtColor(colored_output, cv2.COLOR_BGR2RGB))
ax_colored.imshow(colored_output)
ax_colored.set_title("Color-Coded Edges")

ax_color_circle.scatter(PHI, RHO, c=c)
ax_color_circle.set_title("HSV Color Circle")
_ = ax_color_circle.axis('off')

# Show the plot
plt.tight_layout()
plt.show()
