import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Define the coordinates of the polygon representing the wall
wall_coords = [(0, 0), (7100, 0), (7100, 3200), (6400, 4400), (0, 3200)]

# Solar panel dimensions
main_panel_length = 1300  # mm
main_panel_width = 1100   # mm
additional_panel_length = 1321  # mm
additional_panel_width = 711    # mm
smaller_panel_length = 310  # mm
smaller_panel_width = 355   # mm

# Create a new figure for the wall layout
fig, ax = plt.subplots(figsize=(15, 8))

# Draw the polygon representing the wall
wall_polygon = patches.Polygon(wall_coords, closed=True, edgecolor='black', facecolor='lightgrey', linewidth=2)
ax.add_patch(wall_polygon)

# Function to check if a rectangle is inside the polygon
def is_inside_polygon(x, y, panel_length, panel_width, polygon):
    panel_corners = [(x, y), (x + panel_length, y), (x, y + panel_width), (x + panel_length, y + panel_width)]
    return all(patches.Path(polygon).contains_point(corner) for corner in panel_corners)

# Function to draw panels and store their positions without overlapping
def draw_panels_on_wall(ax, panel_length, panel_width, color, wall_coords, existing_panels, rotate=False, start_y=0):
    panel_count = 0
    panel_positions = []
    x_positions = np.arange(0, max(pt[0] for pt in wall_coords), panel_length if not rotate else panel_width)
    y_positions = np.arange(start_y, max(pt[1] for pt in wall_coords), panel_width if not rotate else panel_length)

    for y in y_positions:
        for x in x_positions:
            if rotate:
                if (is_inside_polygon(x, y, panel_width, panel_length, wall_coords) and
                    not any((x < p[0] + p[2] and x + panel_width > p[0] and y < p[1] + p[3] and y + panel_length > p[1]) for p in panel_positions + existing_panels)):
                    ax.add_patch(patches.Rectangle((x, y), panel_width, panel_length, edgecolor=color, facecolor='none', linewidth=1))
                    panel_positions.append((x, y, panel_width, panel_length))
                    panel_count += 1
            else:
                if (is_inside_polygon(x, y, panel_length, panel_width, wall_coords) and
                    not any((x < p[0] + p[2] and x + panel_length > p[0] and y < p[1] + p[3] and y + panel_width > p[1]) for p in panel_positions + existing_panels)):
                    ax.add_patch(patches.Rectangle((x, y), panel_length, panel_width, edgecolor=color, facecolor='none', linewidth=1))
                    panel_positions.append((x, y, panel_length, panel_width))
                    panel_count += 1
    return panel_count, panel_positions

# Store positions of existing panels to avoid overlap
existing_panels = []

# Draw smaller panels horizontally at the top
smaller_panel_top_count, smaller_panel_top_positions = draw_panels_on_wall(ax, smaller_panel_length, smaller_panel_width, 'purple', wall_coords, existing_panels, rotate=False, start_y=max(pt[1] for pt in wall_coords) - smaller_panel_width)
existing_panels.extend(smaller_panel_top_positions)

# Draw main panels horizontally from left to right, bottom to top
main_panel_count, main_panel_positions = draw_panels_on_wall(ax, main_panel_length, main_panel_width, 'blue', wall_coords, existing_panels, rotate=False, start_y=0)
existing_panels.extend(main_panel_positions)

# Draw main panels vertically from left to right, bottom to top
main_panel_vertical_count, main_panel_vertical_positions = draw_panels_on_wall(ax, main_panel_length, main_panel_width, 'blue', wall_coords, existing_panels, rotate=True, start_y=0)
main_panel_count += main_panel_vertical_count
existing_panels.extend(main_panel_vertical_positions)

# Draw additional panels next from left to right, bottom to top, not rotated
additional_panel_count, additional_panel_positions = draw_panels_on_wall(ax, additional_panel_length, additional_panel_width, 'green', wall_coords, existing_panels, rotate=False, start_y=0)
existing_panels.extend(additional_panel_positions)

# Draw smaller panels last from left to right, bottom to top, not rotated
smaller_panel_count, smaller_panel_positions = draw_panels_on_wall(ax, smaller_panel_length, smaller_panel_width, 'purple', wall_coords, existing_panels, rotate=False, start_y=0)
existing_panels.extend(smaller_panel_positions)

# Set limits and labels
ax.set_xlim(0, max(pt[0] for pt in wall_coords))
ax.set_ylim(0, max(pt[1] for pt in wall_coords))
ax.set_aspect('equal')
ax.set_title('Optimized Solar Panel Layout on Wall')
ax.set_xlabel('Length (mm)')
ax.set_ylabel('Height (mm)')
ax.invert_yaxis()

plt.show()

# Print the number of panels of each type
print(f"Number of 1300 mm × 1100 mm panels: {main_panel_count}")
print(f"Number of 1321 mm × 711 mm panels: {additional_panel_count}")
print(f"Number of 310 mm × 355 mm panels: {smaller_panel_count + smaller_panel_top_count}")
