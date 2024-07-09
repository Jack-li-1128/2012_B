import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Wall dimensions from the provided image
wall_height = 1389.24  # mm
wall_width = 10100  # mm
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Wall dimensions from the provided image
wall_height = 1389.24  # mm
wall_width = 10100  # mm

# Solar panel dimensions
main_panel_length = 1300  # mm
main_panel_width = 1100   # mm
additional_panel_length = 1321  # mm
additional_panel_width = 711    # mm
smaller_panel_length = 310  # mm
smaller_panel_width = 355   # mm

# Create a new figure for the wall layout
fig, ax = plt.subplots(figsize=(15, 5))

# Draw the wall area
ax.add_patch(patches.Rectangle((0, 0), wall_width, wall_height, edgecolor='black', facecolor='lightgrey', linewidth=2))

# Function to check if a rectangle is inside the wall
def is_inside_wall(x, y, panel_length, panel_width, wall_width, wall_height):
    return (x + panel_length <= wall_width) and (y + panel_width <= wall_height)

# Function to draw panels and store their positions without overlapping
def draw_panels_on_wall(ax, panel_length, panel_width, color, wall_width, wall_height, existing_panels):
    panel_count = 0
    panel_positions = []
    x_positions = np.arange(0, wall_width, panel_length)

    for x in x_positions:
        for y in np.arange(0, wall_height, panel_width):
            if (is_inside_wall(x, y, panel_length, panel_width, wall_width, wall_height) and
                not any((x < p[0] + p[2] and x + panel_length > p[0] and y < p[1] + p[3] and y + panel_width > p[1]) for p in panel_positions + existing_panels)):
                ax.add_patch(patches.Rectangle((x, y), panel_length, panel_width, edgecolor=color, facecolor='none', linewidth=1))
                panel_positions.append((x, y, panel_length, panel_width))
                panel_count += 1
    return panel_count, panel_positions

# Store positions of existing panels to avoid overlap
existing_panels = []

# Draw main panels
main_panel_count, main_panel_positions = draw_panels_on_wall(ax, main_panel_length, main_panel_width, 'blue', wall_width, wall_height, existing_panels)
existing_panels.extend(main_panel_positions)

# Draw additional panels
additional_panel_count, additional_panel_positions = draw_panels_on_wall(ax, additional_panel_length, additional_panel_width, 'green', wall_width, wall_height, existing_panels)
existing_panels.extend(additional_panel_positions)

# Draw smaller panels
smaller_panel_count, smaller_panel_positions = draw_panels_on_wall(ax, smaller_panel_length, smaller_panel_width, 'purple', wall_width, wall_height, existing_panels)
existing_panels.extend(smaller_panel_positions)

# Set limits and labels
ax.set_xlim(0, wall_width)
ax.set_ylim(0, wall_height)
ax.set_aspect('equal')
ax.set_title('Optimized Solar Panel Layout on Wall')
ax.set_xlabel('Length (mm)')
ax.set_ylabel('Height (mm)')
ax.invert_yaxis()

plt.show()

# Print the number of panels of each type
print(f"Number of 1300 mm × 1100 mm panels: {main_panel_count}")
print(f"Number of 1321 mm × 711 mm panels: {additional_panel_count}")
print(f"Number of 310 mm × 355 mm panels: {smaller_panel_count}")

# Solar panel dimensions
main_panel_length = 1300  # mm
main_panel_width = 1100    # mm
additional_panel_length = 1321  # mm
additional_panel_width = 711    # mm
smaller_panel_length = 310  # mm
smaller_panel_width = 355   # mm








print(f"_C1_{main_panel_count}")
print(f"_C2_{additional_panel_count}")
print(f"_C6_{smaller_panel_count}")