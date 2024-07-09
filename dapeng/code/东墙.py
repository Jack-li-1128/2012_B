import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Define the coordinates of the polygon representing the wall
wall_coords = [(0, 0), (7100, 0), (7100, 3200), (6400, 4400), (0, 3200)]

# Door dimensions
door_bottom_left = (2600, 0)
door_width = 1100  # mm
door_height = 2500  # mm

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

# Draw the door area
door = patches.Rectangle(door_bottom_left, door_width, door_height, edgecolor='red', facecolor='none', linewidth=2, linestyle='dashed')
ax.add_patch(door)

# Function to check if a rectangle is inside the polygon and not overlapping the door
def is_inside_polygon_and_not_door(x, y, panel_length, panel_width, polygon, door_bottom_left, door_width, door_height):
    panel_corners = [(x, y), (x + panel_length, y), (x, y + panel_width), (x + panel_length, y + panel_width)]
    door_corners = [
        door_bottom_left,
        (door_bottom_left[0] + door_width, door_bottom_left[1]),
        (door_bottom_left[0], door_bottom_left[1] + door_height),
        (door_bottom_left[0] + door_width, door_bottom_left[1] + door_height)
    ]
    # Check if any panel corner is inside the door area
    if any(door_bottom_left[0] <= corner[0] <= door_bottom_left[0] + door_width and
           door_bottom_left[1] <= corner[1] <= door_bottom_left[1] + door_height for corner in panel_corners):
        return False
    # Check if any panel corner is inside the wall polygon
    return all(patches.Path(polygon).contains_point(corner) for corner in panel_corners)

# Function to draw panels and store their positions without overlapping
def draw_panels_on_wall(ax, panel_length, panel_width, color, wall_coords, door_bottom_left, door_width, door_height, existing_panels):
    panel_count = 0
    panel_positions = []
    x_positions = np.arange(0, max(pt[0] for pt in wall_coords), panel_length)

    for x in x_positions:
        for y in np.arange(0, max(pt[1] for pt in wall_coords), panel_width):
            if (is_inside_polygon_and_not_door(x, y, panel_length, panel_width, wall_coords, door_bottom_left, door_width, door_height) and
                not any((x < p[0] + p[2] and x + panel_length > p[0] and y < p[1] + p[3] and y + panel_width > p[1]) for p in panel_positions + existing_panels)):
                ax.add_patch(patches.Rectangle((x, y), panel_length, panel_width, edgecolor=color, facecolor='none', linewidth=1))
                panel_positions.append((x, y, panel_length, panel_width))
                panel_count += 1
    return panel_count, panel_positions

# Store positions of existing panels to avoid overlap
existing_panels = []

# Draw main panels
main_panel_count, main_panel_positions = draw_panels_on_wall(ax, main_panel_length, main_panel_width, 'blue', wall_coords, door_bottom_left, door_width, door_height, existing_panels)
existing_panels.extend(main_panel_positions)

# Draw additional panels
additional_panel_count, additional_panel_positions = draw_panels_on_wall(ax, additional_panel_length, additional_panel_width, 'green', wall_coords, door_bottom_left, door_width, door_height, existing_panels)
existing_panels.extend(additional_panel_positions)

# Draw smaller panels
smaller_panel_count, smaller_panel_positions = draw_panels_on_wall(ax, smaller_panel_length, smaller_panel_width, 'purple', wall_coords, door_bottom_left, door_width, door_height, existing_panels)
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
print(f"_C1_{main_panel_count}")
print(f"_C2_{additional_panel_count}")
print(f"_C6_{smaller_panel_count}")
