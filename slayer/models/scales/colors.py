from __future__ import absolute_import

import numpy as np


def get_random_rgb():
    """Generate a random RGB value

    Returns:
        :obj:`list` of :obj:`float`: Random RGB array
    """
    return [round(np.random.random()*255) for _ in range(0, 3)]


"""
Selection of colors from http://colorbrewer2.org/
"""
DEFAULT_PALETTES = {
    # sequential scales
    'BuGr': [[229, 245, 249], [44, 162, 95]],
    'BuPu': [[224, 236, 244], [136, 86, 167]],
    'GnBu': [[224, 243, 219], [67, 162, 202]],
    'OrRd': [[254, 232, 200], [227, 74, 51]],
    'PuBu': [[236, 231, 242], [43, 140, 190]],
    'PuBuGn': [[236, 226, 240], [28, 144, 153]],
    'PuRd': [[231, 225, 239], [221, 28, 119]],
    'RdPu': [[253, 224, 221], [197, 27, 138]],
    'YlGn': [[247, 252, 185], [49, 163, 84]],
    'YlGnBu': [[237, 248, 177], [44, 127, 184]],
    'YlOrBr': [[255, 247, 188], [217, 95, 14]],
    'YlOrRd': [[255, 237, 160], [240, 59, 32]],
    'Blues': [[222, 235, 247], [49, 130, 189]],
    'Greens': [[229, 245, 224], [49, 163, 84]],
    'Greys': [[240, 240, 240], [99, 99, 99]],
    'Oranges': [[254, 230, 206], [230, 85, 13]],
    'Purples': [[239, 237, 245], [117, 107, 177]],
    'Reds': [[254, 224, 210], [222, 45, 38]],
    # diverging scales
    'BrBG': [[216, 179, 101], [245, 245, 245], [90, 180, 172]],
    'PiYG': [[233, 163, 201], [247, 247, 247], [161, 215, 106]],
    'PRGn': [[175, 141, 195], [247, 247, 247], [127, 191, 123]],
    'RdYlBu': [[252, 141, 89], [255, 255, 191], [145, 191, 219]],
    # qualitative scales
    'accent': [
        [127, 201, 127],
        [190, 174, 212],
        [253, 192, 134],
        [255, 255, 153],
        [56, 108, 176],
        [240, 2, 127],
        [191, 91, 23],
        [102, 102, 102]
    ],
    'dark2': [
        [27, 158, 119],
        [217, 95, 2],
        [117, 112, 179],
        [231, 41, 138],
        [102, 166, 30],
        [230, 171, 2],
        [166, 118, 29],
        [102, 102, 102]
    ],
    'paired': [
        [166, 206, 227],
        [31, 120, 180],
        [178, 223, 138],
        [51, 160, 44],
        [251, 154, 153],
        [227, 26, 28],
        [253, 191, 111],
        [255, 127, 0]
    ],
    'pastel1': [
        [251, 180, 174],
        [179, 205, 227],
        [204, 235, 197],
        [222, 203, 228],
        [254, 217, 166],
        [255, 255, 204],
        [229, 216, 189],
        [253, 218, 236]
    ],
    'set1': [
        [228, 26, 28],
        [55, 126, 184],
        [77, 175, 74],
        [152, 78, 163],
        [255, 127, 0],
        [255, 255, 51],
        [166, 86, 40],
        [247, 129, 191]
    ],
    'set2': [
        [102, 194, 165],
        [252, 141, 98],
        [141, 160, 203],
        [231, 138, 195],
        [166, 216, 84],
        [255, 217, 47],
        [229, 196, 148],
        [179, 179, 179]
    ]
}
