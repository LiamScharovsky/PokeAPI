# allows to render template from template folder
from flask import render_template, current_app as app
import stripe

stripe.api_key = app.config.get('STRIPE_SK')

@app.route('/shop')
def shopPage():
    for product in stripe.Product.list()['data']:
        productDict = {
            'id':product['id'],
            'name': product['name'],
            'desc': product['description'],
            'price':stripe.Price.retrieve(product['default_price'])['unit_amount'],
            'image': product['images'][0],
        }                                       #passes html and list of products 
    return render_template ('shop/list.html', product = stripe.Product.list()['data'])

@app.route('/shop/<id>')                    #route is the product ID. Pick type of value ID is
def ShopID(id):
    return 'Shopping Item Page'
    
@app.route('/shop/cart')
def shoppingCart():
    return 'Cart Page'

@app.route('/shop/checkout')
def checkout():
    return 'checkout Page'

