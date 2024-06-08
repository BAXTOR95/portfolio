import os
from flask import render_template, flash, redirect, url_for, request, jsonify, abort
from app import app, db
from forms import ContactForm, ProjectForm, LoginForm, EditProjectForm, DeleteForm
from notification_manager import NotificationManager
from datetime import date
from models import Project, ProjectImage, User
from urllib.parse import urlparse
from decorators import admin_required
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename


@app.context_processor
def inject_data():
    """Injects the year data into the context of all templates.

    Returns:
        dict: The year data.
    """
    return dict(year=date.today().year)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            notification_manager = NotificationManager()
            contact = {
                'name': form.name.data,
                'email': form.email.data,
                'subject': form.subject.data,
                'message': form.message.data,
            }
            subject = "Contact Form Submission"
            recipient_name = app.config['RECIPIENT_NAME']
            html_body = render_template(
                'email/contact_email.html',
                contact=contact,
                recipient_name=recipient_name,
            )
            notification_manager.send_email(
                subject, html_body, app.config['MY_EMAIL'], html=True
            )
            flash('Thank you, your message has been sent.', 'success')
        except Exception as e:
            flash('Your message could not be sent. Please try again.', 'danger')
            app.logger.error(f"Failed to send email: {e}")
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)


@app.route('/portfolio_details')
def portfolio_details():
    return render_template('portfolio-details.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
@admin_required
def admin():
    projects = Project.query.all()
    delete_form = DeleteForm()
    return render_template('admin.html', projects=projects, form=delete_form)


def save_images(files):
    image_urls = []
    for file in files:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        image_urls.append(file_path.replace("\\", "/"))  # Ensure consistent URL format
    return image_urls


@app.route('/add_project', methods=['GET', 'POST'])
@login_required
@admin_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            category=form.category.data,
            client=form.client.data,
            date=form.date.data,
            url=form.url.data,
            description=form.description.data,
            title=form.title.data,
        )
        db.session.add(project)
        db.session.commit()

        files = request.files.getlist("images")
        if files:
            image_urls = save_images(files)
            for url in image_urls:
                image = ProjectImage(image_url=url, project_id=project.id)
                db.session.add(image)
            db.session.commit()

        flash('Project added successfully!', 'success')
        return redirect(url_for('admin'))
    return render_template('add_project.html', form=form)


@app.route('/edit_project/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    form = EditProjectForm(obj=project)

    if form.validate_on_submit():
        project.category = form.category.data
        project.client = form.client.data
        project.date = form.date.data
        project.url = form.url.data
        project.description = form.description.data
        project.title = form.title.data
        db.session.commit()

        files = request.files.getlist("images")
        if files:
            image_urls = save_images(files)
            for url in image_urls:
                image = ProjectImage(image_url=url, project_id=project.id)
                db.session.add(image)
            db.session.commit()

        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin'))
    return render_template('edit_project.html', form=form, project=project)


@app.route('/delete_project/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    form = DeleteForm()
    if form.validate_on_submit():
        for image in project.images:
            db.session.delete(image)
            try:
                file_path = os.path.normpath(image.image_url)
                if file_path.startswith('/'):
                    file_path = file_path[1:]
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting image file: {e}")
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin'))
