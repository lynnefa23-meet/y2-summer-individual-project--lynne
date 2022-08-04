from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = { 
"apiKey": "AIzaSyDRoX9raDnf9oJbthkN63aNzsTFYhfqGcY",
"authDomain": "personal-project-y2-summer.firebaseapp.com",
"projectId": "personal-project-y2-summer",
"storageBucket": "personal-project-y2-summer.appspot.com",
"messagingSenderId": "395447909481",
"appId": "1:395447909481:web:d3f2b1a4a9fc7b71a636f8",
"measurementId": "G-9NEFQCY638",
"databaseURL": "https://personal-project-y2-summer-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db= firebase.database()

songs= {
	"only_love_can_hurt_like_this": "https://www.youtube.com/watch?v=BVr3jgQMlVU",
	"glimpse_of_us": "https://www.youtube.com/watch?v=Pipna6z8eHE",
	"save_your_tears": "https://www.youtube.com/watch?v=pQ0DOToHVhs",
	"heather": "https://www.youtube.com/watch?v=GPUg7n8-M6o",
	"easy_on_me": "https://www.youtube.com/watch?v=X-yIEMduRXk",
	"take_me_to_church": "https://www.youtube.com/watch?v=1XIoqwW2yF8",
	"sway": "https://www.youtube.com/watch?v=lw8lyF2qBHM",
	"impossible": "https://www.youtube.com/watch?v=vGNQilhqbzs",
	"about_damn_time": "https://www.youtube.com/watch?v=JsOVJ1PAC6s",
	"driver_licence": "https://www.youtube.com/watch?v=_Bjf-iExroI",
	"therfore_i_am": "https://www.youtube.com/watch?v=S7D9Gs8fX54",
	"bella_ciao": "https://www.youtube.com/watch?v=0aUav1lx3rA",
	"when_the_party's_over": "https://www.youtube.com/watch?v=l9yI6z-j29w",
	"bad_guy": "https://www.youtube.com/watch?v=4-TbQnONe_w",
	"no_time_to_die": "https://www.youtube.com/watch?v=pkEa3TwTEUA",
	"as_it_was": "https://www.youtube.com/watch?v=g4FgoRLhMFU",
	"new_rules": "https://www.youtube.com/watch?v=O1TFUEMzTvE",
	"wrecking_ball":"https://www.youtube.com/watch?v=Itzk9W4YXw4",
	"senorita": "https://www.youtube.com/watch?v=FjC5XHyK7hE",
	"hello": "https://www.youtube.com/watch?v=be12BC5pQLE",
	"7_rings": "https://www.youtube.com/watch?v=LTqKlfbsLqQ"
	 }

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

# code here

@app.route('/', methods= ['POST', 'GET'])
def signup():
	error = ""
	if request.method == 'POST':
		email= request.form['email']
		password= request.form['password']
		login_session['user']= auth.create_user_with_email_and_password(email,password)
		user= {"password": request.form['password'], "email":request.form['email']}
		db.child("Users").child(login_session['user']['localId']).set(user)
		return redirect(url_for('library'))
	return render_template("signup.html")


@app.route('/remove/<string:song>')
def delete(song):
	db.child("Users").child(login_session['user']['localId']).child("songs").child(song).remove()

	return redirect(url_for('likes'))



@app.route('/login', methods= ['POST', 'GET'])
def loign():
	error=""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try: 
			login_session['user'] = auth.sign_in_with_email_and_password(email,password)
			return redirect(url_for('login'))
		except: 
			error = "Authentication failed"
	return render_template("login.html")

@app.route('/library', methods=['POST','GET'])
def library():
	# if request.method== 'POST':
	# 	try:
	# 		tweet = {"uid": login_session['user']['localId'],}
	# 		db.child("Songs").push(song)
	# 		return redirect(url_for('library'))
	# 	except:
	# 		error = "Authentication failed"

	
	return render_template("library.html", songs=songs)

@app.route('/add_likes', methods = ["POST", "GET"])
def add_likes():
	if request.method == 'POST':
		song = request.form['songs']
		try: 
			songs = {song:True}
			db.child('Users').child(login_session['user']['localId']).child('songs').update(songs)
			return redirect(url_for('likes'))
		except: 
			error = "Authentication failed"
	return render_template("library.html")

@app.route('/add_likes', methods = ["POST", "GET"])
def remove_likes():
	if request.method == 'POST':
		song = request.form['songs']
		try:
			db.child('Users').child(login_session['user']['localId']).child('songs').child(song).remove()
			return redirect(url_for('likes'))
		except: 
			error = "Authentication failed"
	return render_template("library.html")


@app.route('/likes', methods = ["POST", "GET"])
def likes():
	liked_songs = db.child('Users').child(login_session['user']['localId']).child('songs').get().val()
	return render_template("likes.html", liked_songs= liked_songs)

	


if __name__ == '__main__':
	app.run(debug=True)