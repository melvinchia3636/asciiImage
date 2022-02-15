import json
from re import ASCII
from PIL import Image, ImageDraw, ImageFont
from colour import Color
import math
import os
from tqdm import tqdm

class ASCIIImage:

    def __init__(self, path, size=200, charset=None):
        self.charset = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1] if not charset else charset
        if os.path.exists(path):
            self.path = path
        else:
            raise FileNotFoundError("Could not resolve path to image file.")

        self.size = size
        self.img = Image.open(self.path)
        self.img = self.img.resize((self.size, round(self.img.size[1]/self.img.size[0]*self.size)))
        self.img = self.img.convert("RGBA")
        self.pixel = self.img.load()

    def toImage(self, save_img=False, save_path=".", font_size=16, multicolor=False, bgcolor="black", brightness=1):
        ascii_img = Image.new('RGB', (self.img.size[0] * font_size, self.img.size[1] * font_size), bgcolor)
        draw = ImageDraw.Draw(ascii_img)
        font = ImageFont.truetype("font.ttf", size=font_size)
        font.set_variation_by_name('SemiBold')

        for i in tqdm(range(self.img.size[0]), unit="lines", desc="Converting image to ASCII art"):
            for j in range(self.img.size[1]):
                color = Color(rgb=[i/255 for i in self.pixel[i, j][:3]])
                color.set_luminance(color.get_luminance() * brightness if color.get_luminance() * brightness <= 1 else 1)
                color = [round(i*255) for i in color.get_rgb()]

                if self.pixel[i, j][3] == 0:
                    char = " "
                else:
                    char = self.charset[math.floor(len(self.charset) / 255 * (round(sum(color) / 3) - 1))]
                draw.text((i * font_size, j * font_size), char, tuple(color) if multicolor else (255, 255, 255), font=font, anchor="mm")

        if save_img:
            ascii_img.save(os.path.join(save_path, self.path.split("/")[-1].rsplit(".", 1)[0]+"-ASCII{}.png".format("-color" if multicolor else "-monochrome")))
        else:
            ascii_img.show()

    def toText(self, save_img=False, save_path=".", turn90deg=False, JSON=False):
        img = []
        for i in range(self.img.size[0]):
            img.append("")
            for j in range(self.img.size[1]):
                if self.pixel[i, j][3] == 0:
                    char = " "
                else:
                    char = self.charset[math.floor(len(self.charset) / 255 * (round(sum(self.pixel[i, j][:3]) / 3) - 1))]
                img[-1] += char

        if not JSON:
            result = "\n".join(img) if turn90deg else "\n".join("".join(i) for i in list(zip(*img)))

            if save_img:
                open(os.path.join(save_path, self.path.split("/")[-1].rsplit(".", 1)[0]+"-ASCII.txt"), "w").write(result)
            else:
                print(result)
        else:
            if not turn90deg:
                result = ["".join(i) for i in list(zip(*img))]
            
            if save_img:
                json.dump(result, open(os.path.join(save_path, self.path.split("/")[-1].rsplit(".", 1)[0]+"-ASCII.json"), "w"), indent=4)
            else:
                print(json.dumps(result, indent=4))

img = ASCIIImage("aww.png", size=250, charset="$")
img.toImage(save_img=True, multicolor=True)