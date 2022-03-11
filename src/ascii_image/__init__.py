import json
from re import ASCII
from PIL import Image, ImageDraw, ImageFont
from colour import Color
import math
import os
from tqdm import tqdm

class ASCIIImage:

    def __init__(self, path, size=200, charset=None):
        """Initialize ASCII art generator

        Args:
            path (string): path to image
            size (int, optional): chracters per line. The more characters there are, the slower the speed of conversion. Defaults to 200.
            charset (string_or_list[str], optional): Charset to use for the ascii art. Defaults to None.

        Raises:
            FileNotFoundError: will be raised when the image file does not exist
        """

        self.charset = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1] if not charset else charset
        if os.path.exists(path):
            self.path = path
        else:
            raise FileNotFoundError("Could not resolve path to image file.")

        self.size = size
        self.img = Image.open(self.path)
        self.img = self.img.resize(
            (self.size, round(self.img.size[1]/self.img.size[0]*self.size)))
        self.img = self.img.convert("RGBA")
        self.pixel = self.img.load()

    def toImage(
        self,
        save_path=".",
        font_size=16,
        multicolor=False,
        bgcolor="black",
        brightness=1,
        squeeze=0):
        """Generate a jpg image of ascii art from the given image in initialization

        Args:
            save_path (str, optional): destination path to save the jpg image. Defaults to ".".

            font_size (int, optional): font size of each character in the ascii art. Defaults to 16.

            multicolor (bool, optional): set to True to apply colors into the ascii art. Defaults to False.

            bgcolor (str, optional): background color of the ascii art. Defaults to "black".

            brightness (int, optional): color brightness multiplier of each character in the ascii art. Defaults to 1.

            squeeze (int, optional): spaces to reduce between each character in the ascii art. Defaults to 0.
        """

        ascii_img = Image.new(
            'RGBA', (self.img.size[0] * (font_size - squeeze), self.img.size[1] * (font_size - squeeze)), bgcolor)
        draw = ImageDraw.Draw(ascii_img)
        print(os.getcwd())
        font = ImageFont.truetype(os.getcwd()+"/src/ascii_image/font.ttf", size=font_size)
        font.set_variation_by_name('SemiBold')

        for i in tqdm(range(self.img.size[0]), unit="lines", desc="Converting image to ASCII art"):
            for j in range(self.img.size[1]):
                color = Color(rgb=[i/255 for i in self.pixel[i, j][:3]])
                color.set_luminance(color.get_luminance(
                ) * brightness if color.get_luminance() * brightness <= 1 else 1)
                color = [round(i*255) for i in color.get_rgb()]

                if self.pixel[i, j][3] == 0:
                    char = " "
                else:
                    char = self.charset[math.floor(
                        len(self.charset) / 255 * (round(sum(color) / 3) - 1))]
                draw.text((i * (font_size - squeeze), j * (font_size - squeeze)), char, tuple(color)
                          if multicolor else (255, 255, 255), font=font, anchor="mm")

        ascii_img.save(os.path.join(save_path, self.path.split(
            "/")[-1].rsplit(".", 1)[0]+"-ASCII{}.png".format("-color" if multicolor else "-monochrome")))

    def toText(
        self,
        save_img=False,
        save_path=".",
        turn90deg=False,
        JSON=False):
        """Generate ascii art in text format

        Args:
            save_img (bool, optional): wether to save the result into a text or JSON file. Defaults to False.

            save_path (str, optional): destination path to save the result text file. Defaults to ".".

            turn90deg (bool, optional): turn the ascii art 90 degrees. Defaults to False.
            
            JSON (bool, optional): return the result in JSON format. Defaults to False.
        """
        img = []
        for i in range(self.img.size[0]):
            img.append("")
            for j in range(self.img.size[1]):
                if self.pixel[i, j][3] == 0:
                    char = " "
                else:
                    char = self.charset[math.floor(
                        len(self.charset) / 255 * (round(sum(self.pixel[i, j][:3]) / 3) - 1))]
                img[-1] += char

        if not JSON:
            result = "\n".join(img) if turn90deg else "\n".join(
                "".join(i) for i in list(zip(*img)))

            if save_img:
                open(os.path.join(save_path, self.path.split("/")
                     [-1].rsplit(".", 1)[0]+"-ASCII.txt"), "w").write(result)
            else:
                print(result)
        else:
            if not turn90deg:
                result = ["".join(i) for i in list(zip(*img))]

            if save_img:
                json.dump(result, open(os.path.join(save_path, self.path.split(
                    "/")[-1].rsplit(".", 1)[0]+"-ASCII.json"), "w"), indent=4)
            else:
                print(json.dumps(result, indent=4))