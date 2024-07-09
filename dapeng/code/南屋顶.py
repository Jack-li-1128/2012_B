import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Roof dimensions in mm
roof_length = 10100
roof_width = 6511.53
opening_length = 3600
opening_width = 1360
opening_left_edge = 1383.7
opening_top_edge = 2800

# Solar panel dimensions
main_panel_length = 1650
main_panel_width = 991
additional_panel_length = 1300
additional_panel_width = 1100
smaller_panel_length = 310
smaller_panel_width = 355

# Create a new figure for the optimized layout
fig, ax = plt.subplots(figsize=(12, 8))

# Draw the roof
ax.add_patch(patches.Rectangle((0, 0), roof_length, roof_width, edgecolor='black', facecolor='lightgrey', linewidth=2))

# Draw the opening
ax.add_patch(patches.Rectangle((opening_left_edge, opening_top_edge), opening_length, opening_width, edgecolor='red', facecolor='none', linewidth=2, linestyle='dashed'))

# Function to draw panels without overlapping
def draw_panels(ax, panel_length, panel_width, color, roof_length, roof_width, opening_left_edge, opening_top_edge, opening_length, opening_width, existing_panels):
    x_positions = np.arange(0, roof_length, panel_length)
    y_positions = np.arange(0, roof_width, panel_width)
    panel_count = 0

    for x in x_positions:
        for y in y_positions:
            # Check if the panel is within the roof boundaries and not overlapping the opening or other panels
            if (x + panel_length <= roof_length and
                y + panel_width <= roof_width and
                not (opening_left_edge < x + panel_length and
                     x < opening_left_edge + opening_length and
                     opening_top_edge < y + panel_width and
                     y < opening_top_edge + opening_width) and
                not any((x < p[0] + p[2] and x + panel_length > p[0] and y < p[1] + p[3] and y + panel_width > p[1]) for p in existing_panels)):
                ax.add_patch(patches.Rectangle((x, y), panel_length, panel_width, edgecolor=color, facecolor='none', linewidth=1))
                existing_panels.append((x, y, panel_length, panel_width))
                panel_count += 1
    return panel_count, existing_panels

# Store positions of existing panels to avoid overlap
existing_panels = []

# Draw main panels
main_panel_count, existing_panels = draw_panels(ax, main_panel_length, main_panel_width, 'blue', roof_length, roof_width, opening_left_edge, opening_top_edge, opening_length, opening_width, existing_panels)

# Draw additional panels
additional_panel_count, existing_panels = draw_panels(ax, additional_panel_length, additional_panel_width, 'green', roof_length, roof_width, opening_left_edge, opening_top_edge, opening_length, opening_width, existing_panels)

# Draw smaller panels
smaller_panel_count, existing_panels = draw_panels(ax, smaller_panel_length, smaller_panel_width, 'purple', roof_length, roof_width, opening_left_edge, opening_top_edge, opening_length, opening_width, existing_panels)

# Draw additional smaller panels in the specified range (4000 to 5000 mm)
def draw_smaller_panels_in_range(ax, start_width, end_width, panel_length, panel_width, color, roof_length, roof_width, opening_left_edge, opening_top_edge, opening_length, opening_width, existing_panels):
    x_positions = np.arange(0, roof_length, panel_length)
    y_positions = np.arange(start_width, end_width, panel_width)
    panel_count = 0

    for x in x_positions:
        for y in y_positions:
            # Check if the panel is within the specified width range, roof boundaries, and not overlapping the opening or other panels
            if (x + panel_length <= roof_length and
                y + panel_width <= roof_width and
                not (opening_left_edge < x + panel_length and
                     x < opening_left_edge + opening_length and
                     opening_top_edge < y + panel_width and
                     y < opening_top_edge + opening_width) and
                not any((x < p[0] + p[2] and x + panel_length > p[0] and y < p[1] + p[3] and y + panel_width > p[1]) for p in existing_panels)):
                ax.add_patch(patches.Rectangle((x, y), panel_length, panel_width, edgecolor=color, facecolor='none', linewidth=1, linestyle='dotted'))
                existing_panels.append((x, y, panel_length, panel_width))
                panel_count += 1
    return panel_count, existing_panels

# Draw smaller panels in the specified range
range_panel_count, existing_panels = draw_smaller_panels_in_range(ax, 4000, 5000, smaller_panel_length, smaller_panel_width, 'purple', roof_length, roof_width, opening_left_edge, opening_top_edge, opening_length, opening_width, existing_panels)

# Set limits and labels
ax.set_xlim(0, roof_length)
ax.set_ylim(0, roof_width)
ax.set_aspect('equal')
ax.set_title('Optimized Solar Panel Layout on Roof')
ax.set_xlabel('Length (mm)')
ax.set_ylabel('Width (mm)')
# Print the number of panels of each type
s = f"_B1_{main_panel_count}"
s += f"_C1_{additional_panel_count}"
# Total number of smaller panels including the ones in the specified range
total_smaller_panels = smaller_panel_count + range_panel_count
s += f"_C6_{total_smaller_panels}"
plt.gca().invert_yaxis()
plt.savefig('F:\\Git\\2012_B\\dapeng\\图片生成\\'+s)
plt.show()



