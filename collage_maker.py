# -*- coding: utf-8 -*-
"""
Collage maker - tool to create picture collages
Author: Delimitry
"""

import argparse
import os
import random
from PIL import Image


def make_collage(images, filename, width=2000, init_height=250, fin_width=1920, fin_height=1080):
    """
    Make a collage image with a width equal to `width` from `images` and save to `filename`.
    """
    if not images:
        print('No images for collage found!')
        return False

    margin_size = 0
    # run until a suitable arrangement of images is found
    while True:
        # copy images to images_list
        images_list = images[:]
        coefs_lines = []
        images_line = []
        x = 0
        while images_list:
            # get first image and resize to `init_height`
            img_path = images_list.pop(0)
            img = Image.open(img_path)
            img.thumbnail((width, init_height))
            # when `x` will go beyond the `width`, start the next line
            if x > width:
                coefs_lines.append((float(x) / width, images_line))
                images_line = []
                x = 0
            x += img.size[0] + margin_size
            images_line.append(img_path)
        # finally add the last line with images
        coefs_lines.append((float(x) / width, images_line))

        # compact the lines, by reducing the `init_height`, if any with one or less images
        if len(coefs_lines) <= 1:
            break
        if any(map(lambda c: len(c[1]) <= 1, coefs_lines)):
            # reduce `init_height`
            init_height -= 10
        else:
            break

    # get output height
    out_height = 0
    for coef, imgs_line in coefs_lines:
        if imgs_line:
            out_height += int(init_height / coef) + margin_size
    if not out_height:
        print('Height of collage could not be 0!')
        return False

    collage_image = Image.new('RGB', (width, int(out_height)), (35, 35, 35))
    # put images to the collage
    y = 0
    for coef, imgs_line in coefs_lines:
        if imgs_line:
            x = 0
            for img_path in imgs_line:
                img = Image.open(img_path)
                # if need to enlarge an image - use `resize`, otherwise use `thumbnail`, it's faster
                k = (init_height / coef) / img.size[1]
                if k > 1:
                    img = img.resize((int(img.size[0] * k), int(img.size[1] * k)), Image.ANTIALIAS)
                else:
                    img.thumbnail((int(width / coef), int(init_height / coef)), Image.ANTIALIAS)
                if collage_image:
                    collage_image.paste(img, (int(x), int(y)))
                x += img.size[0] + margin_size
            y += int(init_height / coef) + margin_size
    # collage_image.save(filename)
    # print(collage_image.size)
    if collage_image.size[0] > fin_width and collage_image.size[1] > fin_height:
        crop_image = collage_image.crop((0, 0, fin_width, fin_height))
    crop_image.save(filename)
    return True


def main():
    # prepare argument parser
    parse = argparse.ArgumentParser(description='Photo collage maker')
    parse.add_argument('-f', '--folder', dest='folder', help='folder with images (*.jpg, *.jpeg, *.png)', default='.')
    parse.add_argument('-F', '--file', dest='file', help='file with newline separated list of files', default='.')
    parse.add_argument('-o', '--output', dest='output',
                       help='output collage image filename', default='collage.png')
    parse.add_argument('-w', '--width', dest='width', type=int,
                       help='resulting collage image width')
    parse.add_argument('-i', '--init_height', dest='init_height',
                       type=int, help='initial height for resize the images')
    parse.add_argument('-h', '--height', dest='height',
                       type=int, help='initial height for resize the images')
    parse.add_argument('-s', '--shuffle', action='store_true', dest='shuffle', help='enable images shuffle')
    parse.add_argument('-c', '--count', dest='count', type=int, help='count of images to use', default=10)

    args = parse.parse_args()
    if not args.width or not args.init_height:
        parse.print_help()
        exit(1)

    # get images
    #files = [os.path.join(args.folder, fn) for fn in os.listdir(args.folder)]
    #images = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
    
    if args.file:
         with open(args.file, 'r') as f:
             for line in f:
                 images.append(line.strip())
    elif args.folder:
         for root, dirs, files in os.walk(args.folder):
             for name in files:
                 if re.findall("jpg|png|jpeg", name.split(".")[-1]):
                     fname = os.path.join(root, name)
                     images.append(fname)
    
    if not images:
        print('No images for making collage! Please select other directory with images!')
        exit(1)

    # shuffle images if needed
    if args.shuffle:
        random.shuffle(images)
    
    if args.count > 1:
        images = images[:args.count]
    print('Making collage...')
    res = make_collage(images, args.output, args.width,
                       args.init_height,  args.width, args.height)
    if not res:
        print('Failed to create collage!')
        exit(1)
    print('Collage is ready!')


if __name__ == '__main__':
    main()
