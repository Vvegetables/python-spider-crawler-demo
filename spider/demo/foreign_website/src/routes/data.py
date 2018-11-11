from my_Model import Data, DBsession, Sql, Session, DBsession, e
from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    session,
    Response,
    make_response,
)
from flask import g
from utils.util import write_stop_word, login_required
from . import allow_cross_domain


main = Blueprint('data', __name__)

@main.before_request
def _set_session():
    g.s = DBsession()
    if request.method == 'OPTIONS':
        resp = make_response(jsonify(True))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        allow_headers = "Origin, X-Requested-With, Content-Type, Accept"
        resp.headers['Access-Control-Allow-Headers'] = allow_headers
        return resp


@main.teardown_request
def _close_session(e):
    g.s.commit()
    g.s.close()


@main.route('/', methods=['POST', 'GET'])
def index():
    return render_template('data.html')



@main.route('/api/data', methods=['POST'])
@allow_cross_domain
def api_data():
    form = request.json
    datas = g.s.query(
            Data.id,
            Data.university,
            Data.department,
            Data.teacher,
        ).filter_by(
            university=form.get('university', ''),
            department=form.get('department', ''),
        ).limit(20).offset(
            (int(form.get('page', 1)) - 1) * 20
        )
    column = ('id', 'university', 'department', 'teacher')
    _d = [dict(zip(column, i )) for i in datas]
    return jsonify(_d)


@main.route('/content/<int:id>')
def content(id):
    _id = int(id)
    content = g.s.query(Data.content).filter_by(
        id=_id,
    ).one()
    if content:
        content, = content
        return render_template('content.html', content=content)
    else:
        return redirect(url_for('.index'))


@main.route('/api/universitys', methods=['GET', 'POST'])
@allow_cross_domain
def api_universitys():
    universitys = Data.universitys()
    return jsonify(universitys)


@main.route('/api/deparments', methods=['POST'])
@allow_cross_domain
def api_department():
    form = request.json
    university = form.get('university', '北京大学')
    deparments = Data.deparments(university)
    return jsonify(deparments)


@main.route('/api/page', methods=['POST'])
@allow_cross_domain
def api_page():
    form = request.json
    university = form.get('university', '北京大学')
    department = form.get('department', '')
    if department:
        count_data = Data.count_data(
            university=university,
            department=department,
        )
        return jsonify({'countData': count_data})
    return jsonify('')


@main.route('/api/delete', methods=['GET'])
@login_required
def api_delete():
    r = request.args
    _id = r.get('id', None)
    if _id:
        d = g.s.query(Data).filter(Data.id == (int(_id))).first()
        if d:
            g.s.delete(d)
            write_stop_word(d.teacher)
    return jsonify(r.get('id', None))
