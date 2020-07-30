from flask import Flask, render_template, redirect, url_for, flash, request, session,abort
import requests,unicodedata
from flask_wtf import FlaskForm
from wtforms import SelectField,StringField, PasswordField, SubmitField, BooleanField,IntegerField
from wtforms.validators import DataRequired,Required, Length, Email, EqualTo

import psycopg2 as db

GOOGLE_API_KEY = "AIzaSyDGkEHbMHzjlk4PsJ0ud_1S7ZfyPHI0btg"

class SearchForm(FlaskForm):
    search_term = StringField('Search Term', validators=[DataRequired()])
    submit = SubmitField('Search')

class RatingForm(FlaskForm):
    choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]
    rating = SelectField('your rating for the book', choices = choices)
    submit = SubmitField('submit')


def search(log):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        term = search_form.search_term.data
        
        plus = "+"
        search_term=plus.join(term.split(' '))
        #print(search_term)
        return redirect('/search/results/{}'.format(search_term))
    
    
    return render_template('search_page.html', title='Book Search', search_form=search_form,login=log)

def results(term,x,log):
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
                line.append(None)
        line.append(i["id"])
        results.append(line)





    return render_template('search_results_page.html',login=log,title = "Search Results", results = results,term = term,page=x+1)

def details(id,log,url):
    rating_form = RatingForm()
    #get details from api
    
    for once in range(0,1):

        req = requests.get("https://www.googleapis.com/books/v1/volumes/{volumeId}".format(volumeId = id))

        response = req.json()

        info = {}
        vi = response["volumeInfo"]
        plus = "+"

        try:
            info["title"] = vi["title"] + "--" + vi["subtitle"]
        except:
            info["title"] = vi["title"]

        try:
            info["authors"] = plus.join(vi["authors"])
        except:
            info["authors"] = None

        try:
            info["publisher"] = vi["publisher"]
        except:
            info["publisher"] = None

        try:
            info["publishedDate"] = vi["publishedDate"]
        except:
            info["publishedDate"] = None

        try:
            new_str = unicodedata.normalize("NFKD", vi["description"])
            info["description "] = new_str
        except:
            info["description "] = None

        try:
            all_categories = vi["categories"]
        except:
            all_categories = None
        unique_categories = []
        for i in all_categories:
            sub = i.split('/')
            for k in sub:
                if k not in unique_categories:
                    unique_categories.append(k)

        info["categories"] = unique_categories

        try:
            image = vi["imageLinks"]["smallThumbnail"]
        except:
            try:
                image = vi["imageLinks"]["thumbnail"]
            except:
                try:
                    image = vi["imageLinks"]["small"]
                except:
                    try:
                        image = vi["imageLinks"]["medium"]
                    except:
                        try:
                            image = vi["imageLinks"]["large"]
                        except:
                            image = None

        info["imagelink"] = image
    old_rating = None
    if log:
        connection = db.connect(url)
        cursor = connection.cursor()

        statement = "SELECT user_id, book_id, rating	FROM reviews WHERE user_id = {} and book_id = '{}'".format(session["id"],id)
        cursor.execute(statement)
        result = cursor.fetchone()

        if (result != None):
        
            old_rating = result[2]
            #print("old",old_rating)
        
        cursor.close()
    
    #print("hop1")
    if rating_form.validate_on_submit():
        #print("hop2")
        rating =int(rating_form.rating.data)
        
        if result==None:
            new_rating(url,session["id"],rating,id)
        else:
            update_rating(url,session["id"],rating,id)

        return redirect(url_for('home_page'))
        #redirect to books of the user
        #print(rating)

    return render_template("individual_book_page.html",login=log,details = info,rating_form=rating_form,old_rating = old_rating)

def update_rating(url,user_id,rating,book_id):
    statement = "UPDATE reviews SET rating={}, date_rated={} WHERE user_id = {} and book_id='{}';".format(rating,date=str(today),user_id,book_id)
    connection = db.connect(url)
    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    cursor.close()

def new_rating(url,user_id,rating,book_id):
    statement = "INSERT INTO reviews(user_id, rating, book_id, date_rated) VALUES ({}, {},  '{}', '{}');".format(user_id,rating,book_id,date=str(today))
    connection = db.connect(url)
    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    cursor.close()



