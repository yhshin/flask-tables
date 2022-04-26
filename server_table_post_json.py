import json
from pprint import pprint

from flask import Flask, render_template, request, jsonify, make_response
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
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'address': self.address,
            'phone': self.phone,
            'email': self.email
        }

db.create_all()


@app.route('/')
def index():
    return render_template('server_table_post_json.html',
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
    else:
        # loop through 'columns'
        conditions = []
        for column in data['columns']:
            # note: we used 'columns.data' to specify data source
            col_name   = column['data']
            col_search = column['search']['value']
            searchable = column['searchable']
            if searchable and col_search:  # just to make sure
                conditions.append( getattr(User, col_name).like(f'%{col_search}%'))
        query = query.filter(db.and_(*conditions))

    # TEST custom filters
    if data['unread']:
        query = query.filter(User.age < 30)
        
    #    request.form.get()
    total_filtered = query.count()

    # check 'load-unread' checkbox
    #print(request.form.keys())
    
    # sorting
    orders = []
    for order in data['order']:
        col_index = order['column']
        col_name  = data['columns'][col_index]['data']
        if col_name not in ['name', 'age', 'email']:
            col_name = 'name'
        descending = order['dir'] == 'desc'
        col = getattr(User, col_name)
        if descending:
            col = col.desc()
        orders.append(col)

    if orders:
        query = query.order_by(*orders)

    # pagination
    start  = data['start']
    length = data['length']
    query  = query.offset(start).limit(length)

    # response
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': User.query.count(),
        'draw': data['draw']
    }


@app.route('/make_older', methods=['GET', 'POST'])
def make_older():
    '''make users 1 year older

    this is to test jQurty.ajax() from 'mark as read'
    '''
    if request.method == 'POST':
        jdata = request.get_json()
        entry_ids = sorted(jdata['selected'])
        print(entry_ids)

        # Good for returning successfully updated list
        return jsonify([{'uid':uid} for uid in entry_ids])
    else:
        data = request.args.getlist('selected')
        print(data)
        return 'Feeling older', 200
          


if __name__ == '__main__':
    app.run()
