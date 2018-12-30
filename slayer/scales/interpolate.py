def interpolate(start_rgb, end_rgb, percent_blend):
    """Interpolates an RGB value a specific percentage between two values

    Args:
        start_rgb (`tuple` of `int`): Beginning RGB color value
        end_rgb (`tuple` of `int`): Ending RGB color value
        percent_blend (float): % between two RGB values
    """
    new_rgb = []
    for i in range(0, 3):
        new_rgb.append((end_rgb[i] - start_rgb[i]) * percent_blend + start_rgb[i])
    return new_rgb
