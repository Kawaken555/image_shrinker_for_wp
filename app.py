
import os
import pathlib
import sys
from tkinter import messagebox
from common.constents.filesize import WP_MAX_WIDTH
from common.constents.pathname import CACHE_FILE_PATH, RESIZED_FOLDER_PATH
from common.constents.patterns import IMAGE_FILE_EXTENSION_PATTERN
from explores.directori import Directory
from explores.files.image_file import ImageFile
from explores.files.text_file import TextFile

def get_current_dir_path():
    return pathlib.Path(os.path.realpath(os.path.dirname(sys.argv[0])))
def get_resized_image_dir_path():
    current_dir_path = str(get_current_dir_path())
    return pathlib.Path(current_dir_path + RESIZED_FOLDER_PATH)
def get_current_dir_image_content_paths(current_dir,exclude_path):
    return current_dir.get_inner_file_passes(IMAGE_FILE_EXTENSION_PATTERN, exclude_path)

def convert_paths_to_imagefiles(image_file_paths):
    image_list = []
    for image_file_path in image_file_paths:
        image_list.append(ImageFile(image_file_path))
    return image_list    

def convert_current_path_to_save_target_path(current_dir,target_image_list):
    converted_image_list =[]
    for target_image in target_image_list:
        converted_image = target_image.set_attr(path = __create_absolute_save_target_path(target_image.path,current_dir.path))
        converted_image_list.append(converted_image)
    return converted_image_list

def __create_absolute_save_target_path(target_path,current_dir_path):
        relative_path = str(target_path).replace(str(current_dir_path),'')
        formatted_relative_path = RESIZED_FOLDER_PATH + relative_path
        absolute_save_target_path = pathlib.Path(str(current_dir_path) + formatted_relative_path)
        return absolute_save_target_path

def shrink_target_Image_list(target_image_list):
    shrinked_target_Image_list = []
    for target_image in target_image_list:
        if target_image.is_width_more_than(WP_MAX_WIDTH):
            shrinked_target_Image_list.append(target_image.shrink_image_with_witdh(WP_MAX_WIDTH))
    return shrinked_target_Image_list

def save_image_list(image_list):
    for image in image_list:
        image.save()

def get_cache_path():
    return pathlib.Path(str(get_current_dir_path()) + CACHE_FILE_PATH)

def get_cache():
    cache_path = get_cache_path()
    cache_text_list = TextFile(cache_path).get_contents_textlist()
    return cache_text_list

def remove_cached_paths(target_content_paths,cache_text_list):
    if len(cache_text_list) == 0:
        return target_content_paths

    removed_cache_path_list = []
    for target_content_path in target_content_paths:
        str_path = str(target_content_path)
        if not str_path in cache_text_list:
            removed_cache_path_list.append(target_content_path)
    return removed_cache_path_list

def add_processing_image_path_to_cache(image_file_path_list):
    image_file_str_path_list = []
    for image_file_path in image_file_path_list:
        image_file_str_path_list.append(str(image_file_path))
    TextFile(get_cache_path()).add_texts_from_list(image_file_str_path_list)
    
current_dir : Directory = Directory(get_current_dir_path())
resized_image_dir : Directory = Directory(get_resized_image_dir_path())
current_dir_image_content_paths = \
    get_current_dir_image_content_paths(current_dir, [get_resized_image_dir_path()])

cache = get_cache()
cache_cutted_content_paths = remove_cached_paths(current_dir_image_content_paths,cache)
add_processing_image_path_to_cache(cache_cutted_content_paths)

target_image_file_list = convert_paths_to_imagefiles(cache_cutted_content_paths)

path_converted_image_list = convert_current_path_to_save_target_path(current_dir,target_image_file_list)
shrinked_image_list = shrink_target_Image_list(path_converted_image_list)
save_image_list(shrinked_image_list)

messagebox.showinfo('タスクが完了しました', str(len(shrinked_image_list)) + '件の画像を縮小しました')
