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
            'DT_RowId': f'row_{self.id}',
            'name': self.name,
            'age': self.age,
            'address': self.address,
            'phone': self.phone,
            'email': self.email
        }

db.create_all()


@app.route('/')
def index():
    return render_template('server_table_post.html',
                           title='Server-Driven Table')


@app.route('/api/data', methods=['POST'])
def data():
    query = User.query

    # search filter
    search = request.form.get('search[value]')
    if search:
        query = query.filter(db.or_(
            User.name.like(f'%{search}%'),
            User.email.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.form.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.form.get(f'columns[{col_index}][data]')
        if col_name not in ['name', 'age', 'email']:
            col_name = 'name'
        descending = request.form.get(f'order[{i}][dir]') == 'desc'
        col = getattr(User, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.form.get('start', type=int)
    length = request.form.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': User.query.count(),
        'draw': request.form.get('draw', type=int),
    }


if __name__ == '__main__':
    app.run()
