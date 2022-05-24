# allows to render template from template folder
from flask import render_template, current_app as app, request, redirect, url_for, flash
# from numpy import require
#current_app gives us access to what app used to be
from .models import User, Pokemon
from flask_login import login_user, logout_user, current_user
from app import db
import requests
import smtplib
from uuid import uuid4

@app.route('/users')
def usersList():
    if current_user.is_authenticated:
        #Show all users except for the one that's currently signed in
        return render_template('users/list.html', users=[user for user in User.query.all() if user != current_user])
    else:
        return redirect(url_for('login'))
# route is individual user's ID. Pick type of value ID is

@app.route('/users/unfollow/<user_ID>')
def unfollow(user_ID):  #takes the user ID from the html 
    userToUnfollow = User.query.get(user_ID) #uses it to find it in the database
    current_user.unfollow(userToUnfollow) #unfollows user with said ID
    db.session.commit() #commit it to the database
    flash (f'You unfollowed {userToUnfollow.firstName}', 'primary')
    return redirect(url_for('usersList'))


@app.route('/users/follow<user_ID>')
def follow(user_ID):
    userToFollow = User.query.get(user_ID) #uses it to find it in the database
    current_user.follow(userToFollow) #unfollows user with said ID
    db.session.commit() #commit it to the database
    flash (f'You are now following {userToFollow.firstName}', 'success')
    return redirect(url_for('usersList'))






#Hashing: Algorithm to make password more secure by changing and adding characters    
#Salting: Algorithm to add mroe random characters to your password
@app.route('/users/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        formData = request.form
        #cross reference email to see if it's in thedatabase
        #compare emails to the one email that was given by the user
        user = User.query.filter_by(email=formData.get('email')).first()

        # checks if user exists  or not user.checkPassword(formData.get('password'))and checks if password is correct                                                #if email doesn't exist
        if user is None or not user.checkPassword(formData.get('password')):
            flash('That email address or password does not exist or is incorrect', 'warning')       #flash a message
            return redirect(url_for('login'))                           #redirect to login
        
        #log user in
        login_user(user, remember = formData.get('rememberMe'))  
        
        flash ('You have logged in succesfully', 'success')
        return redirect(url_for('home'))       #redirect site to home since they logged in
    return render_template('users/login.html')


@app.route('/users/getToken')
def getToken():
    
    return render_template('users/getToken.html')                           #redirect to login
        

@app.route('/users/getToken', methods=['GET', 'POST'])
def remember():
    formData = request.form
    user = User.query.filter_by(email=formData.get('email')).first()
    if user is None:
            flash('That email address does not exist or is incorrect', 'warning')       #flash a message
            return redirect(url_for('login'))
    else:
        randToken = str(uuid4())
        formData = request.form
        user = User.query.filter_by(email = formData.get('email')).first()
        user.token = formData.get(randToken)
        db.migrate()
        db.upgrade()
        message ="Hello! Your secret token is " + randToken 
        server = smtplib.SMTP("SMPT.gmail.com", 587)        #Server and port
        server.ehlo()
        server.starttls()                                     #start the server 
        server.login("Pokedex@gmail.com", "PokePassword")   #type real in credentials 
        server.sendmail("Pokedex@gmail.com", user, message)  #from pokedex, to user, with message
        user = User.query.get(current_user.get_id())
        #update token
        
        return render_template('users/loginToken.html')

@app.route('/users/loginToken', methods = ['GET', 'POST'])
def loginToken():
    if request.method == 'POST':
        formData = request.form
        #cross reference email to see if it's in thedatabase
        #compare emails to the one email that was given by the user
        user = User.query.filter_by(email=formData.get('email')).first()
         
        #if email or token is wrong, redirect to login page
        if user is None or not user.token != (formData.get('token')):
            flash('That email address or token does not exist or is incorrect', 'warning')       #flash a message
            return redirect(url_for('login'))                           #redirect to login
        
        #log user in
        login_user(user, remember = formData.get('rememberMe'))  
        
        flash ('You have logged in succesfully', 'success')
        return redirect(url_for('home'))       #redirect site to home since they logged in
    return render_template('users/login.html')


@app.route('/users/logout')
def logout():
    logout_user()      #logs out user
    flash('You have logged out', 'primary')   #message
    return redirect(url_for('login'))  #takes user to login page

@app.route('/delete', methods =['POST'])
def deleteUser():
    if request.method == 'POST':
        id = current_user.get_id()
        deleteUser = User.query.get(id)
        db.session.delete(deleteUser)
        db.session.commit()
        flash ('User deleted', 'info')
    return redirect(url_for('login'))



@app.route('/users/register', methods= ['POST', 'GET'])
def register():
    if request.method == 'POST':
        formData = request.form
        #look for email trying to be registered
        findEmail = User.query.filter_by(email=formData.get('email')).first()
        if findEmail is not None:    #if the email alraedy exists
            flash ('That email is alraedy registered', 'warning')
            return redirect(url_for('register'))
        if formData.get('password') == formData.get('confirmPassword'):  #if the passwords match          
            user = User(    #generate a new user
            firstName = formData.get('firstName'),
            lastName = formData.get('lastName'),
            email = formData.get('email')
            )
            user.generatePassword(formData.get('password'))   #hash the password
            db.session.add(user)
            db.session.commit()      #add and commit the new user

            login_user(user, remember = True)   #log in the user
            flash('Welcome to your Pokedex!', 'success') 
            return redirect(url_for('home'))  #send them to home
        else:
            flash("Your passwords don't match", 'warning')
            return redirect(url_for('register'))

    return render_template('users/register.html')
