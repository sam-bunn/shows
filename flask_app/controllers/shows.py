from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.show import Show
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})

    if not user:
        return redirect('/user/logout')
        
    return render_template('dashboard.html', user=user, shows=Show.get_all())

@app.route('/shows/new')
def create_show():
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('show_new.html')

@app.route('/shows/new/process', methods=['POST'])
def process_show():
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Show.validate_show(request.form):
        return redirect('/shows/new')

    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'network': request.form['network'],
        'date_made': request.form['date_made'],
    }
    Show.save(data)
    return redirect('/dashboard')

@app.route('/shows/<int:id>')
def view_show(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('show_view.html',show=Show.get_by_id({'id': id}))

@app.route('/shows/edit/<int:id>')
def edit_show(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('show_edit.html',show=Show.get_by_id({'id': id}))

@app.route('/shows/edit/process/<int:id>', methods=['POST'])
def process_edit_show(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Show.validate_show(request.form):
        return redirect(f'/shows/edit/{id}')

    data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'network': request.form['network'],
        'date_made': request.form['date_made'],
    }
    Show.update(data)
    return redirect('/dashboard')

@app.route('/shows/destroy/<int:id>')
def destroy_show(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    Show.destroy({'id':id})
    return redirect('/dashboard')