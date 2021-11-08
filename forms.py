from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField, MultipleFileField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField

##WTForm
class UploadForm(FlaskForm):
    img_files = MultipleFileField("Images", validators=[DataRequired()])
    wat_file = FileField("Watermarker", validators=[DataRequired()])
    height = FloatField("Height", validators=[DataRequired()])
    width = FloatField("Width", validators=[DataRequired()])
    transparency = FloatField("Transparency", validators=[DataRequired()])
    submit = SubmitField("Transform")

class ConvertImage(FlaskForm):
    img_files = MultipleFileField("Images", validators=[DataRequired()])
    img_format = SelectField("Format", validators=[DataRequired()], choices=["JPEG", "PNG", "PPM", "GIF", "TIFF", "BMP"])
    submit = SubmitField("Convert")

class ResizeImage(FlaskForm):
    img_files = MultipleFileField("Images", validators=[DataRequired()])
    img_format = SelectField("Format", validators=[DataRequired()], choices=["JPEG", "PNG", "PPM", "GIF", "TIFF", "BMP"])
    size = SelectField("Format", validators=[DataRequired()], choices=["px", "%"])
    percentage = FloatField("Percentage", validators=[])
    submit = SubmitField("Convert")
