from flask import current_app as app         #Same thing as routes

@app.errorhandler(404)          #page not found
def notFoundError(error):
    return 'That page cannot be found in our server'
@app.errorhandler(500)          #internal error
def internalServerError(error):
    return 'Internal error. Sorry!'