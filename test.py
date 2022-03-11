from src.ascii_image import ASCIIImage

img = ASCIIImage("chip.png", size=80)
img.toImage(bgcolor=(0, 0, 0, 0), multicolor=True)