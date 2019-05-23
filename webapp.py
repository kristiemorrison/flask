from flask import Flask, render_template
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField

#URL Database - Starts with one record
url_database = [{"Record":{"ID":1, "URL":"https://store.google.com/?utm_source=hp_header&utm_medium=google_oo&utm_campaign=GS100042", 
                   "ShortURL":"https://soshort.com/1"}}]

#Initial URL ID
new_id = {"ID":2}

#This could be way improved... I spent too much time on getting the form working
letters = ["a", "b", "c", "d", "e"]


class InfoForm(FlaskForm):
    url = StringField('What is your long URL?')
    submit = SubmitField('GET YOUR SHORT ONE')

@app.route('/', methods=['GET', 'POST'])
def index():
    url = False
    form = InfoForm()
    if form.validate_on_submit():
        url = form.url.data
    short_url = False
    if form.url.data:
        for u in url_database:
            #Checking if long url already exists in db
            if u["Record"]["URL"] == form.url.data:
                print("URL exists in database")
                short_url = u["Record"]["ShortURL"]
                break
        if short_url == False:
            #URL doesn't exist in db - creating new record
            unique_id = new_id["ID"]
            short_url = "https://soshort.com/"+str(unique_id)#soshort.com could be shorter
            url_database.append({"Record": {"ID":unique_id, "URL":form.url.data, "ShortURL":short_url}})
            print(url_database)
            if isinstance(unique_id, int):
                unique_id += 1 
            #Again, I can do better than this
            if len(str(unique_id)) > 1 and len(letters) > 0:
                unique_id = letters[0]
                letters.pop(0)# this is not working quite right
            if isinstance(unique_id, str) and len(letters) == 0:
                unique_id = 10
            new_id["ID"] = unique_id
    form.url.data = ''
    return render_template('home.html', form=form, url=url, short_url=short_url)


if __name__ == "__main__":
    app.run(debug=True)