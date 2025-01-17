import os
import aiofiles
import aiohttp
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)


def changeImageSize(maxWidth, maxHeight, image):
    if image.size[0] == image.size[1]:
        # Does not change the scale of the orientation image and displays it centered.
        # It may look even better
        newImage = image.resize((maxHeight, maxHeight))
        img = Image.new("RGBA", (maxWidth, maxHeight))
        img.paste(newImage, (int((maxWidth - maxHeight) / 2), 0))
        return img
    else:
        widthRatio = maxWidth / image.size[0]
        heightRatio = maxHeight / image.size[1]
        newWidth = int(widthRatio * image.size[0])
        newHeight = int(heightRatio * image.size[1])
        newImage = image.resize((newWidth, newHeight))
    return newImage


async def thumb(thumbnail, title, userid, ctitle):
    img_path = f"search/thumb{userid}.png"
    if 'http' in thumbnail:
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(img_path, mode="wb")
                    await f.write(await resp.read())
                    await f.close()
    else:
        img_path = thumbnail
    image1 = Image.open(img_path)
    image2 = changeImageSize(1280, 720, image1)
    image3 = image2.convert("RGBA")
    image4 = image3.convert("RGBA")
    Image.alpha_composite(image3, image4).save(f"search/temp{userid}.png")
    img = Image.open(f"search/temp{userid}.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("driver/source/regular.ttf", 50)
    font2 = ImageFont.truetype("driver/source/medium.ttf", 72)
    img.save(f"search/final{userid}.png")
    os.remove(f"search/temp{userid}.png")
    os.remove(img_path)
    final = f"search/final{userid}.png"
    return final
