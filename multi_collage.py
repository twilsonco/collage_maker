# -*- coding: utf-8 -*-
"""
Collage maker - tool to create picture collages
Author: Jitesh
"""

import os
import random
from PIL import Image
from collage_maker import make_collage


def folder_list(folder):
    files = [os.path.join(folder, fn) for fn in os.listdir(folder)]
    images = [fn for fn in files if os.path.splitext(
        fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
    return images

def main():
    
    folder1 = "/home/jitesh/3d/Data/val2017"
    folder2 = "/home/jitesh/3d/Data/Hospital"
    output = "/home/jitesh/3d/Dataset_Synthesizer/Source/Content/collaged_images"
    if not os.path.isdir(output):
        os.mkdir(output)

    final_width = 1920
    final_height = 1080
    init_width = 2000
    init_height = 250
    number_of_collaged_images = 3000
    # get images
    images = folder_list(folder1) + folder_list(folder2)
    if not images:
        print('No images for making collage! Please select other directory with images!')
        exit(1)

    # shuffle images if needed
    if 1:  # shuffle:
        random.shuffle(images)
        print((len(images)))

    print('Making collage...')
    for n in range(number_of_collaged_images):
        collaged_output = os.path.join(output,str(n+1)+".png")
        # print(collaged_output)
        sel_images = random.choices(images, k=50)
        res = make_collage(sel_images, collaged_output,
                           init_width, init_height, final_width, final_height)
        if not res:
            print('Failed to create collage!')
            exit(1)
        print(f'Collage {n+1} is ready!')


if __name__ == '__main__':
    main()
