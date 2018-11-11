from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    jsonify,
    g,
)
from my_Model import DBsession, CompletedUniversity
import redis

client = redis.Redis()

main = Blueprint('spider', __name__)

@main.before_request
def _set_session():
    g.s = DBsession()


@main.teardown_request
def _close_session(e):
    g.s.commit()
    g.s.close()

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/task', methods=['POST'])
def add():
    form = request.form
    task = dict(
        university=form.get('university', ''),
        department=form.get('department', ''),
        url=form.get('url', ''),
        slowdown=form.get('slowdown', 'None')
    )
    print(task)
    client.lpush('task', task)
    return redirect(url_for('.index'))


@main.route('/manytask', methods=['POST'])
def addmanytask():
    form = request.form
    manytask = form['manytask']
    tasks = manytask.split('\n')
    try:
        for task in tasks:
            t = task.split(' ')
            t = dict(
                url=t[0],
                university=t[1],
                department=t[2].replace('\r', ''),
            )
            client.lpush('task', t)
        return redirect(url_for('.index'))
    except:
        return redirect(url_for('.index'))


@main.route('/add/stopword', methods=['POST'])
def addstopword():
    form = request.form
    word = form['word']
    with open('Data/stop_word.txt', 'a') as f:
        f.write('{}\n'.format(word))
    return redirect(url_for('.index'))


@main.route('/stopword', methods=['GET'])
def stopword():
    with open('Data/stop_word.txt', 'r') as f:
        stopwords = f.readlines()
    return render_template('stopword.html', stopwords=stopwords)


@main.route('/spided', methods=['GET'])
def spided():
    m = g.s.query(CompletedUniversity).all()
    for form in m:
        task = dict(
            university=form.university,
            department=form.department,
            url=form.url,
            slowdown='None',
        )
        client.lpush('task', task)
    d = []
    return jsonify(d)
