def interpolate(start_rgb, end_rgb, percent_blend):
    new_rgb = []
    for i in range(0, 3):
        new_rgb.append((end_rgb[i] - start_rgb[i]) * percent_blend + start_rgb[i])
    return new_rgb


assert interpolate([255, 0, 0], [128, 128, 128], 0.5) == [191.5, 64.0, 64.0]


def assign_colors(data, colors):
    return [
        (datum, colors[i * len(colors) // len(data)])
        for i, datum in enumerate(data)]


def domain():
    pass


def range():
    pass
