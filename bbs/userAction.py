import time

from bbs import app, models, db
from flask import render_template, flash, redirect, session, url_for, request, g


@app.route('/register', methods=['POST'])
def register():
    user = models.User(nickname=request.form['username'], email=request.form['email'], password=request.form['password'], timestamp=time.time())
    db.session.add(user)
    db.session.commit()
    flash('注册成功~')
    return redirect(url_for('login'))


@app.route('/sign', methods=['POST'])
def sign():
    formEmail = request.form['email']
    formPwd = request.form['password']
    user = models.User.query.filter_by(email=formEmail).filter_by(password=formPwd).first()
    if user is None:
        error = '用户名或密码错误~'
        return render_template('login.html', error=error)

    flash('登录成功~')
    session['logged_in'] = True
    session['login_user_nickname'] = user.nickname
    session['login_user_id'] = user.id
    return redirect(url_for('index'))


@app.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    session['login_user_nickname'] = ''
    session['login_user_id'] = -1
    return redirect(url_for('login'))