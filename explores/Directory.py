import os
import pathlib
import re

from common.constents.patterns import RECURSIVE_PATH_PATTERN


class Directory:
    
    path:pathlib
    
    def __init__(self, target_directory_pass: pathlib, parents = False) -> None:
        self.path = target_directory_pass
        if not self.__exist_target_directory():
            self.path.mkdir(parents)
        os.chmod(self.path,0o777)
            
    def __exist_target_directory(self) -> bool:
        return self.path.is_dir()

    def get_inner_file_passes(self, pattern = None) -> list:
        if pattern is None:
            return list(self.path.glob(RECURSIVE_PATH_PATTERN))     
        else: 
            a = [path for path in self.path.glob(RECURSIVE_PATH_PATTERN) 
                if re.match(pattern,str(path),flags=re.IGNORECASE)]

            return  [path for path in self.path.glob(RECURSIVE_PATH_PATTERN) 
                if re.match(pattern,str(path),flags=re.IGNORECASE)]

             
