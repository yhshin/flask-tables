import json
from pprint import pprint, pformat

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.Integer, index=True)
    address = db.Column(db.String(256))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'address': self.address,
            'phone': self.phone,
            'email': self.email
        }

db.create_all()


@app.route('/')
def index():
    return render_template('server_table_json_post.html',
                           title='Server-Driven Table')


@app.route('/api/data', methods=['POST'])
def data():
    query = User.query

    # hmm... whole json data is a key of a
    #        'single' element ImmutableMultiDict
    #        so it's not possible to know the key
    #
    #  form = { 'data_as_a_key': '' }
    #
    data, = list(request.form.keys()) # get the key, and
    data = json.loads(data)           # convert it to dict

    # search filter
    search = data['search']['value']
    if search:
        query = query.filter(db.or_(
            User.name.like(f'%{search}%'),
            User.email.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    for item in data['order']:
        col_index = item['column']
        col_name = data['columns'][col_index]['data']
        if col_name not in ['name', 'age', 'email']:
            col_name = 'name'
        descending = item['dir'] == 'desc'
        col = getattr(User, col_name)
        if descending:
            col = col.desc()
        order.append(col)

    if order:
        query = query.order_by(*order)

    # pagination
    start  = data['start']
    length = data['length']
    query  = query.offset(start).limit(length)

    # response0
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': User.query.count(),
        'draw': data['draw']
    }

if __name__ == '__main__':
    app.run()
