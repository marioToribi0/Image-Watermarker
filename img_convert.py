from PIL import Image, ImageFilter

# url_watermark = "static/img/python.png"
# url_images = ["static\img\Proyecto Final (Algebra Lineal).png"]

class ImgConvert:
    def __init__(self) -> None:
        pass

    ##POSITIONS
    #   Direction is a tuple with percentage starting (0,0), that is, left-top.
    def position(self,direction: tuple[float], img: Image, wat: Image):
        width, height = (img.size[0]-wat.size[0], img.size[1]-wat.size[1])
        return (int(width*direction[0]/100), int(height*direction[1]/100))
    
    def watermark(self, url_watermark: str, url_images: list[str], position: tuple[float], transparency: float):
        # Transparency convert
        transparency = min(max(transparency/100*255, 0), 255)

        # Paste watermark
        with Image.open(url_watermark).convert("RGBA") as wat:
            for url_img in url_images:
                with Image.open(url_img).convert("RGBA") as img:
                    # Resize img
                    min_value = min(img.size)
                    wat_size = int(min_value*0.15)

                    wat = wat.resize((wat_size, wat_size))
                    
                    # Position watermaker
                    pos = self.position(position, img, wat)

                    # Load image and extract alpha channel
                    A = wat.getchannel('A')

                    # Make all opaque pixels into semi-opaque
                    newA = A.point(lambda i: 140 if i>0 else 0)

                    # Put new alpha channel back into original image and save
                    wat.putalpha(newA)

                    img.paste(wat, pos,mask=wat)
                    # img.save(url_img.filename.split(".")[0]+"_watermarker.png", format="png")
                    return img
    def convert_image(self, url_image, format:str):
        with Image.open(url_image) as img:
            return img

    def resize_image(self, url_image, size: float, size_type:str):
        #IF RECEIVED FLOAT NUMBERS CONVERT TO INTEGER
        if (size_type=="px"):
            with Image.open(url_image).convert("RGB") as img:
                basewidth = int(size)
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        
        #PERCENTAGE
        else:
            with Image.open(url_image).convert("RGB") as img:
                basewidth = int((float(img.size[0])*size/100))
                hsize = int((float(img.size[1])*float(size/100)))
                img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        
        return img
        
        size = tuple(map(lambda x: int(x), size))


# img = ImgConvert()
# img.watermark(url_images=url_images, url_watermark=url_watermark, position=(100,100), transparency=50)