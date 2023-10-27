import os

from PIL import Image, ImageChops, ImageOps
import numpy as np
import httpx, sys

def check_colors(img, canvas, pixelgame):
    """check template colors.
    colors -> array
    img -> PIL Object
    canvas -> str as e, 1, m, t
    pixelgame -> str """
    
    if pixelgame != "pixelcanvasio":
        if pixelgame == "pixelplanet":
            gamelink = "pixelplanet.fun"
        elif pixelgame == "canvaspixel":
            gamelink = "www.canvaspixel.net"
        elif pixelgame == "pixmap":
            gamelink = "pixmap.fun"
        else:
            gamelink = "pixelplanet.fun"
        try:
            me = httpx.get(f"https://{gamelink}/api/me").json()
        except Exception as e:
            print(f'game api error: {e}')
            return 1

        def image_to_array():
            palette = me["canvases"][str(canvas)]["colors"]
            pixels = img.load()
            width, height = img.size
            image = Image.new("RGB", (width, height))

            array = np.full((width, height), -1, dtype=np.int8)
            for x in range(width):
                for y in range(height):
                    cpixel = pixels[x, y]
                    if cpixel[3] > 0:
                        for c, color in enumerate(palette):
                            if cpixel[:3] == color[:3]:
                                array[x, y] = c
                                break

            #return array
            im = Image.fromarray(array, mode="RGB")
            image.paste(im)
            image.save('./generated/converted.png')

            black = Image.new('1', image.size, 0)
            white = Image.new('1', image.size, 1)
            mask = Image.composite(white, black, img)

            def lut(i):
                return 255 if i > 0 else 0

            with ImageChops.difference(img, image) as error_mask:
                error_mask = error_mask.point(lut).convert('L').point(lut).convert('1')
                error_mask = Image.composite(error_mask, black, mask)
        
            img.convert('LA').save("./generated/grayed.png")
            new_grayed = Image.open("./generated/grayed.png").convert("RGBA")
            
            image2 = Image.composite(Image.new('RGBA', image.size, (255, 0, 0)), new_grayed, image).save("./generated/erros_check.png")
        
        image_to_array()


def saveTemplate(name, img, coords, canvas, factionID, pixelgame):
    """Saves a template in the faction path.
    name -> str
    img -> PIL Object
    coords -> array with x & y
    canvas -> str as e, 1 or m
    factionID -> str of the faction ID
    pixelgame -> str """
    factionPath = None
    for i in os.listdir(r'./factions/'):
        if i.startswith(f'{factionID}'):
            factionPath = i
        else:
            pass
    imgPath = f'./factions/{factionPath}/_{name}_{coords[0]}_{coords[1]}_{canvas}_{pixelgame}_.png'
    if factionPath is None:
        return 0
    if not os.path.exists(imgPath):
        img.save(imgPath)
        return 2
    else:
        return 1
def saveData(factionID):
    pass
