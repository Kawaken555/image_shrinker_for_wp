import pathlib
from typing import List

from common.constents.textencoding import UTF_8

class TextFile: 
    path: pathlib

    def __init__(self,target_file_path: pathlib) -> None:
        self.path = target_file_path    
        if not self.__exist_target_file():
            self.path.touch()   
     
    def __exist_target_file (self) -> bool:
        return self.path.is_file()

    def add_texts_from_list(self,new_texts: List[str]):
        with self.path.open(mode='a+', encoding=UTF_8) as f:
            contents_list: List[str] = f.readlines()
            for new_text in new_texts:
                contents_list.append(new_text  + "\n")
            f.writelines(contents_list)

    def get_contents_textlist(self):
        with self.path.open(mode = 'r', encoding=UTF_8) as f:
            return [s.strip() for s in f.readlines()]
