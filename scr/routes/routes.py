from flask import Blueprint, render_template, Response, request, redirect, url_for, session, flash
from ..controller import generate
from ..models import User
from ..controller import validateRegisterForm, registerUser

# remove in deploy
from config import Config

global_scope = Blueprint("views", __name__)


@global_scope.route('/')
def home():
    return render_template('home.html')


@global_scope.route('/dataRegister', methods=['GET', 'POST'])
def dataRegister():
    if request.method == 'POST':
        # request in form
        name = request.form['names']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['emailAddress']

        # remove in deploy #####
        if Config.adminRegister == name + firstName + lastName + email:
            session['fullName'] = name + firstName + lastName
            return redirect(url_for('.video'))
        ########################

        # call the controller to validate user
        user = User(name, firstName, lastName, email)
        resultRegister = validateRegisterForm(user)
        if resultRegister is not None:
            return render_template('dataRegister.html', resultsRegister=True)
        elif resultRegister is False:
            # flash message if exist an exception in query db
            flash('Hubo Un error buscando el registro')
            return redirect(url_for('.dataRegister'))
        else:
            # register form
            validateRegister = registerUser(user)
            if validateRegister:
                session['fullName'] = name + firstName + lastName
                return redirect(url_for('.video'))
            else:
                # exception in register user
                flash('Ocurrio un error al registrar al usuario')
                return redirect(url_for('.dataRegister'))
    else:
        return render_template("dataRegister.html", resultsRegister=False)


# route of video
@global_scope.route('/video', methods=['GET'])
def video():
    return render_template('videoRegister.html', )


# route of scr images video stream
@global_scope.route('/video_feed')
def video_feed():
    return Response(generate(name=session['fullName']), mimetype="multipart/x-mixed-replace; boundary=frame")
