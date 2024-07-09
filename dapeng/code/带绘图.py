import matplotlib.pyplot as plt
import matplotlib.patches as patches


def calculate_filling_ratio(box_width, box_height, items):
    """
    计算二维装箱问题的填充率。

    :param box_width: 箱子的宽度
    :param box_height: 箱子的高度
    :param items: 物品的尺寸列表，每个物品是一个 (width, height) 元组
    :return: 填充率
    """
    total_box_area = box_width * box_height
    placed_items_area = 0

    # 初始化放置位置
    x_offset = 0
    y_offset = 0
    max_height_in_row = 0

    fig, ax = plt.subplots()
    ax.set_xlim(0, box_width)
    ax.set_ylim(0, box_height)

    # 放置物件的回溯函数
    def place_items(x_offset, y_offset):
        nonlocal placed_items_area
        if y_offset + min([h for w, h in items]) > box_height:
            return

        row_height = 0
        for w, h in items:
            if x_offset + w <= box_width and y_offset + h <= box_height:
                rect = patches.Rectangle((x_offset, y_offset), w, h, linewidth=1, edgecolor='r', facecolor='blue')
                ax.add_patch(rect)
                placed_items_area += w * h
                x_offset += w
                row_height = max(row_height, h)
                if x_offset + w > box_width:
                    x_offset = 0
                    y_offset += row_height
                place_items(x_offset, y_offset)
            else:
                break

    place_items(x_offset, y_offset)

    plt.gca().invert_yaxis()
    plt.show()

    filling_ratio = placed_items_area / total_box_area
    return filling_ratio


# 箱子尺寸
box_width = 10.1
box_height = 6.51153

# 小物件尺寸
items = [(1.58, 0.8), (0.8, 1.58), (0.310, 0.355), (0.355, 0.310)]

filling_ratio = calculate_filling_ratio(box_width, box_height, items)
print(f"填充率: {filling_ratio:.2%}")
