from typing import Union
from pathlib import Path

from PIL import Image
import numpy as np

def avg_color_perimeter(image_path: Union[str, Path]) -> tuple:
    img = Image.open(image_path)
    img_np = np.array(img)

    width, height = img.size
    
    top_row = img_np[0]
    bottom_row = img_np[-1]
    left_column = [ img_np[i][0]  for i in range(1, height-1) ]
    right_column= [ img_np[i][-1] for i in range(1, height-1) ]

    border_pixels = []

    for sublist in [ top_row, bottom_row, left_column, right_column ]:
        if type(sublist[0]) is list or type(sublist[0]) is np.ndarray:
            for item in sublist:
                border_pixels.append(item)
        else: 
            border_pixels.append(sublist)

        mean_r_value = np.mean( [ pixel[0] for pixel in border_pixels ] )
        mean_g_value = np.mean( [ pixel[1] for pixel in border_pixels ] )
        mean_b_value = np.mean( [ pixel[2] for pixel in border_pixels ] )

        return (mean_r_value, mean_g_value, mean_b_value)

def is_background_too_dark(image_path: Union[str, Path], threshold: int=50) -> bool:
    avg_r, avg_g, avg_b = avg_color_perimeter(image_path)
    if avg_r <= threshold and avg_g <= threshold and avg_b <= threshold:
        return True
    return False

def find_epub_directories(root_dir):
    epubs = []

    for dirpath, _, files in os.walk(root_dir):
        for filename in fnmatch.filter(files, '*.epub'):
            epubs.append(Path(dirpath))

    return epubs