from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from img_convert import ImgConvert
from forms import UploadForm, ConvertImage, ResizeImage

from io import BytesIO
import zipfile
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECRET_KEY'

## CALL IMG CONVERT
convert = ImgConvert()

@app.route("/", methods=["POST", "GET"])
def home():
    form = UploadForm()
    
    if request.method=="POST":
        ## REQUEST DATA
        img_files = form.img_files.data
        wat_file = form.wat_file.data
        height = float(form.height.data)
        width = float(form.width.data)
        transparency = form.transparency.data

        # If there is more than 1 file
        if (len(img_files)>1):
            memory_file = BytesIO()
            ##ZIP FILE
            with zipfile.ZipFile(memory_file, 'w') as zf:
                ## GET IMAGE
                for i in range(len(img_files)): 
                    #SAVE BYTEIO
                    img = convert.watermark(wat_file, [img_files[i]], (width, height), transparency)
                    byte_io = BytesIO()
                    img.save(byte_io, format="png")

                    #WRITE AND SEND DATA
                    data = zipfile.ZipInfo(img_files[i].filename.split(".")[0]+"_watermarker.png")
                    data.date_time = time.localtime(time.time())[:6]
                    data.compress_type = zipfile.ZIP_DEFLATED
                    zf.writestr(data, byte_io.getvalue())

            memory_file.seek(0)

            return send_file(memory_file, attachment_filename='images_with_watermarker.zip', as_attachment=True)
        else:
            img = convert.watermark(wat_file, [img_files[0]], (width, height), transparency)
            byte_io = BytesIO()
            img.save(byte_io, format="png")
            byte_io.seek(0)
            return send_file(byte_io, mimetype='image/jpeg', as_attachment=True, attachment_filename=f'{img_files[0].filename.split(".")[0]}_watermarker.png')

    return render_template("index.html", form=form)

#CONVERT IMG TO FORMAT
@app.route("/convert_images", methods=["GET", "POST"])
def convert_images():
    form = ConvertImage()
    if (request.method=="POST"):
        img_files = form.img_files.data
        img_format = form.img_format.data
        # If there is more than 1 file
        if (len(img_files)>1):
            memory_file = BytesIO()
            ##ZIP FILE
            with zipfile.ZipFile(memory_file, 'w') as zf:
                ## GET IMAGE
                for i in range(len(img_files)): 
                    #SAVE BYTEIO
                    img = convert.convert_image(img_files[i], img_format)
                    byte_io = BytesIO()
                    img.save(byte_io, format=img_format)

                    #WRITE AND SEND DATA
                    data = zipfile.ZipInfo(img_files[i].filename.split(".")[0]+f".{img_format.lower()}")
                    data.date_time = time.localtime(time.time())[:6]
                    data.compress_type = zipfile.ZIP_DEFLATED
                    zf.writestr(data, byte_io.getvalue())

            memory_file.seek(0)

            return send_file(memory_file, attachment_filename='images.zip', as_attachment=True)
        else:
            img = convert.convert_image(img_files[0], img_format)
            byte_io = BytesIO()
            img.save(byte_io, format=img_format)
            byte_io.seek(0)
            return send_file(byte_io, mimetype='image/jpeg', as_attachment=True, attachment_filename=img_files[0].filename.split(".")[0]+f".{img_format.lower()}")

    return render_template("convert-images.html", form=form)

#RESIZE IMAGES ENDPOINT
@app.route("/resize_images", methods=["GET", "POST"])
def resize_images():
    form = ResizeImage()

    if (request.method=="POST"):
        img_files = form.img_files.data
        img_format = form.img_format.data
        size_type = form.size.data
        img_size = float(form.percentage.data)

        # If there is more than 1 file
        if (len(img_files)>1):
            memory_file = BytesIO()
            ##ZIP FILE
            with zipfile.ZipFile(memory_file, 'w') as zf:
                ## GET IMAGE
                for i in range(len(img_files)): 
                    #SAVE BYTEIO
                    img = convert.resize_image(img_files[i], img_size, size_type)
                    byte_io = BytesIO()
                    img.save(byte_io, format=img_format)

                    #WRITE AND SEND DATA
                    data = zipfile.ZipInfo(img_files[i].filename.split(".")[0]+f".{img_format.lower()}")
                    data.date_time = time.localtime(time.time())[:6]
                    data.compress_type = zipfile.ZIP_DEFLATED
                    zf.writestr(data, byte_io.getvalue())

            memory_file.seek(0)

            return send_file(memory_file, attachment_filename='images.zip', as_attachment=True)
        
        else:
            img = convert.resize_image(img_files[0], img_size, size_type)
            byte_io = BytesIO()
            img.save(byte_io, format=img_format)
            byte_io.seek(0)
            return send_file(byte_io, mimetype='image/jpeg', as_attachment=True, attachment_filename=img_files[0].filename.split(".")[0]+f".{img_format.lower()}")
    
    return render_template("resize-images.html", form=form)

if (__name__=="__main__"):
    app.run(debug=True)