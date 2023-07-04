from quart import Blueprint, Quart, render_template, session, redirect, request
from models import User, Password, SharingConfig
from utils.encryption import decrypt

general = Blueprint('general', __name__)

@general.route('/')
async def home():
    return await render_template('index.html', session=session)
    
@general.route('/dashboard')
async def dashboard():
    if not session.get('token'):
        return redirect('/login')
    
    user = await User.filter(token=session['token']).first()
    passwords = await Password.filter(userToken=session['token']).all()
    return await render_template('dashboard.html', user=user, passwords=passwords, decrypt=decrypt)

@general.route('/dashboard/shared/view')
async def sharedPasswords():
    if not session.get('token'):
        return redirect('/login')
    
    sharedConfigs = await SharingConfig.filter(viewerToken=session['token']).all()
    user = await User.filter(token=session['token']).first()

    data_dict = {}
    user_names = []
    if not sharedConfigs:
        return await render_template('sharedpass.html', passwords=None, user=user, sharers=None)
    
    for sharedConfig in sharedConfigs:
        password = await Password.filter(userToken=sharedConfig.sharerToken).all()
        sharer = await User.filter(token=sharedConfig.sharerToken).first()
        name = f"{sharer.firstname} {sharer.lastname} ({sharer.username})"
        data_dict[name] = password
        user_names.append(name)
    return await render_template('sharedpass.html', data=data_dict, usernames=user_names, user=user, decrypt=decrypt)

@general.route('/dashboard/shared/share', methods=['POST', 'GET'])
async def share():
    if not session.get('token'):
        return redirect('/login')

    if request.method == "POST":
        form = await request.form
        user = await User.filter(username=form['username']).first()
        if not user:
            return redirect('/dashboard?alert=There is no user account with that username')
        config = await SharingConfig.filter(sharerToken=session['token'], viewerToken=user.token).first()
        if not config:
            config = await SharingConfig.create(sharerToken=session['token'], viewerToken=user.token)
        else:
            return redirect('/dashboard/shared/configure?success=Shared passwords successfully')

        return redirect('/dashboard/shared/configure?success=Shared passwords successfully')
    return await render_template('shareform.html')

@general.route('/dashboard/shared/configure')
async def shareConfig():
    if not session.get('token'):
        return redirect('/login')

    configs = await SharingConfig.filter(sharerToken=session['token']).all()
    users = []
    for i in configs:
        user = await User.filter(token=i.viewerToken).first()
        users.append(user)

    currentUser = await User.filter(token=session['token']).first()
    return await render_template('shareconfig.html', users=users, currentuser=currentUser)

@general.route('/dashboard/shared/delete')
async def shareDelete():
    if not session.get('token'):
        return redirect('/login')

    viewerToken = request.args['viewerToken']
    sharerToken = request.args['sharerToken']
    config = await SharingConfig.filter(viewerToken=viewerToken, sharerToken=sharerToken).first()
    await config.delete()
    return redirect('/dashboard/shared/configure')

@general.route('/audit')
async def audit():
    return await render_template('audit.html')

@general.route('/generate')
async def generatePass():
    return await render_template('generator.html')


async def register(app : Quart):
    app.register_blueprint(general)