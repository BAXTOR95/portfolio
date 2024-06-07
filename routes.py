from flask import render_template, flash, redirect, url_for, request, jsonify, abort
from app import app
from forms import ContactForm
from notification_manager import NotificationManager
from datetime import date


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
