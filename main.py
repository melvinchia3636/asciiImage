import json
from re import ASCII
from PIL import Image, ImageDraw, ImageFont
import math
import os

class ASCIIImage:
    GRADIENT = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]

    def __init__(self, path, size=200):
        if os.path.exists(path):
            self.path = path
        else:
            raise FileNotFoundError("Could not resolve path to image file.")

        self.size = size
        self.img = Image.open(self.path)
        self.img = self.img.resize((self.size, self.size))
        self.img = self.img.convert("RGBA")
        self.pixel = self.img.load()

    def toImage(self, save_img=False, save_path=".", font_size=16, monochrome=True):
        ascii_img = Image.new('RGB', (self.size * font_size, self.size * font_size), "black")
        draw = ImageDraw.Draw(ascii_img)
        font = ImageFont.truetype("sans-serif.ttf", size=font_size)

        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                if self.pixel[i, j][3] == 0:
                    char = " "
                else:
                    char = self.GRADIENT[math.floor(len(self.GRADIENT) / 255 * (round(sum(self.pixel[i, j][:3]) / 3) - 1))]
                draw.text((i * font_size, j * font_size), char, self.pixel[i, j][:3] if not monochrome else (255, 255, 255), font=font)
            print(i)

        if save_img:
            ascii_img.save(os.path.join(save_path, self.path.split("/")[-1].rsplit(".", 1)[0]+"-ASCII{}.png".format("-color" if not monochrome else "-monochrome")))
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
                    char = self.GRADIENT[math.floor(len(self.GRADIENT) / 255 * (round(sum(self.pixel[i, j][:3]) / 3) - 1))]
                img[-1] += char
            print(i)

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