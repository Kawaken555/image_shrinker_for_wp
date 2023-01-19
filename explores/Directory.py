import copy
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

    def get_inner_file_passes(self, pattern = None, exclude_paths = None) -> list:
        inner_file_list = []
        
        if pattern is None:
            inner_file_list = list(self.path.glob(RECURSIVE_PATH_PATTERN))      
        else: 
            inner_file_list = [path for path in self.path.glob(RECURSIVE_PATH_PATTERN) 
                if re.match(pattern,str(path),flags=re.IGNORECASE)]

        if exclude_paths is not None:
            exclueded_path_list = self.__exclude_specified_path(inner_file_list,exclude_paths)
            return exclueded_path_list
        else: 
            return inner_file_list      

    def __exclude_specified_path(self,target_path_list, exclude_path_list):
        extract_path_list = []
        for target_path in target_path_list:
            for exclude_path in exclude_path_list:
               if not str(target_path).startswith(str(exclude_path)):
                   extract_path_list.append(target_path)
        return extract_path_list

