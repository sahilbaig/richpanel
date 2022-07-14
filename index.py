from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class users(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   email=db.Column(db.String(100))
   password=db.Column(db.String(100))

@app.route('/' , methods=["GET","POST"])
def index():

    if request.method=="POST":
        # check if user already exists
        username=request.form.get('user_name')
        password=request.form.get('user_password')
        email=request.form.get('user_email')
        if bool(users.query.filter_by(name=username).first()) or bool(users.query.filter_by(email=email).first()):
            flash("User exists")
            return redirect(('https://127.0.0.1:5000/login'))
        else:
            username=request.form.get('user_name')
            password=request.form.get('user_password')
            email=request.form.get('user_email')
            a= users(name=username,email=email, password=password)
            db.session.add(a)
            db.session.commit()
   
    return render_template('index.html')


@app.route('/login', methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get('user_name')
        password=request.form.get('user_password')
        email=request.form.get('user_email')
        if bool(users.query.filter_by(name=username).first()) and bool(users.query.filter_by(email=email).first()) and  bool(users.query.filter_by(password=password).first()): 
            return redirect(url_for(dashboard))

    return render_template("login.html")

@app.route("/dashboard" , methods=["GET","POST"])
def dashboard():
    show_pages_list=requests.get("https://graph.facebook.com/v14.0/me/accounts?type=page&access_token=EAAE6fKeHgJgBABqq1p8v8wzj9AmE0FWY4iODp3NrKj9aQjEDCQifUOstYkVcO05FvMY02dTftZABszHfZC7wFG1ceIEekdqDksFMtHPW8YcfH5iZBvjb9shObxInTZBPsBcpPHvHpzNDQwAuJVoFze9N9FzoJ3n7buBJMwaSUgZDZD").json()
    if request.method=="POST":
        submitted_value=request.form.get("submitted_value")
        # return redirect('https://stackoverflow.com/questions/25919517/python-flask-redirect-with-error')
        return redirect(f'https://127.0.0.1:5000/messages/{submitted_value}')
    
    return render_template('dashboard.html',r=show_pages_list)
    # 


@app.route("/messages/<id>")
def messages(id):

    # gets page access token 
    get_all_id=requests.get('https://graph.facebook.com/3280943425483367/accounts?fields=name,access_token&access_token=EAAE6fKeHgJgBAB0VCC6sZC6BNOb1ZBJBAQ22RQRvQjgOoQgNtLHiT94ypR9JZBglWqRAoPLzlg6bJWf09H9yyMPfacRjkq2JNh6xD1mqu2dhZA1YY9CNZC2GAVlxDkkTYZCbDVe4F1XF9E2cksHO4mf9uurhBt0ByGayfuoAuS9pYqXLtTvhOumftZCZB7uwOTZCUhBWqSZCDAPwZDZD').json()
    access_token=""
    for i in get_all_id["data"]:
        if i["id"]==id:
            access_token=(i["access_token"])
    # read convo 
    messages=requests.get(f'https://graph.facebook.com/{id}/conversations?access_token={access_token}').json()
    

    return render_template("message.html",messages=messages)


if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'))
