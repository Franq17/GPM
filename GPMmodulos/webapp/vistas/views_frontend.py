# -*- coding: utf-8 -*-

from uuid import uuid4

from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)
from flask_mail import Message
from flaskext.babel import gettext as _
from flask_login import login_required, login_user, current_user, logout_user, confirm_login, login_fresh

from ..modelos import User
from ..extensions import db, mail, login_manager
from .forms_frontend import SignupForm, LoginForm, RecoverPasswordForm, ReauthForm, ChangePasswordForm


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
@frontend.route('/<solicitud>')
def index(solicitud = None):
    if current_user.is_authenticated():
        return redirect(url_for('user.index', numSolicitud=solicitud))

    page = int(request.args.get('page', 1))
    pagination = User.query.paginate(page=page, per_page=10)
    #if solicitud is not None:
    #    print "SOLICITUD!!!!!"+ solicitud
    return render_template('index.html', pagination=pagination, current_user=current_user, solicitud=solicitud)
    #return render_template('index.html', pagination=pagination, current_user=current_user)


@frontend.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('user.index'))

    form = LoginForm(login=request.args.get('login', None),
                     next=request.args.get('next', None))

    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.login.data,
                                    form.password.data)

        if user and authenticated:
            remember = request.form.get('remember') == 'y'
            if login_user(user, remember=remember):
                flash(_("Sesion Iniciada"), 'success')
            return redirect(form.next.data or url_for('user.index'))
        else:
            flash(_('Lo siento, login invalido'), 'error')

    return render_template('frontend/login.html', form=form)


@frontend.route('/reauth', methods=['GET', 'POST'])
@login_required
def reauth():
    form = ReauthForm(next=request.args.get('next'))

    if request.method == 'POST':
        user, authenticated = User.authenticate(current_user.name,
                                    form.password.data)
        if user and authenticated:
            confirm_login()
            current_app.logger.debug('reauth: %s' % session['_fresh'])
            flash(_('Reatenticado.'), 'success')
            return redirect('/change_password')

        flash(_('Contrasena incorrecta.'), 'error')
    return render_template('frontend/reauth.html', form=form)


@frontend.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_('Sesion Finalizada'), 'success')
    return redirect(url_for('frontend.index'))


@frontend.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated():
        return redirect(url_for('user.index'))

    form = SignupForm(next=request.args.get('next'))

    if form.validate_on_submit():
        user = User()
        user.user_detail = UserDetail()
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        if login_user(user):
            return redirect(form.next.data or url_for('user.index'))

    return render_template('frontend/signup.html', form=form)


@frontend.route('/change_password', methods=['GET', 'POST'])
def change_password():
    user = None
    if current_user.is_authenticated():
        if not login_fresh():
            return login_manager.needs_refresh()
        user = current_user
    elif 'activation_key' in request.values and 'email' in request.values:
        activation_key = request.values['activation_key']
        email = request.values['email']
        user = User.query.filter_by(activation_key=activation_key) \
                         .filter_by(email=email).first()

    if user is None:
        abort(403)

    form = ChangePasswordForm(activation_key=user.activation_key)

    if form.validate_on_submit():
        user.password = form.password.data
        user.activation_key = None
        db.session.add(user)
        db.session.commit()

        flash(_("Su contrasena ha sido cambiada, favor vuelva a loguearse"),
              "success")
        return redirect(url_for("frontend.login"))

    return render_template("frontend/change_password.html", form=form)


@frontend.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = RecoverPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash('Please see your email for instructions on '
                  'how to access your account', 'success')

            user.activation_key = str(uuid4())
            db.session.add(user)
            db.session.commit()

            url = url_for('frontend.change_password', email=user.email, activation_key=user.activation_key, _external=True)
            html = render_template('macros/_reset_password.html', project=current_app.config['PROJECT'], username=user.name, url=url)
            message = Message(subject='Reset your password in ' + current_app.config['PROJECT'], html=html, recipients=[user.email])
            mail.send(message)

            return render_template('frontend/reset_password.html', form=form)
        else:
            flash(_('Sorry, no user found for that email address'), 'error')

    return render_template('frontend/reset_password.html', form=form)


@frontend.route('/about')
def about():
    return render_template('frontend/footers/about.html', active="about")


@frontend.route('/blog')
def blog():
    return render_template('frontend/footers/blog.html', active="blog")


@frontend.route('/help')
def help():
    return render_template('frontend/footers/help.html', active="help")


@frontend.route('/privacy')
def privacy():
    return render_template('frontend/footers/privacy.html', active="privacy")


@frontend.route('/terms')
def terms():
    return render_template('frontend/footers/terms.html', active="terms")
