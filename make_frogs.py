
from PIL import Image, ImageDraw
import os
w, h = 40,40
shape = [(0, 0), (w,h)]

def make_frogs(nr_of_frogs):
    for i in range(1,nr_of_frogs+1):
        if os.path.exists(str(i)+".png"):
            pass
        else:
            img = Image.new("RGB", (w, h))
            img1 = ImageDraw.Draw(img)
            img1.rectangle(shape, fill="red")
            img1.text((w/4,0), str(i),font_size=30,fill="blue")
            img.save(str(i)+".png")





