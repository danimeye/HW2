## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json 

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

### Part 1 ###

@app.route('/artistform')
def artistForm():
	return render_template('artistform.html')


@app.route('/artistinfo')
def artistInfo():
	if request.method == 'GET':
		artist = request.args.get('artist')
		base_url = "https://itunes.apple.com/search"
		params_diction = {}
		params_diction["term"] = artist
		params_diction["country"] = 'US'
		resp = requests.get(base_url, params = params_diction)
		text = resp.text
		python_obj = json.loads(text)
		result_obj = python_obj["results"]
	return render_template('artist_info.html', objects = result_obj)


@app.route('/specific/song/<artist_name>')
def specific(artist_name):
	if request.method == 'GET':
		base_url = "https://itunes.apple.com/search"
		params_diction = {}
		params_diction["term"] = artist_name
		params_diction["country"] = 'US'
		resp = requests.get(base_url, params = params_diction)
		text = resp.text
		python_obj = json.loads(text)
		result_obj = python_obj["results"]

	return render_template('specific_artist.html', results = result_obj)


@app.route('/artistlinks')
def artistLinks():
	return render_template('artist_links.html')

### Part 2 ###

class AlbumEntryForm(FlaskForm):
	album_name = StringField('Enter the name of an album:', validators = [Required()])
	rating = RadioField('How much do you like this album? (1 low, 3 high)', choices = [('1', '1'), ('2', '2'), ('3', '3')], validators = [Required()])
	submit = SubmitField('Submit')

@app.route('/album_entry')
def albumEntry():
	this_form = AlbumEntryForm()
	return render_template('album_entry.html', form = this_form)

@app.route('/album_result', methods = ['GET', 'POST'])
def albumResults():
	this_form = AlbumEntryForm()
	print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	if this_form.validate_on_submit():
		print("**********************************")
		album_title = this_form.album_name.data
		user_rating = this_form.rating.data
		return render_template('album_data.html', album_name = album_title, rating = user_rating)
	flash('All fields are required!')
	return redirect(url_for('albumEntry'))

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
