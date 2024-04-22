#!/usr/bin/env python
import os
import logging
from PIL import Image
import argparse

cwd = os.path.abspath(os.path.dirname(__file__))
logger = logging.getLogger(__name__)
# Add supported image format as necessary: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
file_extensions = ['jpg', 'jpeg', 'gif', 'png', 'bmp']


def convert(image, orientation="portrait", width=480, height=800, crop_image=False, crop_x1=0, crop_y1=0, crop_x2=480,
            crop_y2=800):
    try:
        if orientation == "landscape":
            width, height = height, width
        elif orientation != "portrait":
            raise TypeError("Incorrectly specified orientation. Must be \"landscape\" or \"portrait\".")
        image_size = (width, height)

        if crop_image:
            image = image.crop([crop_x1, crop_y1, crop_x2, crop_y2])

        image = image.resize(image_size, resample=Image.Resampling.LANCZOS)

        palette = [0, 0, 0,  # black
                   255, 255, 255,  # white
                   0, 255, 0,  # green
                   0, 0, 255,  # blue
                   255, 0, 0,  # red
                   255, 255, 0,  # yellow
                   255, 128, 0]  # orange

        seven_color_palette = Image.new("P", image_size)
        seven_color_palette.putpalette(palette)
        image = image.quantize(palette=seven_color_palette, dither=Image.Dither.FLOYDSTEINBERG)
        image = image.convert(colors=24)

        return image
    except IOError as err:
        logger.exception(err)
    except KeyboardInterrupt as err:
        logger.exception(err)
        exit()
    except TypeError as err:
        logger.exception(err)
        exit()


if __name__ == '__main__':
    FORMAT = '%(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    parser = argparse.ArgumentParser(prog="Image converter to 7-Color e-paper BMP",
                                     description="Converts full color images to BMP images that can "
                                                 "be used on a 7 color e-paper display."
                                                 "Images are saved to ./export/",
                                     epilog="MIT License",
                                     usage='%(prog)s [options]',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('filename',
                        nargs='?',
                        help="If no file is specified, the converter will walk through all files in"
                             "./pictures/ and save those files to ./export/",
                        type=argparse.FileType('rb'))
    parser.add_argument('--orientation', '-o',
                        default="portrait",
                        help="Orientation of the image. Specify either portrait or landscape.")
    parser.add_argument('--width',
                        default=480,
                        type=int,
                        help="Width of the image.")
    parser.add_argument('--height',
                        default=800,
                        type=int,
                        help="Height of the image.")
    parser.add_argument('--crop', '-c',
                        nargs=4,
                        default=argparse.SUPPRESS,
                        type=int,
                        help="Crop the image to bounds specified. Format is x1 y1 x2 y2. "
                             "The format is the bounding box that will be cropped with x1 and y1 "
                             "as the top left corner and x2 and y2 as the bottom right corner. "
                             "This option will not be used in batched mode (no filename specified).")
    args = parser.parse_args()

    img_orientation = args.orientation if args.orientation else "portrait"
    img_width = args.width if args.width else 480
    img_height = args.height if args.height else 800

    if args.filename is not None:
        crop = True if args.crop else False
        x1, y1, x2, y2 = 0, 0, 0, 0
        if args.crop is not None:
            x1, y1, x2, y2 = args.crop
        file = args.filename
        ext = file.name.split(".")[-1].lower()
        try:
            if ext not in file_extensions:
                raise TypeError

            img = Image.open(file).convert("RGB")
            if crop:
                res = convert(img,
                              width=img_width,
                              height=img_height,
                              orientation=img_orientation,
                              crop_image=True,
                              crop_x1=x1,
                              crop_y1=y1,
                              crop_x2=x2,
                              crop_y2=y2)
            else:
                res = convert(img, width=img_width, height=img_height, orientation=img_orientation)
            export_path = "./export/" + os.path.basename(file.name).split(".")[0] + ".bmp"
            res.save(export_path)
            logger.info("Wrote file to {path}".format(path=export_path))
        except TypeError as e:
            logger.exception(e)
            exit()
    else:
        for (dirpath, _, files) in os.walk(cwd + '/pictures/'):
            for file in files:
                ext = file.split(".")[-1].lower()
                if file[0] == ".":
                    continue
                elif ext not in file_extensions:
                    continue
                filename = dirpath + file
                img = Image.open(filename).convert("RGB")
                res = convert(img, width=img_width, height=img_height, orientation=img_orientation)
                export_path = "./export/" + file.split(".")[0] + ".bmp"
                res.save(export_path)
                logger.info("Wrote file to {path}".format(path=export_path))
