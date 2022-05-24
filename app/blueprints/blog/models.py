#MVC DESIGN PATTERN
import uuid  #allows to generate random IDs 
from datetime import datetime as dt
from app import db              #imports SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash #gph hashes and salts, cph reverse engeneers to check 
from flask_login import UserMixin
from app import login


followers = db.Table(
    'followers',    #name of table
    db.Column ('followerID', db.String(32), db.ForeignKey('user.id')), #name of column of followers
    db.Column ('followedID', db.String(32), db.ForeignKey('user.id'))  #name of table of whoever the follower is following
)

class Pokemon(db.Model):
    #Makes an ID with SQLALchemy Model as a string with a limit of 32 (same as default), 
    #with a default and it's the primary key
    id = db.Column(db.String(32), primary_key = True)
    #Just a string wiht no limit
    name = db.Column(db.Text)
    height = db.Column(db.Text)
    weight = db.Column(db.Text)
    type1 = db.Column(db.Text)
    type2 = db.Column(db.Text)
    #Pass reference of utcnow without () because it does it on it's own
    dateCreated = db.Column(db.DateTime, default=dt.utcnow)
    # Needs to be userID, it's a one to many (One author can have many posts)
    author = db.Column(db.ForeignKey('user.id'))

    def toDict(self):                                   #grab data 
        return {
            'id':self.id,
            'name': self.name,
            'height': self.height,
            'weight': self.weight,
            'type1': self.type1,
            'type2': self.type2,
            'dateCreated': self.dateCreated,
            'author': User.query.get(self.author)
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4().hex

    def __repr__(self):
        return f'<Pokemon: {self.body[:30]}...>'
    
class User(db.Model, UserMixin):
    id = db.Column(db.String(32), primary_key = True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    #emails need to be unique
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(300))
    #Create relationship with user and post, and cascade
    pokemons = db.relationship('Pokemon', backref='pokemonss', cascade = 'all, delete-orphan')
    dateCreated = db.Column(db.DateTime, default=dt.utcnow)
    followed = db.relationship(
        'User', #table that is relevant for the relationship
        secondary = followers, #pass reference of the followers table
        primaryjoin = (followers.c.followerID == id), #take ID of user and join it with person that is being followed
        secondaryjoin= (followers.c.followedID == id),#ID of person being followed
        backref= db.backref('followers', lazy = 'dynamic'), #allows to see users followers
        #lazy = dynamic means data being loaded is lazy loaded (only loads when needed)
        lazy='dynamic'
        )
    token = db.Column(db.String(50))
    #FOLLOWING STUFF
    def followedPokemon(self):
        followed = Pokemon.query.join(
            followers,
            (followers.c.followedID == Pokemon.author)
            ).filter(followers.c.followerID == self.id)
        own = Pokemon.query.filter_by(author=self.id)
        return followed.union(own).order_by(Pokemon.dateCreated.desc())   
            #grabs all the posts and filters it only to the ones that the current user
            #follows, then grab users posts and order them by date craeted 
        
    
    
    def follow(self, user):
        if not self.isFollowing(user):  #if you're not following the person
            self.followed.append(user)  #add to the list of followed people
    
    def unfollow(self, user):
        if self.isFollowing(user):      #if you're following the person
            self.followed.remove(user)  #remove them from your followed people
    
    def isFollowing(self, user):
        return self.followed.filter(followers.c.followedID == user.id).count() > 0 #checks if the user is already being followed
        #filter() custom made filter if the ID of the person you're checking for appears, it means you're following them

    #PASSWORD STUFF
    def generatePassword(self, password_from_form):
        self.password = generate_password_hash(password_from_form) #generates hashed password from user input
    
    def checkPassword(self, password_from_form):
        return check_password_hash(self.password, password_from_form) #unhashes and compares password with user input

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4().hex
        

    def __repr__(self):
        return f'<User:{self.email}>'

@login.user_loader
def loadUser (user_id):             #returns the user based on the user_id that was inputted
    return User.query.get(user_id)

