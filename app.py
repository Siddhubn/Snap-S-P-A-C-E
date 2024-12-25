from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
from forms import LoginForm, RegisterForm
from models import db, User, Photo

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configure uploads
UPLOAD_FOLDER = app.config['UPLOADED_PHOTOS_DEST']
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('gallery'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Save to database
            photo = Photo(filename=filename, user_id=current_user.id)
            db.session.add(photo)
            db.session.commit()
            flash('Image uploaded successfully!', 'success')
            return redirect(url_for('gallery'))
        else:
            flash('Invalid file type.', 'danger')
    return render_template('upload.html')

@app.route('/gallery')
@login_required
def gallery():
    images = Photo.query.filter_by(user_id=current_user.id).all()
    return render_template('gallery.html', images=images)

@app.route('/delete/<int:image_id>')
@login_required
def delete(image_id):
    photo = Photo.query.get_or_404(image_id)
    if photo.user_id != current_user.id:
        flash('You do not have permission to delete this image.', 'danger')
        return redirect(url_for('gallery'))

    # Delete file from filesystem
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    # Delete from database
    db.session.delete(photo)
    db.session.commit()
    flash('Image deleted successfully!', 'success')
    return redirect(url_for('gallery'))

# Helper function to validate file types
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
