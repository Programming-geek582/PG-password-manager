from quart import Blueprint, Quart, render_template, request, redirect, session
from models import User
from shortuuid import ShortUUID


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
async def login():
    if request.method == "POST":
        form = await request.form
        user = await User.filter(username=form['username'], password=form['password']).first()

        if not user:
            return redirect('/register?alert=Pls register first')
        session['token'] = user.token
        print('setting session token')
        
        return redirect('/dashboard')
        
    return await render_template('login.html')

@auth.route('/register', methods=['POST', 'GET'])
async def registration():
    if request.method == "POST":
        form = await request.form
        user = await User.filter(username=form['username']).first()
        if user:
            return redirect('/register?alert=An account already exists with this username, kindly use another username')
        newuser = await User.create(username=form['username'], token=ShortUUID().random(10), password=form['password'], firstname=form['firstname'], lastname=form['lastname'])

        session['token'] = newuser.token
        return redirect('/dashboard')
    return await render_template('register.html')

@auth.route('/logout')
async def logout():
    session.clear()
    return redirect('/')

async def register(app : Quart):
    app.register_blueprint(auth)