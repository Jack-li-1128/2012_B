import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Wall dimensions from the provided image
wall_height = 3200  # mm
wall_width = 10100  # mm

# Excluded regions (doors and windows) from the provided image
excluded_rectangles = [
    (3500, 900, 3600, 2500),   # middle rectangle region (x, y, width, height)
    (7800, 900, 1100, 1400)  # right rectangle region (x, y, width, height)
]

excluded_circle = (850 + 900, 600 + 900, 900)  # left circle region (center_x, center_y, radius)

# Solar panel dimensions
main_panel_length = 1956  # mm
main_panel_width = 991    # mm
additional_panel_length = 1580  # mm
additional_panel_width = 808    # mm
smaller_panel_length = 310  # mm
smaller_panel_width = 355   # mm

# Create a new figure for the wall layout
fig, ax = plt.subplots(figsize=(15, 5))

# Draw the white area on the wall
ax.add_patch(patches.Rectangle((0, 0), wall_width, wall_height, edgecolor='black', facecolor='lightgrey', linewidth=2))

# Draw the excluded rectangle regions (doors and windows)
for region in excluded_rectangles:
    ax.add_patch(patches.Rectangle((region[0], region[1]), region[2], region[3], edgecolor='red', facecolor='none', linewidth=2, linestyle='dashed'))

# Draw the excluded circle region (door)
circle = patches.Circle((excluded_circle[0], excluded_circle[1]), excluded_circle[2], edgecolor='red', facecolor='none', linewidth=2, linestyle='dashed')
ax.add_patch(circle)

# Function to draw panels and store their positions without overlapping the excluded regions
def draw_panels(ax, panel_length, panel_width, color, wall_width, wall_height, excluded_rectangles, excluded_circle, existing_panels):
    x_positions = np.arange(0, wall_width, panel_length)
    y_positions = np.arange(0, wall_height, panel_width)
    panel_count = 0

    for x in x_positions:
        for y in y_positions:
            # Check if the panel is within the wall boundaries and not overlapping the excluded regions
            circle_center_x, circle_center_y, circle_radius = excluded_circle
            if (x + panel_length <= wall_width and
                y + panel_width <= wall_height and
                not any((x < region[0] + region[2] and x + panel_length > region[0] and y < region[1] + region[3] and y + panel_width > region[1]) for region in excluded_rectangles) and
                not any((x < p[0] + p[2] and x + panel_length > p[0] and y < p[1] + p[3] and y + panel_width > p[1]) for p in existing_panels) and
                not ((x < circle_center_x < x + panel_length or x < circle_center_x + panel_length < x + panel_length) and
                     (y < circle_center_y < y + panel_width or y < circle_center_y + panel_width < y + panel_width)) and
                not (np.sqrt((x - circle_center_x) ** 2 + (y - circle_center_y) ** 2) < circle_radius or
                     np.sqrt((x + panel_length - circle_center_x) ** 2 + (y - circle_center_y) ** 2) < circle_radius or
                     np.sqrt((x - circle_center_x) ** 2 + (y + panel_width - circle_center_y) ** 2) < circle_radius or
                     np.sqrt((x + panel_length - circle_center_x) ** 2 + (y + panel_width - circle_center_y) ** 2) < circle_radius)):
                ax.add_patch(patches.Rectangle((x, y), panel_length, panel_width, edgecolor=color, facecolor='none', linewidth=1))
                existing_panels.append((x, y, panel_length, panel_width))
                panel_count += 1
    return panel_count, existing_panels

# Store positions of existing panels to avoid overlap
existing_panels = []

# Draw main panels
main_panel_count, existing_panels = draw_panels(ax, main_panel_length, main_panel_width, 'blue', wall_width, wall_height, excluded_rectangles, excluded_circle, existing_panels)

# Draw additional panels
additional_panel_count, existing_panels = draw_panels(ax, additional_panel_length, additional_panel_width, 'green', wall_width, wall_height, excluded_rectangles, excluded_circle, existing_panels)

# Draw smaller panels
smaller_panel_count, existing_panels = draw_panels(ax, smaller_panel_length, smaller_panel_width, 'purple', wall_width, wall_height, excluded_rectangles, excluded_circle, existing_panels)

# Set limits and labels
ax.set_xlim(0, wall_width)
ax.set_ylim(0, wall_height)
ax.set_aspect('equal')
ax.set_title('Optimized Solar Panel Layout on Wall')
ax.set_xlabel('Length (mm)')
ax.set_ylabel('Height (mm)')

plt.gca().invert_yaxis()
plt.show()

# Print the number of panels of each type
print(f"_B2_{main_panel_count}")
print(f"_A3_{additional_panel_count}")
print(f"_C6_{smaller_panel_count}")
