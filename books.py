from flask import Flask, render_template, redirect, url_for, flash, request, session,abort
import requests
from flask_wtf import FlaskForm
from wtforms import SelectField,StringField, PasswordField, SubmitField, BooleanField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

GOOGLE_API_KEY = "AIzaSyDGkEHbMHzjlk4PsJ0ud_1S7ZfyPHI0btg"

class SearchForm(FlaskForm):
    search_term = StringField('Search Term', validators=[DataRequired()])
    submit = SubmitField('Search')

def search():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        term = search_form.search_term.data
        
        plus = "+"
        search_term=plus.join(term.split(' '))
        print(search_term)
        return redirect('/search/results/{}'.format(search_term))
    
    
    return render_template('search_page.html', title='Book Search', search_form=search_form)


def results(term,x):
    #print(x,x*10)
    req = requests.get("https://www.googleapis.com/books/v1/volumes?q={search_term}&maxResults=10&startIndex={index}&projection=lite&langRestrict=en&key={key}".format(index=x*10,search_term=term,key=GOOGLE_API_KEY))
    
    response = req.json()
    #print(response)
    comma = ","
    results = []
    for i in response["items"]:
        line = []
        line.append(i["volumeInfo"]["title"])
        try:
            line[0] = line[0] + "-" + (i["volumeInfo"]["subtitle"])
        
        except:
            pass
        try:
            line.append(comma.join(i["volumeInfo"]["authors"]))
        except:
            line.append("")
        try:
            line.append(i["volumeInfo"]["imageLinks"]["thumbnail"])
        except:
            try:
                line.append(i["volumeInfo"]["imageLinks"]["smallThumbnail"])
            except:
                line.append("")
        #print(i["id"])
        results.append(line)





    return render_template('search_results_page.html',title = "Search Results", results = results)


    




