# Seven color e-paper display image converter

Waveshare sells a wonderful [7.3inch ACeP 7-Color E-Paper photo frame](https://www.waveshare.com/photopainter.htm).
The [documentation](https://www.waveshare.com/wiki/PhotoPainter) includes a converter program for Mac and Windows but
there is no source available for that converter program. It's a binary file and that makes me uncomfortable to run,
so I created this python script.

This can be used as both a command line and in another Python script.

For best results:
* Before processing, I recommend cropping to a resolution that is a ratio of 480x800 or 800x480
* Images are resized using Lanczos resampling but resizing to 480x800 or 800x480 beforehand gives best results
* The dithering algorithm is Floyd–Steinberg dithering. I found Pillow to work better than GIMP here


## Quick start

Clone the project and install requirements
```bash
git clone https://gitlab.com/matthew/color-e-paper-image-converter.git
cd color-e-paper-image-converter
python3 -m pip install -r requirements.txt
```

Move your original images to the pictures folder and then execute the script
```bash
python3 ./color_epd_converter.py image.jpeg
```


## Command line

```
> ./color_epd_converter.py --help   
usage: Image converter to 7-Color e-paper BMP [options]

Converts full color images to BMP images that can be used on a 7 color e-paper display.Images are saved to ./export/

positional arguments:
  filename              If no file is specified, the converter will walk through all files in./pictures/ and
                        save those files to ./export/ (default: None)

options:
  -h, --help            show this help message and exit
  --orientation ORIENTATION, -o ORIENTATION
                        Orientation of the image. Specify either portrait or landscape. (default: portrait)
  --width WIDTH         Width of the image. (default: 480)
  --height HEIGHT       Height of the image. (default: 800)
  --crop CROP CROP CROP CROP, -c CROP CROP CROP CROP
                        Crop the image to bounds specified. Format is x1 y1 x2 y2.
                        The format is the bounding box that will be cropped with
                        x1 and y1 as the top left corner and x2 and y2 as the bottom right corner.
                        This option will not be used in batched mode (no filename specified).
```

## Python

```python
import color_epd_converter
from PIL import Image

img = Image.open("./pictures/IMG_0201.jpeg").convert("RGB")
img = color_epd_converter.convert(img,
                                  orientation="portrait",
                                  width=480,
                                  height=800,
                                  crop_image=False,
                                  crop_x1=0,
                                  crop_y1=0,
                                  crop_x2=480,
                                  crop_y2=800)
# Or just use the defaults
# img = color_epd_converter.convert(img)
img.save("./export/IMG_0201.bmp")
```
