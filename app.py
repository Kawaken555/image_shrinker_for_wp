
import os
import pathlib
from common.constents.filesize import WP_MAX_WIDTH
from common.constents.pathname import RESIZED_FOLDER_PATH
from common.constents.patterns import IMAGE_FILE_EXTENSION_PATTERN
from explores.Directory import Directory
from explores.files.image_file import ImageFile

def get_current_dir_path():
    return pathlib.Path(os.getcwd())
def get_resized_image_dir_path():
    return pathlib.Path(os.getcwd()+ RESIZED_FOLDER_PATH)
def get_current_dir_image_content_paths(current_dir):
    return current_dir.get_inner_file_passes(IMAGE_FILE_EXTENSION_PATTERN)

def convert_paths_to_images(image_file_paths):
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

current_dir : Directory = Directory(get_current_dir_path())
resized_image_dir : Directory = Directory(get_resized_image_dir_path())
current_dir_image_content_paths = get_current_dir_image_content_paths(current_dir)

target_image_list = convert_paths_to_images(current_dir_image_content_paths)

path_converted_image_list = convert_current_path_to_save_target_path(current_dir,target_image_list)
shrinked_image_list = shrink_target_Image_list(path_converted_image_list)
save_image_list(shrinked_image_list)

print( str(len(shrinked_image_list)) + '件の画像を縮小しました')
