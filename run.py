from app import createApp, db  # points to __init__.py and runs its functionalities

app = createApp()          # now we're making a variable that runs createApp

from app.blueprints.blog.models import Pokemon, User

@app.shell_context_processor
def makeContext():
    return {
        'db': db,           #Now we have access to db, user, post in the shell
        'User': User,
        'Pokemon': Pokemon
        
    }


