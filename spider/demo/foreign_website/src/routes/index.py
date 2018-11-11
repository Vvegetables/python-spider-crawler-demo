from flask import(
    Blueprint,
    session,
    request,
    url_for,
    redirect,
    render_template,
)
from my_Model import User

main = Blueprint('index', __name__)


@main.route('/login/v', methods=['POST'])
def login():
    form = request.form
    username = form.get('username', '')
    password = form.get('password', '')
    if User.verify_login(username, password):
        session['user_id'] = 1
    else:
        session['user_id'] = -1
    return redirect(url_for('data.index'))

@main.route('/login', methods=['GET'])
def index():
    return render_template('login.html')
