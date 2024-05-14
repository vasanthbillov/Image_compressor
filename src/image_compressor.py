# -*- coding: utf-8 -*-

from PIL import Image,ImageEnhance
import os
from enum import Enum
import tinify

class ImageType(Enum):
    JPG = 1
    PNG = 2

class ScaleType(Enum):
    EVEN_SCALE = 1  #width is enough
    ODD_SCALE = 2     #Mention hieght and width

# Public Variables /KGEAB02V01A.png
source_dir = "images/input/KGEAB02V01A.png"
destination_dir = "images/output"

image_type = ImageType.PNG  # JPG or PNG
scale_type = ScaleType.EVEN_SCALE  # PRE_DEFINED or RATIO_TO_WIDTH
width_x = 563  # 480
height_x = 317  # 360
is_multiple = False
use_tinify = False;  # It nicely reduces size for pngs
# tinify_key = ''
tinify_key = "JdvBjtKzYyxYlPSQ4kZC49My5gSYtSGf"

contrast_value = 1.2
sharpness_value = 2

def get_height(width, img):
    wpercent = (width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    return hsize

def add_sharpness(img, sharpness):
    enhancer = ImageEnhance.Sharpness(img)
    img_enhanced = enhancer.enhance(sharpness)
    return img_enhanced

def add_contrast(img, contrast_value):
    enhancer = ImageEnhance.Contrast(img)
    img_enhanced = enhancer.enhance(contrast_value)
    return img_enhanced

def resize_pics(old_pic, new_pic, width, height):
    if old_pic != source_dir + '/.DS_Store':
        if use_tinify:
            if tinify.key is not None:
                source_img = tinify.from_file(old_pic)
                if width is not None or width <= 0 :
                    resized_img = source_img.resize(
                        method="scale",
                        width=width
                    )
                resized_img.to_file(new_pic)
        else:
            img = Image.open(old_pic)
            new_height = 0
            if scale_type == ScaleType.ODD_SCALE:
                new_height = height

            if scale_type == ScaleType.EVEN_SCALE:
                new_height = get_height(width, img)
            if width is not None or width <= 0 :
                img = img.resize((width, new_height), Image.ANTIALIAS)
                img_enhanced = add_sharpness(img, sharpness_value)
                img_enhanced = add_contrast(img_enhanced, contrast_value)

            if image_type == ImageType.PNG:
                img_enhanced.save(new_pic, optimize = True)

            if image_type == ImageType.JPG:
                rgb_img = img.convert('RGB')
                img_enhanced.save(new_pic,'jpeg', optimize = True, quality = 90, subsampling = 0)

def compress_images(source_dirx, dest_dir, width, height):
    if tinify_key:
        tinify.key = tinify_key

    if os.path.isfile(source_dirx):
        path_splited = source_dirx.split(".")
        na = path_splited[0].split("/")
        file = na[len(na)-1]

        new_pic = ""
        if image_type == ImageType.JPG:
            new_pic = dest_dir + "/" + na[len(na)-1] + ".jpg"
        if image_type == ImageType.PNG:
            new_pic = dest_dir + "/" + na[len(na)-1] + ".png"
        resize_pics(source_dirx, new_pic, width, height)
    else:
        # files = os.listdir(source_dirx)
        # for file in files:
        #     name = file.split(".")
        #     old_pic = source_dirx + "/" + file
        #     new_pic = ""
        #     if image_type == ImageType.JPG:
        #         new_pic = dest_dir + "/" + name[0] + ".jpg"
        #     if image_type == ImageType.PNG:
        #         new_pic = dest_dir + "/" + name[0] + ".png"
            # print(new_pic)
            # resize_pics(old_pic, new_pic, width, height)



            # _selected_git_path = '/Users/vakumar/Documents/Zynga/Github/mobile/assets/wonka/RemoteAssets/features/LuckyCards/V1/ThemeS16/images'
            slcted = source_dirx.split('/')[-1]
            for root, dirs, files in os.walk(source_dirx, topdown = True):

                for file in files:
                    src_pic = os.path.join(root, file)
                    # print(root)
                    n_root = root.split(slcted)
                    # print(n_root)
                    
                    # print(src_pic.split(slcted))

                    paths = src_pic.split(slcted)
                    # name = paths[1].split(".")

                    # print(n_root[1] +'/'+ file)
                    new_dir = dest_dir + n_root[1] 

                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)

                    new_pic = new_dir +'/'+ file

                    print(src_pic)
                    print(new_pic)

                    resize_pics(src_pic, new_pic, width, height)



# source_dir = '/Users/vakumar/Documents/Zynga/Github/mobile/assets/wonka/RemoteAssets/features/LuckyCards/V1/ThemeS15/images/42/Card_131.png'
# source_dir = '/Users/vakumar/Documents/Zynga/Github/mobile/assets/wonka/RemoteAssets/features/LuckyCards/V1/ThemeS15/images/42/Card_1312.png'
# width_x =808
# height_x =856
# compress_images(source_dir, destination_dir, width_x, height_x)
