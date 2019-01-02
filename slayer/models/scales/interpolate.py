from __future__ import absolute_import

def _interpolate(start_rgb, end_rgb, percent_blend):
    """Interpolates an RGB value a specific percentage between two values

    Args:
        start_rgb (:obj:`list` of :obj:`int`): Beginning RGB color value
        end_rgb (:obj:`list` of :obj:`int`): Ending RGB color value
        percent_blend (float): % blend between two RGB values

    Returns:
        :obj:`list` of :obj:`float`: The RGB value between the specified colors.
    """
    new_rgb = []
    for i in range(0, 3):
        new_rgb.append((end_rgb[i] - start_rgb[i]) * percent_blend + start_rgb[i])
    return new_rgb


def interpolate(rgb_list, percent_blend):
    """Interpolates RGB value between a list of colors

    Todo:
        * Simplify function body

    Args:
        rgb_list (:obj:`list` of :obj:`list` of :obj:`int`): List of RGB values in a color scale.
        percent_blend (float): % blend between RGB values

    Returns:
        :obj:`list` of :obj:`float`: The RGB value between the specified colors.
    """
    if len(rgb_list) == 1:
        return rgb_list
    if len(rgb_list) == 2:
        return _interpolate(rgb_list[0], rgb_list[1], percent_blend)
    elif len(rgb_list) == 3:
        if percent_blend < 0.5:
            return _interpolate(rgb_list[0], rgb_list[1], percent_blend * 2)
        else:
            return _interpolate(rgb_list[1], rgb_list[2], percent_blend / 1.5)
    return
