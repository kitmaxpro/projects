from flask import Flask,render_template,request,jsonify,session, redirect, url_for
from flask_pymongo import PyMongo
import bcrypt
from flask_pymongo import pymongo
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/miskaa"
mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('items'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        #if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
        if request.form['pass'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('items'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : request.form['pass']})
            session['username'] = request.form['username']
            return redirect(url_for('items'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/additems', methods=['POST'])
def additems():
    users = mongo.db.users
    while request.method == 'POST':
        if request.form['item'] == 'book':
            sq = {'id' : '1', 'item' : 'book'}
            sqm = sq.copy()
            gif = users.find_one({'name' : session['username']})
            users.update({'_id' : gif['_id']},{"$push" : {'cart' : sqm}},upsert=False)
        elif request.form['item'] == 'smartphone':
            sq = {'id' : '2', 'item' : 'smartphone'}
            sqm = sq.copy()
            gif = users.find_one({'name' : session['username']})
            users.update({'_id' : gif['_id']},{"$push" : {'cart' : sqm}},upsert=False)
        elif request.form['item'] == 'shirt':
            sq = {'id': '3', 'item' : 'shirt'}
            sqm = sq.copy()
            gif = users.find_one({'name' : session['username']})
            users.update({'_id' : gif['_id']},{"$push" : {'cart' : sqm}},upsert=False)
        elif request.form['item'] == 'bagpack':
            sq = {'id' : '4', 'item' : 'bagpack'}
            sqm = sq.copy()
            gif = users.find_one({'name' : session['username']})
            users.update({'_id' : gif['_id']},{"$push" : {'cart' : sqm}},upsert=False)
        elif request.form['item'] == 'toaster':
            sq = {'id' : '5', 'item' : 'toaster'}
            sqm = sq.copy()
            gif = users.find_one({'name' : session['username']})
            users.update({'_id' : gif['_id']},{"$push" : {'cart' : sqm}},upsert=False) 
        return redirect(url_for('items'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        users = mongo.db.users
        users.find( { "name" : session['username']}, { "cart": {"$elemMatch":{ "": { "$eq": "2" }}} } )
        return redirect(url_for('cart'))

@app.route('/minf', methods=['POST'])
def minf():
    if request.method == 'POST':
        users = mongo.db.users
        users.delete_one( { "name" : session['username']}, { "cart": {"$elemMatch":{ "id": { "$gt": "2" }}} } )
        return redirect(url_for('cart'))

@app.route('/items')
def items():
    return render_template('items.html')
        
@app.route('/cart')
def cart():
    users = mongo.db.users
    
    return render_template('cart.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)