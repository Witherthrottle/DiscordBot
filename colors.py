
color_list = [
    'Red', 'Blue', 'Green', 'Yellow', 'Orange', 'Purple', 'Pink', 'Brown', 'Cyan', 'Magenta',
    'Lime', 'Teal', 'Olive', 'Maroon', 'Navy', 'White', 'Black', 'Gray', 'Silver', 'Gold',
    'Indigo', 'Turquoise', 'Violet', 'Lavender', 'Plum', 'Coral', 'Salmon', 'Tomato', 'Khaki', 'SlateGray',
    'LightGreen', 'LightBlue', 'LightPink', 'LightGray', 'LightYellow', 'LightCyan', 'LightSalmon', 'LightSkyBlue', 'LightSteelBlue', 'LightSlateGray',
    'DarkRed', 'DarkBlue', 'DarkGreen', 'DarkYellow', 'DarkOrange', 'DarkPurple', 'DarkPink', 'DarkBrown', 'DarkCyan', 'DarkMagenta',
    'PaleRed', 'PaleBlue', 'PaleGreen', 'PaleYellow', 'PaleOrange', 'PalePurple', 'PalePink', 'PaleBrown', 'PaleCyan', 'PaleMagenta',
    'DeepRed', 'DeepBlue', 'DeepGreen', 'DeepYellow', 'DeepOrange', 'DeepPurple', 'DeepPink', 'DeepBrown', 'DeepCyan', 'DeepMagenta',
    'Azure', 'Chartreuse', 'Crimson', 'Gold', 'HotPink', 'LemonChiffon', 'OliveDrab', 'Orchid', 'Peru', 'RosyBrown',
    'SandyBrown', 'SeaGreen', 'Sienna', 'SpringGreen', 'SteelBlue', 'Thistle', 'YellowGreen', 'DarkSlateGray', 'MediumAquamarine', 'MediumPurple'
]

color_names = {
    'Red': (255, 0, 0),
    'Blue': (0, 0, 255),
    'Green': (0, 255, 0),
    'Yellow': (255, 255, 0),
    'Orange': (255, 165, 0),
    'Purple': (128, 0, 128),
    'Pink': (255, 192, 203),
    'Brown': (165, 42, 42),
    'Cyan': (0, 255, 255),
    'Magenta': (255, 0, 255),
    'Lime': (0, 255, 0),
    'Teal': (0, 128, 128),
    'Olive': (128, 128, 0),
    'Maroon': (128, 0, 0),
    'Navy': (0, 0, 128),
    'White': (255, 255, 255),
    'Black': (0, 0, 0),
    'Gray': (128, 128, 128),
    'Silver': (192, 192, 192),
    'Gold': (255, 215, 0),
    'Indigo': (75, 0, 130),
    'Turquoise': (64, 224, 208),
    'Violet': (238, 130, 238),
    'Lavender': (230, 230, 250),
    'Plum': (221, 160, 221),
    'Coral': (255, 127, 80),
    'Salmon': (250, 128, 114),
    'Tomato': (255, 99, 71),
    'Khaki': (240, 230, 140),
    'SlateGray': (112, 128, 144),
    'LightGreen': (144, 238, 144),
    'LightBlue': (173, 216, 230),
    'LightPink': (255, 182, 193),
    'LightGray': (211, 211, 211),
    'LightYellow': (255, 255, 224),
    'LightCyan': (224, 255, 255),
    'LightSalmon': (255, 160, 122),
    'LightSkyBlue': (135, 206, 250),
    'LightSteelBlue': (176, 196, 222),
    'LightSlateGray': (119, 136, 153),
    'DarkRed': (139, 0, 0),
    'DarkBlue': (0, 0, 139),
    'DarkGreen': (0, 100, 0),
    'DarkYellow': (255, 140, 0),
    'DarkOrange': (255, 140, 0),
    'DarkPurple': (48, 25, 52),
    'DarkPink': (231, 84, 128),
    'DarkBrown': (101, 67, 33),
    'DarkCyan': (0, 139, 139),
    'DarkMagenta': (139, 0, 139),
    'PaleRed': (255, 192, 203),
    'PaleBlue': (175, 238, 238),
    'PaleGreen': (152, 251, 152),
    'PaleYellow': (255, 255, 224),
    'PaleOrange': (255, 222, 173),
    'PalePurple': (221, 160, 221),
    'PalePink': (255, 182, 193),
    'PaleBrown': (152, 118, 84),
    'PaleCyan': (224, 255, 255),
    'PaleMagenta': (238, 130, 238),
    'DeepRed': (139, 0, 0),
    'DeepBlue': (0, 0, 139),
    'DeepGreen': (0, 100, 0),
    'DeepYellow': (255, 215, 0),
    'DeepOrange': (255, 140, 0),
    'DeepPurple': (153, 50, 204),
    'DeepPink': (255, 20, 147),
    'DeepBrown': (101, 67, 33),
    'DeepCyan': (0, 139, 139),
    'DeepMagenta': (139, 0, 139),
    'Azure': (240, 255, 255),
    'Chartreuse': (127, 255, 0),
    'Crimson': (220, 20, 60),
    'HotPink': (255, 105, 180),
    'LemonChiffon': (255, 250, 205),
    'OliveDrab': (107, 142, 35),
    'Orchid': (218, 112, 214),
    'Peru': (205, 133, 63),
    'RosyBrown': (188, 143, 143),
    'SandyBrown': (244, 164, 96),
    'SeaGreen': (46, 139, 87),
    'Sienna': (160, 82, 45),
    'SpringGreen': (0, 255, 127),
    'SteelBlue': (70, 130, 180),
    'Thistle': (216, 191, 216),
    'YellowGreen': (154, 205, 50),
    'DarkSlateGray': (47, 79, 79),
    'MediumAquamarine': (102, 205, 170),
    'MediumPurple': (147, 112, 219)
}