from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
import os
import colorgram

class ImageForm(FlaskForm):
    file = FileField(label='Upload file', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = ImageForm()
    if form.validate_on_submit():
        dir = 'static/images'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f)) 
        image_path = 'static/images/input.'+form.file.data.mimetype.split('/')[1]
        with open(image_path, 'wb') as img:
            img.write(form.file.data.read())
        color_palette = find_color_palatte(image_path)
        if color_palette is not None:
            return render_template("index.html", color_palette=color_palette, image_path=image_path,  form=form)
    return render_template("index.html", form=form)

def find_color_palatte(image_path):
    colors = colorgram.extract(image_path, 10)
    return colors


if __name__ == '__main__':
    app.run(debug=True)