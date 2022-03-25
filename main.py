from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import pandas


class Form(FlaskForm):
    text = StringField(label="Text:", validators=[DataRequired()])
    code = RadioField(label='Convert to:', choices=[('Morse', 'Morse Code'), ('Nato', 'NATO')])
    submit= SubmitField(label="Translate")


class Converter():
    translated = ""
    data = pandas.read_csv("alphabet.csv")

    def convert(self, text, to_code):
        self.translated = ""
        for char in text.upper():
            if char == " ":
                self.translated += "//"
                self.translated += " "
            else:
                try:
                    self.translated += self.data.loc[self.data.Letter == char, to_code].values[0]
                    self.translated += " /"
                except IndexError:
                    self.translated += "#"
                    self.translated += " /"
        return self.translated

converter = Converter()
app = Flask(__name__)
app.secret_key = "Estamosamascuatro"
Bootstrap(app)



@app.route("/", methods=["GET", "POST"])
def home():
    form = Form()
    if form.validate_on_submit():
        text = form.text.data
        code = form.code.data
        translated_text = converter.convert(text, code)
        return render_template("index.html", text=translated_text, code=code, form=form)
    return render_template("index.html", form=form)



if __name__ == "__main__":
    app.run(debug=True)


