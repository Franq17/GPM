#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Flaskr-SqlAlchemy
    ~~~~~~

    A microblog example application with Flask and SqlAlchemy.
    (Adapted from flaskr example tutorial)

    Flaskr
    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
    
    Flaskr-SqlAlchemy
    :copyright: (c) 2011 by Roberto Gea.
    :license: BSD, see LICENSE for more details.

"""
from flask import (request, session, redirect, url_for,
                   abort, render_template, flash)
from sqlalchemy import desc

import os

## app and db is defined on model.py
from model import db, app, Entry
import config


def init_db():
    if not os.path.exists(config.DATABASE):
        db.create_all()


@app.route('/')
def show_entries():
    query = Entry.query.order_by(desc(Entry.id))
    print query
    entries = [dict(title=row.title, text=row.text) for row in query.all()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    entry = Entry(request.form['title'], request.form['text'])
    db.session.add(entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


def main():
    init_db()
    app.run()


if __name__ == '__main__':
    main()
