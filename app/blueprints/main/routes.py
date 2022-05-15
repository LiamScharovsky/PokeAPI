# allows to render template from template folder
from flask import render_template, current_app as app, request, redirect, url_for, flash
#current_app gives us access to what app used to be
from datetime import datetime as dt

from regex import D                           #import to allow us to use time stamps
from app.blueprints.blog.models import Post, User  #import post from Models
from app import db, mail
from flask_login import current_user
from flask_mail import Message


@app.route('/', methods = ['GET', 'POST'])  # uses routes to the link. Make it handle GET and POST requests
def home():  # name of funtion
    if current_user.is_authenticated:

        if request.method == 'POST':
            data = request.form.get('blogPost')   #get info from input name
            
            #create new post 
            p = Post(body=data, author=current_user.get_id())
            
            db.session.add(p)       #stage p to be commited to database
            db.session.commit()     #commit p to database
            
            flash('Holy Guacamole, you made a post!', 'info') #what will be displayed, what color

            return redirect(url_for('home'))     #reroutes the page wherever you want it to go                                             # to dict method for each post in the table
        return render_template ('main/home.html', posts= [post.toDict() for post in current_user.followedPosts().all()])  
        #the query grabs the posts from the database table                              #only show the posts of people the user follows
    else:
        return redirect(url_for('login'))

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    if request.method == 'POST':
        formData = request.form
        user = User.query.get(current_user.get_id())
        #update all info
        user.firstName = formData.get('firstName')
        user.lastName = formData.get('lastName')
        user.email = formData.get('email')

        #if password and confirmPassword are the same, update the password
        if len(formData.get('password')) == 0:   #if it's 0, don't do anything
            pass
        elif formData.get('password') == formData.get('confirmPassword'):
            user.generatePassword(formData.get('password'))
        else:
            flash('Passwords are not the same', 'warning')
            return redirect(url_for('profile'))
        # what will be displayed, what color
        flash('Info updated', 'info')


        db.session.commit()
        # reroutes the page wherever you want it to go                                             # to dict method for each post in the table
        return redirect(url_for('profile'))
    return render_template('main/profile.html', posts=[post.toDict() for post in Post.query.filter_by(author=current_user.get_id()).order_by(Post.dateCreated.desc()).all()])


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        formData = request.form
        msg = Message(
            subject= 'Fakebook2 Inquiry',
            recipients= [app.config.get('MAIL_RECIPIENT')],
            sender= app.config.get('MAIL_RECIPIENT'),
            body = render_template('email/message.txt', data=formData),
            html= render_template('email/message.html', data=formData),
            reply_to = formData.get('email')
        )
        mail.send(msg)
        flash ("Hahahaha, I'm not reading that", 'success')
        return redirect(request.referrer)
    return render_template('main/contact.html')
