from flask import Flask,render_template,request
app = Flask(__name__)

app.secret_key = 'development key'

import secrets
import requests
# import urllib
username = 'justro.hit'
password = 'qwertyuiop123'

from PIL import Image
import PIL,os


from flask_wtf import FlaskForm
from wtforms import StringField ,SubmitField
from wtforms.validators import DataRequired, ValidationError


class AddForm(FlaskForm):
    data1 = StringField('data', validators = [DataRequired()] )
    data2 = StringField('data', validators = [DataRequired()] )

    submit = SubmitField('memeify')

data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]


def make_meme_from(id,text0,text1):
    URL = 'https://api.imgflip.com/caption_image'
    params = {
        'username':username,
         'password':password,
         'template_id':id,
         'text0':text0,
         'text1':text1
         }
    response = requests.request('POST',URL,params=params).json()
    print(response)
    #
    p= response['data']['url']
    im = Image.open(requests.get(p, stream=True).raw)
    fake_name = "fbzgbkdkzgjbjg.jpg"
    # im = im.save(fake_name)
    hashed_caption = secrets.token_hex(8)
    fn = hashed_caption+secrets.token_hex(12)+'.jpg'

    picture_path = os.path.join(app.root_path , 'static' , fn)
    im.save(picture_path)
    return fn









@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/all_memes',methods=['GET',"POST"])
def memes():


    return render_template("memes.html",images = images)

@app.route('/got_meme/<id>',methods=['GET',"POST"])
def edit_meme(id):

    print(id)

    result = list(filter(lambda person: person['id'] == (id), images))
    print(result)
    form = AddForm()


    print("POS")
    if (form.validate_on_submit()):
        text0 = form.data1.data
        print(text0)

        text1 = form.data2.data
        print(text1)

        val = make_meme_from(id,text0,text1,)
        print(val)
        return render_template("submission.html",picture = val)

    return render_template("edit_meme.html",result = result,form = form)




app.run(debug=False)
