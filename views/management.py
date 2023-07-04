from quart import Blueprint, Quart, render_template, session, redirect, request
from models import Password, User
from utils.encryption import encrypt, decrypt

management = Blueprint('management', __name__)

@management.route('/passwords/create', methods=['POST', 'GET'])
async def create():
    if not session.get('token'):
        return redirect('/login')

    if request.method == "POST":
        form = await request.form
        password = await Password.create(userToken=session['token'], website=form['website'], username=form['username'], password=encrypt(form['password']))

        return redirect('/dashboard?success=Password created')
    return await render_template('createpass.html')

@management.route('/passwords/update/<string:website>', methods=['GET', 'POST'])
async def update(website : str):
    if not session.get('token'):
        return redirect('/login')

    if request.method == 'POST':
        form = await request.form
        new_website = form.get('website')
        username = form.get('username')
        new_password = form.get('password')

        password = await Password.filter(userToken=session['token'], website=website).first()
        print(password)
        if not password:
            return redirect('/dashboard')

        password.website = new_website
        password.username = username
        password.password = encrypt(new_password)
        await password.save()

        return redirect('/dashboard?success=Password updated')

    password = await Password.filter(userToken=session['token'], website=website).first()

    if not password:
        return redirect('/dashboard')

    return await render_template('updatepass.html', password=password, decrypt=decrypt)

@management.route('/passwords/delete', methods=['GET'])
async def delete():
    if not session.get('token'):
        return redirect('/login')

    website = request.args.get('website')

    password = await Password.filter(userToken=session['token'], website=website).first()

    if not password:
        return redirect('/dashboard')

    await password.delete()

    return redirect('/dashboard?success=Password deleted')

async def register(app : Quart):
    app.register_blueprint(management)