from pathlib import Path
from typing import Union

import pytesseract
from PIL import Image, ImageOps
import numpy as np

from sabi import utils

class ImgFile:

    def __init__(self, imagepath):
        self.i = imagepath

class ImageReader:

    def __init__(self, imagepath: Union[str, Path], verbose: bool=False):
        self._imagepath = imagepath
        self.verbose = verbose

        self._invert_flag = False

    @property
    def imagepath(self) -> Union[str, Path]:
        return self._imagepath
    @imagepath.setter
    def imagepath(self, value: Union[str, Path]) -> None:
        self._imagepath = value

    @property
    def img(self) -> Image:
        if utils.is_background_too_dark(self.imagepath) and self._invert_flag:
            return self.invert_image()
        return Image.open(self.imagepath)
    @property
    def invert_flag(self) -> bool:
        self._invert_flag = not self._invert_flag
        if self.verbose: print(f"ImageReader({self._imagepath.name}).invert_flag is set to '{self._invert_flag}'")
        return self._invert_flag


    def invert_image(self) -> Image:
        img = Image.open(self.imagepath)
        
        # Convert image to RGB if it's not
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        inverted_img = ImageOps.invert(img)

        if self.verbose: print(f"ImageReader({self._imagepath.name}).invert_image completed")

        return inverted_img

    def read_image(self) -> str:
        np_image = np.array(self.img)
        np_image = np.array(Image.open(self.imagepath))
        if self.verbose: print(f"ImageReader({self._imagepath.name}).read_image() processing")
        text = pytesseract.image_to_string(np_image)
        return text

    @classmethod
    def from_filepath(cls, filepath: Union[str, Path]) -> 'ImageReader':
        return cls(filepath)