from flask import render_template, abort, request
from flask import redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user
from jinja2 import TemplateNotFound

from forms import LoginForm, ToolForm
from models import User, Tool

from app import app, db, login_manager

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.route('/user/', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('list_tools'))
    return render_template('sign_in.html', form=form, no_nav=True)

@app.route('/sign-out/')
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('list_tools'))

@app.route('/', methods=['GET'])
def list_tools():
    tools = Tool.query.all()
    return render_template('tools.html',
                            tools=tools,
                            current_user=current_user)

@app.route('/tool/', methods=['GET', 'POST'])
@login_required
def new_tool():
    form = ToolForm()
    if form.validate_on_submit():
        tool = Tool()
        form.populate_obj(tool)
        db.session.add(tool)
        db.session.commit()
        return redirect(url_for('list_tools'))
    return render_template('tool.html', form=form, is_new=True)

@app.route('/tool/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_tool(id):
    tool = Tool.query.get_or_404(id)
    form = ToolForm(obj=tool)
    if form.validate_on_submit():
        form.populate_obj(tool)
        db.session.merge(tool)
        db.session.commit()
        db.session.refresh(tool)
        return redirect(url_for('list_tools'))
    return render_template('tool.html', form=form,
                           tool=tool)

@app.route('/tool/<int:id>/delete')
@login_required
def delete_tool(id):
    tool = Tool.query.get_or_404(id)
    db.session.delete(tool)
    db.session.commit()
    return redirect(url_for('list_tools'))
