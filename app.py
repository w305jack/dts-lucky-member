from flask import Flask, render_template, request, redirect
from database import db_session, init_db
from sqlalchemy import desc

from models.member import Members
import datetime
from random import choice

app = Flask(__name__)


@app.before_first_request
def init():
    init_db()


@app.route('/')
def start():
    now = datetime.datetime.now()
    return render_template('start.html', nav='start', now=now)


@app.route('/draw')
def draw():
    members = Members.query.all()

    if not members:
        return redirect('/add-member')

    member = choice(seq=members)

    return render_template('draw.html', member=member)


@app.route('/members')
def restaurant_list():
    members = Members.query.all()

    return render_template('member.html', nav='member', members=members)


@app.route('/add-member', methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'POST':
        name = request.form.get('name')

        member = Members(name=name)
        db_session.add(member)
        db_session.commit()

        return redirect('/members')

    return render_template('add_member.html')


@app.route('/edit-member', methods=['GET', 'POST'])
def edit_restaurant():
    id = request.args.get('id')

    member = Members.query.filter(Members.id == id).first()

    if request.method == 'POST':
        name = request.form.get('name')

        member.name = name
        member.modified_time = datetime.datetime.now()

        db_session.commit()

        return redirect('/members')

    return render_template('edit_member.html', member=member)


@app.route('/delete-member')
def delete_restaurant():
    id = request.args.get('id')

    member = Members.query.filter(Members.id == id).first()

    if member:
        db_session.delete(member)
        db_session.commit()

    return redirect('/members')


def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


app.jinja_env.filters['datetime'] = datetimeformat

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(debug=True)
