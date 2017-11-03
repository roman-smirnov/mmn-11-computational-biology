# distinct color generator module


def _get_pattern(number):
    """ generate a pattern of which colors to take - i.e a binary triple"""
    # the pattern is a 3-tuple of the first 3 bits of a given number
    p_r = number & 1
    p_g = (number >> 1) & 1
    p_b = (number >> 2) & 1
    return p_r, p_g, p_b


def _get_color(number, delta):
    """ hash a number into an rgb color - delta is the separation between color values"""
    r, g, b = _get_pattern(number)  # which channels to set a value to
    val = 255 - delta * int(number / 8)  # the value to set for each color channel
    return r * val, g * val, b * val


def generate_rgb_colors(num_of_colors):
    """ generates a list of distinct rgb colors as 3-tuples """
    levels = int(num_of_colors / 8)
    delta = int(255 / (levels + 1))
    colors = [(0, 0, 0)]  # need to add black because it's skipped in the generation loop
    for num in range(0, num_of_colors + levels):  # +levels because each 8th element is skipped
        if num % 8 == 0:  # each 8th element is black - skip to avoid duplicates
            continue
        colors.append(_get_color(num, delta))  # hash number to rgb color triple
    return colors


def _get_color_as_tk_str(color):
    """ convert an rgb color 3-tuple into a tkinter hex color string (e.g #99ff33) """
    return "#%02x%02x%02x" % color  # convert to hex and skip the '0x' part of each element


def generate_tk_colors(num_of_colors):
    """ generate a list of distinct rgb colors as hex string with a hash prefix (e.g #99ff33)"""
    color_list = generate_rgb_colors(num_of_colors)  # generate a list of rgb color 3-tuples
    tk_color_list = []
    # convert each color into the tk color format and append to the list
    for color in color_list:
        tk_color_list.append(_get_color_as_tk_str(color))
    return tk_color_list
