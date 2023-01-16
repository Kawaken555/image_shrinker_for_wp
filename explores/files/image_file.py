import copy
import os
import pathlib
import re
from common.constents.patterns import IMAGE_FILE_EXTENSION_PATTERN
from decimal import Decimal
from PIL import Image

class ImageFile: 
    file: Image    
    path: pathlib

    def __init__(self,target_file_path: pathlib , parents = False) -> None:    
        if not self.__is_image_file(target_file_path):
            raise Exception('jpg ないし png ファイルではありません') 
        self.file = Image.open(str(target_file_path))
        self.path = target_file_path
    
    def __is_image_file(self,target_folder_path)->bool:
        return re.match(IMAGE_FILE_EXTENSION_PATTERN,target_folder_path.name,flags=re.IGNORECASE)

    def is_width_more_than(self,target_width):
        width, height = self.file.size
        return width > target_width

    def is_height_more_than(self,target_height):
        width, height = self.file.size
        return height > target_height

    def shrink_image_with_witdh(self,target_width):

        width, height = self.file.size
        width_divide_num = Decimal(
            str(width / target_width)).quantize(Decimal("0.001"), rounding="ROUND_HALF_UP"
        )
        resized_image = self.file.resize(
            (
                round(width / width_divide_num),
                round(height / width_divide_num),
            ),
            Image.LANCZOS,
        )
        copied_image = self.copy()
        copied_image.file = resized_image
        return copied_image

    def save(self):
       self.file.save(self.path)

    def copy(self):
        return copy.deepcopy(self)

    def set_attr(self,file = None, path = None):
        copied_image = self.copy()
        if file is not None:
            copied_image.file = file
        if path is not None:
            copied_image.path = path
        return copied_image