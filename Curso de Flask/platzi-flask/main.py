from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap 
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
bootstrap = Bootstrap(app)

# Esto viene a querer encriptar el IP del usuario y usar "sesion()" function
# Es un diccionario que tiene llaves y valores
# En lugar de guardarlo en la cookie
app.config['SECRET_KEY'] = 'SUPER SECRETO'

todos = ['Comprar café', 'Enviar solicitud de compra', 'Entregar video a productor']

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.errorhandler(404)
def not_found(error):
    # Le pasamos en el contexto el error para poderlo desplegar
    return render_template('404.html', error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr
    
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')
    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username': username
    }
    
    # Esta ruta va a detectar cuando estás mandando un POST y va a validar la forma,
    # De esta forma GET es el template, POST redirect a inicio.html
    if login_form.validate_on_submit():
        # Si es válido obtenemos el username
        username = login_form.username.data
        # Vamos a guardar este username en la sesión
        session['username'] = username
        
        flash('Nombre de usuario registrado con éxito!')
        
        return redirect(url_for('index'))

    # Expandir variables automáticamente
    return render_template('hello.html', **context)