from flask import Flask, render_template, request, redirect, url_for, flash,  send_file,  send_from_directory, current_app, session, make_response,  get_flashed_messages, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from models import db, User,TesdaEnrollies, Announcement,SeniorEnrollies, Certificate, UserAccount, Course,section_subject_association ,Subject, Section,Teacher,Student, Module, Comment, Enrollment, Enrollies, Grades, Schedule
from forms import LoginForm,  AnnouncementForm ,TesdaEnrolliesForm, CertificateForm, UpdateUserForm, ForgetpasswordForm, UserAccountForm, CourseForm, SubjectForm, FilterForm, SeniorEnrolliesForm, SectionForm, ChangePasswordForm
from forms import TeacherForm, StudentForm, ModuleForm, UpdateStudentForm, EnrollmentForm, EnrolliesForm, AssignTeacherToSubjectForm,  Period1Form, Period2Form, Period3Form, ScheduleForm, RegistrationForm, CommentForm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from flask_paginate import Pagination, get_page_parameter
from datetime import datetime, timedelta
import os
import requests
from flask_mail import Mail, Message
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError
from models import User
import pytz
import secrets



#'mysql+mysqlconnector://root:@localhost/apcba'
#'postgresql://apcba_raur_user:RdGTEi7roBWoYfW56OYbOHipLEFzUX4e@dpg-cnaanhgl5elc73962nlg-a.oregon-postgres.render.com/apcba_raur'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'somethingdan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://apcba_raur_user:RdGTEi7roBWoYfW56OYbOHipLEFzUX4e@dpg-cnaanhgl5elc73962nlg-a.oregon-postgres.render.com/apcba_raur'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # Use port 587 for TLS
app.config['MAIL_USERNAME'] = 'aega.salipsip.au@phinmaed.com'
app.config['MAIL_PASSWORD'] = 'pjzaibiickmobfoe'
app.config['MAIL_USE_TLS'] = True  # Use TLS
app.config['MAIL_USE_SSL'] = False  # Not using SSL

db.init_app(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

import logging
if app.debug:
    app.logger.setLevel(logging.DEBUG)
    logging.getLogger('werkzeug').setLevel(logging.DEBUG)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  
        flash('You are already logged in. Please log out to log in with a different account.', 'info')
        return redirect(url_for('dashboard'))  

    form = LoginForm()
    if request.method == 'POST':
        recaptcha_response = request.form['g-recaptcha-response']
        secret_key = '6Lf1m5opAAAAAMaNWiL23B60OadpYrBWyGC0owzd'
        payload = {'response': recaptcha_response, 'secret': secret_key}
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', payload)
        result = response.json()
        
        if not result['success']:
            flash('CAPTCHA validation failed.', 'error')
            return render_template('web/login.html', form=form)

        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user and user.password == password:  
                if 'user_id' in session:
                    # Log out the existing user before logging in with a new account
                    logged_in_user = User.query.get(session['user_id'])
                    logout_user(logged_in_user)

                login_user(user)
                session['user_id'] = user.id
                flash('Logged in successfully!', 'success')

                # Redirect to the page user was trying to access before login, if available
                next_page = session.get('next', url_for('dashboard'))
                session.pop('next', None)  # Remove the stored next page from session
                return redirect(next_page)
            else:
                flash('Invalid email or password.', 'error')
    else:
        # Store the page user was trying to access before login in the session
        session['next'] = request.args.get('next', url_for('dashboard'))

    return render_template('web/login.html', form=form)

#/////////////////////FORGOT PASSWORD ROUTE/////////////////////
def generate_verification_code():
    # Generate a random 6-digit verification code
    return str(secrets.randbelow(10**6)).zfill(6)

# Function to generate and send verification code via email
def send_verification_code(email, code):
    msg = Message('Verification Code', sender='aega.salipsip.au@phinmaed.com', recipients=[email])
    msg.body = f'Your verification code is: {code}'
    mail.send(msg)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    email_registered = True  # Assume email is registered by default

    if request.method == 'POST':
        email = request.form['email']
        # Check if the email exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            # Email exists in the database
            # Generate verification code
            verification_code = generate_verification_code()
            # Store the verification code in the session
            session['verification_code'] = verification_code
            session['email'] = email  # Store the email in session for verification
            # Send verification code via email
            send_verification_code(email, verification_code)
            return redirect(url_for('enter_code'))
        else:
            # Email is not registered, set email_registered to False
            email_registered = False

    return render_template('web/forgot_password.html', email_registered=email_registered)
#//////GENERATING CODE FUNC//////////
def generate_code():
    # Code to generate and send code via email
    pass
#//////////RESENDING CODE///////////
@app.route('/resend_code', methods=['POST'])
def resend_code():
    # Code to resend the code
    generate_code()  # Call the function to generate and send the code
    session['code_sent_time'] = datetime.now(pytz.utc)  # Update the code sent time with timezone information
    return redirect(url_for('enter_code'))

expiration_time = 5  # in minutes

@app.route('/enter_code', methods=['GET', 'POST'])
def enter_code():
    expiration_time = 5  # in minutes, adjust as needed

    if request.method == 'POST':
        # Process the form submission and verify the entered code
        entered_code = request.form['code']
        # Code to verify the entered code
        if entered_code == session.get('verification_code'):
            # Redirect user to their specific role page
            return redirect(url_for('change_password'))
        else:
            # Handle incorrect code entry
            return render_template('web/enter_code.html', error='Incorrect code')

    # Check if the code has expired
    if 'code_sent_time' in session:
        code_sent_time = session['code_sent_time']
        expiration_datetime = code_sent_time + timedelta(minutes=expiration_time)
        if datetime.now(pytz.utc) > expiration_datetime:
            # Code has expired, generate and send a new one
            generate_verification_code()
            session['code_sent_time'] = datetime.now(pytz.utc)
            # Redirect to the enter_code route to render the updated form
            return redirect(url_for('enter_code'))

    else:
        # No code has been sent yet, generate and send one  
        generate_verification_code()
        session['code_sent_time'] = datetime.now(pytz.utc)

    return render_template('web/enter_code.html')

# Route to change password
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ForgetpasswordForm()  # Assuming you have a form defined for changing password
    error_message = None  # Initialize error message variable

    if request.method == 'POST' and form.validate_on_submit():
        # Process the form submission and change the password  
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data
        if new_password != confirm_password:
            error_message = 'Passwords do not match'
        else:
            try:
                # Update password in the database
                email = session.get('email')
                if email:
                    user = User.query.filter_by(email=email).first()  
                    if user:
                        user.password = new_password
                        db.session.commit()
                        flash('Password updated successfully!', 'success')
                        return redirect(url_for('login'))  # Redirect to the login page after successful password change
                    else:
                        error_message = "User not found."
                else:
                    error_message = "Email not found in session."
            except Exception as e:
                # Handle any exceptions that occur during the commit process
                error_message = f"An error occurred while updating the password: {str(e)}"

    # If the form was not submitted or validation failed, include the form and any error message in the template
    return render_template('web/change_password.html', form=form, error=error_message)

#//////////END CODE VERIFICATION////////////////////////

#//////////DASHBOARD ROUTE////////////
@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user 
    if current_user.role == 'admin':
        # Retrieve counts from the database
        student_count = Student.query.count()
        teacher_count = Teacher.query.count()
        section_count = Section.query.count()
        user_count = User.query.count()
        course_count = Course.query.count()
        subject_count = Subject.query.count()

        # Calculate counts of active and inactive students
        active_student_count = Student.query.filter_by(active=True).count()
        inactive_student_count = student_count - active_student_count

        # Calculate counts of students enrolled in each year
        grade_11_count = Enrollment.query.filter_by(year='Grade 11').count()
        grade_12_count = Enrollment.query.filter_by(year='Grade 12').count()
        first_year_count = Enrollment.query.filter_by(year='First Year').count()
        second_year_count = Enrollment.query.filter_by(year='Second Year').count()
        third_year_count = Enrollment.query.filter_by(year='Third Year').count()
        fourth_year_count = Enrollment.query.filter_by(year='Fourth Year').count()

        # Render the admin dashboard template
        return render_template('admin/dashboard.html', student_count=student_count, teacher_count=teacher_count, 
                               section_count=section_count, user_count=user_count, 
                               active_student_count=active_student_count, inactive_student_count=inactive_student_count, 
                               course_count=course_count, subject_count=subject_count, 
                               grade_11_count=grade_11_count, grade_12_count=grade_12_count, 
                               first_year_count=first_year_count, second_year_count=second_year_count, 
                               third_year_count=third_year_count, fourth_year_count=fourth_year_count,
                               user=user)
    elif current_user.role == 'teacher':
        # Retrieve announcements for teachers
        announcements = Announcement.query.order_by(Announcement.timestamp.desc()).all()
        return render_template('teacher/teacher_announcement.html', user=user, announcements=announcements)

    elif current_user.role == 'student':
        # Retrieve announcements for students
        announcements = Announcement.query.order_by(Announcement.timestamp.desc()).all()
        return render_template('student/student_announcement.html', user=user, announcements=announcements)



#/////////////////////////////END/////////////////////////


    
@app.route('/logout')
@login_required
def logout():
    # Invalidate session
    session.clear()
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CommentForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        comment_text = form.comment.data

        new_comment = Comment(name=name, email=email, comment=comment_text)
        db.session.add(new_comment)
        db.session.commit()

        try:
            # Send email directly to your email address
            msg = Message(subject="New Comment",
                          sender=email,
                          recipients=["zdanlester@gmail.com"])  # Your email address
            msg.body = f"New comment from {name} ({email}):\n\n{comment_text}"
            mail.send(msg)
        except Exception as e:
            # Handle email sending errors
            app.logger.error(f"Error sending email: {str(e)}")
            flash('Error sending email. Please try again later.', 'error')
        else:
            flash('Comment submitted successfully!', 'success')

        return redirect(request.url)  # Redirect to the same page after form submission to prevent form resubmission

    return render_template('web/index.html', form=form)



@app.route('/web/Level')
def level():
    return render_template('web/level.html')

@app.route('/web/websiteenroll')
def websiteenroll():
    return render_template('web/websiteenroll.html')

@app.route('/student/student_dashboard')
def student_dashboard():
    return render_template('student/student_dashboard.html')

@app.route('/student/student_change_password', methods=['GET', 'POST'])
@login_required
def student_change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)

        if user.password != form.old_password.data:
            flash('Incorrect current password. Please try again.', 'danger')
            return redirect(url_for('student_change_password'))

        # Assign the new password directly (without hashing)
        user.password = form.new_password.data
        db.session.commit()

        flash('Password updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('student/student_change_password.html', form=form)

@app.route('/teacher/teacher_change_password', methods=['GET', 'POST'])
@login_required
def teacher_change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)

        if user.password != form.old_password.data:
            flash('Incorrect current password. Please try again.', 'danger')
            return redirect(url_for('teacher_change_password'))

        # Update the password directly
        user.password = form.new_password.data
        db.session.commit()

        flash('Password updated successfully!', 'success')
        return redirect(url_for('teacher_change_password'))

    return render_template('teacher/teacher_change_password.html', form=form)

@app.route('/web/senior_enrollies/add', methods=['GET', 'POST'])
def senior_enrollies():
    form = SeniorEnrolliesForm()

    if form.validate_on_submit():
        existing_application = SeniorEnrollies.query.filter_by(email=form.email.data).first()

        if existing_application:
            flash('This email is already used.', 'error')
            return render_template('web/senior_enrollies.html', form=form)

        try:
            date_of_birth = datetime.strptime(form.date_of_birth.data, "%Y-%m-%d")
            password = date_of_birth.strftime("%Y-%m-%d")

            new_senior_enrollies = SeniorEnrollies(
                first_name=form.first_name.data,
                middle_name=form.middle_name.data,
                last_name=form.last_name.data,
                suffix=form.suffix.data,
                email=form.email.data,
                address=form.address.data,
                year=form.year.data,
                lrn=form.lrn.data,
                contact_number=form.contact_number.data,
                date_of_birth=form.date_of_birth.data,
                place_of_birth=form.place_of_birth.data,
                gender=form.gender.data,
                nationality=form.nationality.data,
                religion=form.religion.data,
                previous_school_info=form.previous_school_info.data,
                grade_last_completed=form.grade_last_completed.data,
                academic_achievements=form.academic_achievements.data,
                parent_names=form.parent_names.data,
                parent_contact_info=form.parent_contact_info.data,
                parent_occupation=form.parent_occupation.data,
                special_needs=form.special_needs.data,
                track_strand=form.track_strand.data
            )

            db.session.add(new_senior_enrollies)
            db.session.commit()


            flash('Enrollment successful!', 'success')
            return redirect(url_for('senior_enrollies'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error during enrollment: {str(e)}")
            flash('Error during enrollment. Please try again later.', 'error')

    return render_template('web/senior_enrollies.html', form=form)

@app.route('/admin/view_senior_enrollies')
def view_senior_enrollies():
    enrollies_list = SeniorEnrollies.query.filter_by(is_archived=False).all()
    return render_template('admin/view_senior_enrollies.html', enrollies_list=enrollies_list)



@app.route('/web/tesda_enrollies', methods=['GET', 'POST'])
def tesda_enrollies():
    form = TesdaEnrolliesForm()

    if form.validate_on_submit():
        existing_application = TesdaEnrollies.query.filter_by(email=form.email.data).first()

        if existing_application:
            flash('This email is already used.', 'error')
            return render_template('web/tesda_enrollies.html', form=form)

        try:

            new_tesda_enrollies = TesdaEnrollies(
                first_name=form.first_name.data,
                middle_name=form.middle_name.data,
                last_name=form.last_name.data,
                suffix=form.suffix.data,
                email=form.email.data,
                track_strand=form.track_strand.data,
                year=form.year.data,
                address=form.address.data,
                contact_number=form.contact_number.data,
                date_of_birth=form.date_of_birth.data,
                place_of_birth=form.place_of_birth.data,
                gender=form.gender.data,
                nationality=form.nationality.data,
                religion=form.religion.data,
                previous_school_info=form.previous_school_info.data,
                grade_last_completed=form.grade_last_completed.data,
                academic_achievements=form.academic_achievements.data,
                parent_names=form.parent_names.data,
                parent_contact_info=form.parent_contact_info.data,
                parent_occupation=form.parent_occupation.data,
                special_needs=form.special_needs.data
                
            )

            db.session.add(new_tesda_enrollies)
            db.session.commit()


            flash('Enrollment successful!', 'success')
            return redirect(url_for('tesda_enrollies'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error during enrollment: {str(e)}")

    enrollies_list = SeniorEnrollies.query.all()
    return render_template('web/tesda_enrollies.html', form=form, enrollies_list=enrollies_list)




@app.route('/admin/view_tesda_enrollies')
def view_tesda_enrollies():
    
    enrollies_list = TesdaEnrollies.query.filter_by(is_archived=False).all()
    return render_template('admin/view_tesda_enrollies.html', enrollies_list=enrollies_list)


@app.route('/web/enrollies', methods=['GET', 'POST'])
def enrollies():
    form = EnrolliesForm()
    
    # Get courses filtered by course_type and semester
    course = request.args.get('course_title')
    courses_college_semester = Course.query.filter_by(course_type='college', semesters='1st semester').all()
    
    if form.validate_on_submit():
        existing_application = Enrollies.query.filter_by(email=form.email.data).first()
        
        if existing_application:
            flash('This email is already used.', 'error')
            return render_template('web/enrollies.html', form=form, courses_college_semester=courses_college_semester)
            
        try:
            new_enrollies = Enrollies(
                first_name=form.first_name.data,
                middle_name=form.middle_name.data,
                last_name=form.last_name.data,
                suffix=form.suffix.data,
                email=form.email.data,
                track_strand=course,  # Set track and strand to course title
                year=form.year.data,
                address=form.address.data,
                contact_number=form.contact_number.data,
                date_of_birth=form.date_of_birth.data,
                place_of_birth=form.place_of_birth.data,
                gender=form.gender.data,
                nationality=form.nationality.data,
                religion=form.religion.data,
                previous_school_info=form.previous_school_info.data,
                grade_last_completed=form.grade_last_completed.data,
                academic_achievements=form.academic_achievements.data,
                parent_names=form.parent_names.data,
                parent_contact_info=form.parent_contact_info.data,
                parent_occupation=form.parent_occupation.data,
                special_needs=form.special_needs.data
            )

            db.session.add(new_enrollies)
            db.session.commit()

            flash('Enrollment successful!', 'success')
            return redirect(url_for('enrollies'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error during enrollment: {str(e)}")

    enrollies_list = Enrollies.query.all()
    return render_template('web/enrollies.html', form=form, enrollies_list=enrollies_list, courses_college_semester=courses_college_semester)

#########
@app.route('/admin/accepeted_enrollie_SHS/<int:enrollie_id>')
@login_required
def archive_enrollie_shs(enrollie_id):
    enrollie = SeniorEnrollies.query.get(enrollie_id)
    if enrollie:
        try:
            user = User(
                first_name=enrollie.first_name,
                middle_name=enrollie.middle_name,
                last_name=enrollie.last_name,
                suffix=enrollie.suffix,
                password=enrollie.date_of_birth,
                email=enrollie.email,
                role='student'
            )
            db.session.add(user)
            db.session.commit()

            student = Student(
                student_id=user.id,
                first_name=enrollie.first_name,
                middle_name=enrollie.middle_name,
                last_name=enrollie.last_name,
                suffix=enrollie.suffix,
            )
            db.session.add(student)
            db.session.commit()

            # Create a UserAccount entry
            user_account = UserAccount(
                user_id=user.id,
                first_name=enrollie.first_name,
                middle_name=enrollie.middle_name,
                last_name=enrollie.last_name,
                suffix=enrollie.suffix,
                email=enrollie.email,
                track_strand=enrollie.track_strand,
                year=enrollie.year,
                contact_number=enrollie.contact_number,
                date_of_birth=enrollie.date_of_birth,
                place_of_birth=enrollie.place_of_birth,
                gender=enrollie.gender,
                nationality=enrollie.nationality,
                parent_names=enrollie.parent_names,
                parent_contact_info=enrollie.parent_contact_info,
                address=enrollie.address
            )
            db.session.add(user_account)
            db.session.commit()

            enrollie.is_archived = True
            db.session.commit()
            flash('Archived successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error archiving enrollie: {str(e)}")
            flash('Error archiving enrollie.', 'error')
    return redirect(url_for('view_senior_enrollies'))

@app.route('/admin/view_archived_shs')
def view_archived_shs():
    archived_shs_enrollies_list = SeniorEnrollies.query.filter_by(is_archived=True).all()
    return render_template('admin/view_archived_shs.html', archived_shs_enrollies_list=archived_shs_enrollies_list)

@app.route('/admin/accepeted_enrollie_TESDA/<int:enrollie_id>')
@login_required
def archive_enrollie_tesda(enrollie_id):
    enrollie = TesdaEnrollies.query.get(enrollie_id)
    if enrollie:
        try:
            user = User(
                first_name=enrollie.first_name,
                middle_name=enrollie.middle_name,
                last_name=enrollie.last_name,
                suffix=enrollie.suffix,
                password=enrollie.date_of_birth,
                email=enrollie.email,
                role='student'
            )
            db.session.add(user)
            db.session.commit()

            student = Student(
                student_id=user.id,
                first_name=enrollie.first_name,
                middle_name=enrollie.middle_name,
                last_name=enrollie.last_name,
                suffix=enrollie.suffix,
            )
            db.session.add(student)
            db.session.commit()

             # Create a UserAccount entry
            user_account = UserAccount(
                user_id=user.id,
                first_name=enrollie.first_name,
                middle_name=enrollie.middle_name,
                last_name=enrollie.last_name,
                suffix=enrollie.suffix,
                email=enrollie.email,
                track_strand=enrollie.track_strand,
                year=enrollie.year,
                contact_number=enrollie.contact_number,
                date_of_birth=enrollie.date_of_birth,
                place_of_birth=enrollie.place_of_birth,
                gender=enrollie.gender,
                nationality=enrollie.nationality,
                parent_names=enrollie.parent_names,
                parent_contact_info=enrollie.parent_contact_info,
                address=enrollie.address
            )
            db.session.add(user_account)
            db.session.commit()
            

            enrollie.is_archived = True
            db.session.commit()
            flash('Archived successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error archiving enrollie: {str(e)}")
            flash('Error archiving enrollie.', 'error')
    return redirect(url_for('view_tesda_enrollies'))

@app.route('/admin/view_archived_tesda')
def view_archived_tesda():
    archived_tesda_enrollies_list = TesdaEnrollies.query.filter_by(is_archived=True).all()
    return render_template('admin/view_archived_tesda.html', archived_tesda_enrollies_list=archived_tesda_enrollies_list)

#########


@app.route('/admin/accepeted_enrollie_College/<int:enrollie_id>')
@login_required
def archive_enrollie(enrollie_id):
    enrollie = Enrollies.query.get(enrollie_id)
    if enrollie:
        try:
            # Create a User entry
            user = User(
                first_name=enrollie.first_name,
                middle_name=enrollie.middle_name,
                last_name=enrollie.last_name,
                suffix=enrollie.suffix,
                password=enrollie.date_of_birth,  # You might want to hash the password
                email=enrollie.email,
                role='student'
            )
            db.session.add(user)
            db.session.commit()

            # Create a Student entry
            student = Student(
                student_id=user.id,
                first_name=enrollie.first_name,
                middle_name=enrollie.middle_name,
                last_name=enrollie.last_name,
                suffix=enrollie.suffix
            )
            db.session.add(student)
            db.session.commit()

            # Create a UserAccount entry
            user_account = UserAccount(
                user_id=user.id,
                first_name=enrollie.first_name,
                middle_name=enrollie.middle_name,
                last_name=enrollie.last_name,
                suffix=enrollie.suffix,
                email=enrollie.email,
                track_strand=enrollie.track_strand,
                year=enrollie.year,
                contact_number=enrollie.contact_number,
                date_of_birth=enrollie.date_of_birth,
                place_of_birth=enrollie.place_of_birth,
                gender=enrollie.gender,
                nationality=enrollie.nationality,
                parent_names=enrollie.parent_names,
                parent_contact_info=enrollie.parent_contact_info,
                address=enrollie.address
            )
            db.session.add(user_account)
            db.session.commit()

            # Mark the enrollie as archived
            enrollie.is_archived = True
            db.session.commit()
            
            flash('Archived successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error archiving enrollie: {str(e)}")
            flash('Error archiving enrollie.', 'error')
    return redirect(url_for('view_enrollies'))



@app.route('/admin/enrollies')
def view_enrollies():
    
    enrollies_list = Enrollies.query.filter_by(is_archived=False).all()
    return render_template('admin/view_enrollies.html', enrollies_list=enrollies_list)

@app.route('/admin/view_archived_enrollies')
def view_archived_enrollies():
    archived_enrollies_list = Enrollies.query.filter_by(is_archived=True).all()
    return render_template('admin/view_archived_enrollies.html', archived_enrollies_list=archived_enrollies_list)



@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
def users():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('admin/dashboard'))

    users_data = User.query.all()
    number_of_accounts = User.query.count()
    search_query = request.args.get('q', default='', type=str)

    if search_query:
        users_data = User.query.filter(
            or_(
                User.email.ilike(f"%{search_query}%"),
                User.name.ilike(f"%{search_query}%"),
            )
        ).all()

    
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 8  
    offset = (page - 1) * per_page
    pagination_users = users_data[offset: offset + per_page]

    pagination = Pagination(page=page, per_page=per_page, total=len(users_data), css_framework='bootstrap4')

    teacher_form = TeacherForm()
    student_form = StudentForm()

    if request.method == 'POST':
        if teacher_form.validate_on_submit() and current_user.role == 'admin':
            new_teacher = Teacher(
                teacher_id=teacher_form.teacher_id.data,
                name=teacher_form.name.data,
            )
            db.session.add(new_teacher)
            try:
                db.session.commit()
                flash('Teacher added successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding teacher: {str(e)}', 'danger')

        elif student_form.validate_on_submit() and current_user.role == 'admin':
            new_student = Student(
                student_id=student_form.student_id.data,
                name=student_form.name.data,
            
            )
            db.session.add(new_student)
            try:
                db.session.commit()
                flash('Student added successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding student: {str(e)}', 'danger')

        return redirect(url_for('users'))

    return render_template('admin/users.html', users=pagination_users, search_query=search_query, teacher_form=teacher_form, student_form=student_form,  number_of_accounts=number_of_accounts, pagination=pagination)


@app.route('/admin/teachers')
@login_required
def view_teachers():
    
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    teachers_data = Teacher.query.all()

    return render_template('admin/view_teachers.html', teachers=teachers_data)



@app.route('/students', methods=['GET'])
@login_required
def view_students():
    if current_user.role not in ['admin', 'teacher']:
        flash('You are not authorized to view students.', 'danger')
        return redirect(url_for('dashboard'))

    if current_user.role == 'teacher':
        teacher = Teacher.query.filter_by(teacher_id=current_user.id).first()
        if teacher:
            section = teacher.section  
            if section:
                enrollments = section.enrollments
                return render_template('teacher/view_class.html', authenticated=True, enrollments=enrollments)
            else:
                flash('You are not assigned to any section.', 'warning')
                return redirect(url_for('dashboard'))
        else:
            flash('You are not assigned to any sections.', 'warning')
            return redirect(url_for('dashboard'))

    elif current_user.role == 'admin':
        students = Student.query.all()
        return render_template('admin/view_students.html', authenticated=True, students=students)
    
@app.route('/student/<int:student_id>/toggle_active', methods=['POST'])
def toggle_active_student(student_id):
    student = Student.query.get_or_404(student_id)
    # Toggle the active status
    student.active = not student.active
    db.session.commit()
    flash(f'Student {student.first_name} {student.last_name} is now {"active" if student.active else "inactive"}', 'success')
    return redirect(url_for('view_students', student_id=student_id))
    
@app.route('/student_subjects/<int:student_id>', methods=['GET'])
@login_required
def student_subjects(student_id):
    enrolled_subjects = {}

    # Fetch enrolled subjects for the specified student
    existing_enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    for enrollment in existing_enrollments:
        section_id = enrollment.section_id
        enrolled_subjects[student_id] = Subject.query.filter_by(section_id=section_id).all()

    return render_template('teacher/student_subjects.html', enrolled_subjects=enrolled_subjects.get(student_id, []))



@app.route('/admin/students/update/<int:student_id>', methods=['GET', 'POST'])
@login_required
def update_student(student_id):
    if current_user.role != 'admin':
        return redirect(url_for('view_students'))

    student_to_update = Student.query.get(student_id)
    if not student_to_update:
        return redirect(url_for('view_students'))

    form = UpdateStudentForm(obj=student_to_update)


    if form.validate_on_submit():
        if form.updated_name.data:
            student_to_update.name = form.updated_name.data
        

        db.session.commit()
        return redirect(url_for('view_students'))

    return render_template('admin/update_student.html', form=form, student=student_to_update)

@app.route('/admin/students/delete/<int:student_id>', methods=['GET', 'POST'])
@login_required
def delete_student(student_id):
    if current_user.role != 'admin':
        return redirect(url_for('view_students'))

    student_to_delete = Student.query.get(student_id)
    if not student_to_delete:
        return redirect(url_for('view_students'))

    db.session.delete(student_to_delete)
    db.session.commit()
    flash('Student deleted successfully.', 'success')

    return redirect(url_for('view_students'))



@app.route('/announcement', methods=['GET', 'POST'])
@login_required
def announcement():
    form = AnnouncementForm()

    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data, content=form.content.data, author_id=current_user.id)
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement has been posted successfully', 'success')
    announcements = Announcement.query.order_by(Announcement.timestamp.desc()).all()

    if current_user.is_authenticated:
        if current_user.role == 'student':
            template = 'student/student_announcement.html'
        elif current_user.role == 'teacher':
            template = 'teacher/teacher_announcement.html'
        elif current_user.role == 'admin':
            template = 'admin/announcement.html'
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

    return render_template(template, user=current_user, form=form, announcements=announcements)

@app.route('/admin/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('dashboard'))

    form = RegistrationForm()


    if form.validate_on_submit():
        hashed_password = form.password.data  # In a real application, you should hash the password

        # Create a new user with the provided information
        user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            middle_name=form.middle_name.data,
            last_name=form.last_name.data,
            suffix=form.suffix.data,
            password=hashed_password,
            role=form.role.data,
        )
        db.session.add(user)
        db.session.commit()

        # Assign the current user as a teacher
        teacher = Teacher(
            teacher_id=user.id,
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
            suffix=user.suffix
        )
        db.session.add(teacher)
        db.session.commit()

        flash('Registered successfully!', 'success')
        return redirect(url_for('register'))

    return render_template('admin/register.html', form=form)


@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    # Check if the current user is an admin
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('dashboard'))

    user_to_update = User.query.get(user_id)

    # Check if the user to update exists
    if not user_to_update:
        flash('User not found.', 'danger')
        return redirect(url_for('dashboard'))

    # Check if the user being updated is an admin
    if user_to_update.role == 'admin':
        flash('Admin user cannot be updated.', 'danger')
        return redirect(url_for('users'))

    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.new_first_name.data:
            user_to_update.first_name = form.new_first_name.data
        if form.new_middle_name.data:
            user_to_update.middle_name = form.new_middle_name.data
        if form.new_last_name.data:
            user_to_update.last_name = form.new_last_name.data
        if form.new_suffix.data:
            user_to_update.suffix = form.new_suffix.data
        if form.new_email.data:
            user_to_update.email = form.new_email.data
        if form.new_password.data:
            user_to_update.password = form.new_password.data  


        db.session.commit()
        flash(f'User updated successfully!', 'success')
        return redirect(url_for('users'))

    return render_template('admin/update_user.html', form=form, user=user_to_update)



@app.route('/admin/update_announcement/<int:announcement_id>', methods=['GET', 'POST'])
@login_required
def update_announcement(announcement_id):
    announcement = Announcement.query.get(announcement_id)

    if not announcement or current_user.id != announcement.author_id:
        return redirect(url_for('dashboard'))

    form = AnnouncementForm(obj=announcement)

    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.content = form.content.data
        db.session.commit()
        flash('Annoucnement has been updated successfully', 'success')  # Moved flash above return
        return redirect(url_for('dashboard'))

    return render_template('admin/update_announcement.html', form=form, announcement=announcement)

@app.route('/admin/delete_announcement/<int:announcement_id>')
@login_required
def delete_announcement(announcement_id):
    announcement = Announcement.query.get(announcement_id)

    if not announcement or current_user.id != announcement.author_id:
        return redirect(url_for('dashboard'))

    db.session.delete(announcement)
    db.session.commit()
    flash('Announcement has been deleted successfully', 'success')
    return redirect(url_for('dashboard'))




@app.route('/certificate', methods=['GET', 'POST'])
@login_required
def certificate():
    form = CertificateForm()

    if form.validate_on_submit():
        title = form.title.data
        pdf = form.pdf.data
        pdf_filename = f"{title.replace(' ', '_')}.pdf"
        os.makedirs(os.path.join('uploads', 'documents'), exist_ok=True)
        pdf.save(os.path.join('uploads', 'documents', pdf_filename))
        certificate = Certificate(title=title, pdf=pdf_filename, user_id=current_user.id)
        db.session.add(certificate)
        db.session.commit()
        flash('Uploaded successfully!', 'success')
        return redirect(url_for('certificate'))
        
    if current_user.role == 'student':
        title_filter = request.args.get('title', default='', type=str)
        # Filter certificates based on the current user's ID
        certificates = Certificate.query.order_by(Certificate.id.desc()).all()
        template = 'student/student_certificate.html'
    elif current_user.role == 'teacher':
        title_filter = request.args.get('title', default='', type=str)
        certificates = Certificate.query.order_by(Certificate.id.desc()).all()
        template = 'teacher/teacher_certificate.html'
    elif current_user.role == 'admin':
        title_filter = request.args.get('title', default='', type=str)
        certificates = Certificate.query.order_by(Certificate.id.desc()).all()
        template = 'admin/certificate.html'
    else:
        return redirect(url_for('dashboard'))

    return render_template(template, user=current_user, form=form, certificates=certificates)

@app.route('/admin/update_certificate/<int:certificate_id>', methods=['GET', 'POST'])
@login_required
def update_certificate(certificate_id):
    certificate = Certificate.query.get(certificate_id)

    if not certificate or current_user.id != certificate.user_id:
        return redirect(url_for('dashboard'))

    form = CertificateForm(obj=certificate)

    if form.validate_on_submit():
        certificate.title = form.title.data

        if 'pdf' in request.files:
            pdf = request.files['pdf']
            pdf_filename = f"{form.title.data.replace(' ', '_')}.pdf"
            pdf.save(os.path.join('uploads', 'documents', pdf_filename))
            certificate.pdf = pdf_filename

        db.session.commit()
        flash('Updated successfully!', 'success')
        return redirect(url_for('certificate'))
    

    return render_template('admin/update_certificate.html', form=form, certificate=certificate)

@app.route('/admin/delete_certificate/<int:certificate_id>')
@login_required
def delete_certificate(certificate_id):
    certificate = Certificate.query.get(certificate_id)

    if not certificate or current_user.id != certificate.user_id:
        return redirect(url_for('certificate'))

    db.session.delete(certificate)
    db.session.commit()
    flash('Deleted successfully!', 'success')
    return redirect(url_for('certificate'))

@app.route('/admin/download_certificate/<int:certificate_id>')
@login_required
def download_certificate(certificate_id):
    certificate = Certificate.query.get(certificate_id)

    if not certificate or current_user.id != certificate.user_id:
        return redirect(url_for('certificate'))

    certificate_path = os.path.join('uploads', 'documents', certificate.pdf)
    flash('Message has been deleted successfully!', 'success')
    return send_file(certificate_path, as_attachment=True)



@app.route('/student_account', methods=['GET', 'POST'])
def student_account():
    form = UserAccountForm()  # Initialize the form

    # Retrieve the current user's user_id (You need to implement this part)
    user_id = current_user.id  # Assuming you are using Flask-Login

    # Retrieve the existing user account information if available
    user_account = UserAccount.query.filter_by(user_id=user_id).first()

    if user_account:
        # Pre-fill the form fields with the existing user account data
       
        form.lrn.data = user_account.lrn
        form.name.data = user_account.name
        form.email.data = user_account.email
        form.track_strand.data = user_account.track_strand
        form.address.data = user_account.address
        form.year.data = user_account.year
        form.contact_number.data = user_account.contact_number
        form.date_of_birth.data = user_account.date_of_birth
        form.place_of_birth.data = user_account.place_of_birth
        form.gender.data = user_account.gender
        form.nationality.data = user_account.nationality
        form.parent_names.data = user_account.parent_names
        form.parent_contact_info.data = user_account.parent_contact_info

    if form.validate_on_submit():
        # Process the form data
 
        lrn = form.lrn.data
        name = form.name.data
        email = form.email.data
        track_strand = form.track_strand.data
        address = form.address.data
        year = form.year.data
        contact_number = form.contact_number.data
        date_of_birth = form.date_of_birth.data
        place_of_birth = form.place_of_birth.data
        gender = form.gender.data
        nationality = form.nationality.data
        parent_names = form.parent_names.data
        parent_contact_info = form.parent_contact_info.data

        # Check if the user_id already exists
        user_account = UserAccount.query.filter_by(user_id=user_id).first()

        if user_account:
            # If user_id exists, update the existing UserAccount entry
            user_account.lrn = lrn
            user_account.name = name
            user_account.email = email
            user_account.track_strand = track_strand
            user_account.address = address
            user_account.year = year
            user_account.contact_number = contact_number
            user_account.date_of_birth = date_of_birth
            user_account.place_of_birth = place_of_birth
            user_account.gender = gender
            user_account.nationality = nationality
            user_account.parent_names = parent_names
            user_account.parent_contact_info = parent_contact_info
            flash('UserAccount updated successfully!', 'success')
        else:
            # If user_id doesn't exist, create a new UserAccount entry
            user_account = UserAccount(

                lrn=lrn,
                name=name,
                email=email,
                track_strand=track_strand,
                address=address,
                year=year,
                contact_number=contact_number,
                date_of_birth=date_of_birth,
                place_of_birth=place_of_birth,
                gender=gender,
                nationality=nationality,
                parent_names=parent_names,
                parent_contact_info=parent_contact_info
            )
            flash('UserAccount created successfully!', 'success')

        db.session.add(user_account)
        db.session.commit()

        return redirect(url_for('student_account'))

    return render_template('student/student_account.html', form=form, user_account=user_account)



@app.route('/teacher/account', methods=['GET', 'POST'])
@login_required
def teacher_account():
    form = UserAccountForm(obj=current_user.user_account)

    if form.validate_on_submit():
        if not current_user.user_account:
            user_account_instance = UserAccount()
            form.populate_obj(user_account_instance)
            user_account_instance.user = current_user
            db.session.add(user_account_instance)
        else:
            form.populate_obj(current_user.user_account)

        db.session.commit()
        return redirect(url_for('teacher_account'))

    return render_template('teacher/teacher_account.html', form=form)
#######################################################################################################################################################################################
@app.route('/courses', methods=['GET', 'POST'])
@login_required
def course():
    form_course = CourseForm()

    if form_course.validate_on_submit():
        new_course = Course(
            course_type=form_course.course_type.data,
            abbreviation=form_course.abbreviation.data,
            title=form_course.title.data,
            year=form_course.year.data,
            Class=form_course.Class.data,
            semesters=form_course.semesters.data,
            is_active=form_course.is_active.data
        )
        db.session.add(new_course)
        db.session.commit()
        flash('Course created successfully!', 'success')
        return redirect(url_for('course'))

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 8
    offset = (page - 1) * per_page

    # Assuming Course is your SQLAlchemy model
    total_courses = Course.query.count()
    courses = Course.query.offset(offset).limit(per_page).all()

    pagination = Pagination(page=page, per_page=per_page, total=total_courses, css_framework='bootstrap4')

    return render_template('admin/course.html', courses=courses, form_course=form_course, pagination=pagination)


@app.route('/update_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)

    if form.validate_on_submit():
        course.course_type = form.course_type.data
        course.abbreviation = form.abbreviation.data
        course.title = form.title.data
        course.year = form.year.data
        course.Class = form.Class.data
        course.semesters = form.semesters.data
        course.is_active = form.is_active.data

        db.session.commit()
        flash('Updated successfully!', 'success')
        return redirect(url_for('course'))

    return render_template('admin/update_course.html', form=form, course=course)

##########################################################################################################################################################################################
@app.route('/manage_section', methods=['GET', 'POST'])
def manage_section():
    # Assuming you're using Flask-Login for user authentication
    form_section = SectionForm()
    form_subject = SubjectForm()  # Creating an instance of the SubjectForm

    course_id_filter = request.args.get('course_id', type=int)
    section_name_filter = request.args.get('section_name', type=str)
    sections_query = Section.query

    if course_id_filter:
        sections_query = sections_query.filter_by(course_id=course_id_filter)
    if section_name_filter:
        sections_query = sections_query.filter(Section.name.ilike(f'%{section_name_filter}%'))

    sections = sections_query.all()
    courses = Course.query.all()
    serialized_courses = [{'id': course.id, 'title': course.title, 'semesters': course.semesters} for course in courses]
    form_section.course_id.choices = [(course.id, course.title) for course in courses]
    teachers = Teacher.query.all()
    form_section.set_teacher_choices(teachers)

    if form_section.validate_on_submit():
        selected_teacher_id = form_section.teacher_id.data

        new_section = Section(
            name=form_section.name.data,
            capacity=form_section.capacity.data,
            school_year=form_section.school_year.data,
            year=form_section.year.data,
            course_id=form_section.course_id.data,
            teacher_id=selected_teacher_id
        )

        # Fetch all subjects related to the chosen course
        selected_course = Course.query.get(form_section.course_id.data)
        subjects = selected_course.subjects

        # Associate all fetched subjects with the new section
        new_section.subjects.extend(subjects)

        db.session.add(new_section)
        db.session.commit()
        flash('Section created successfully!', 'success')

        # Redirect to the same page to clear the form fields
        return redirect(url_for('manage_section'))

    return render_template('admin/manage_section.html', sections=sections, courses=serialized_courses,
                           form_section=form_section, form_subject=form_subject)

@app.route('/archive_section/<int:section_id>', methods=['POST'])
def archive_section(section_id):
    section = Section.query.get_or_404(section_id)

    # Archive the section
    section.is_archived = True
    db.session.commit()
    flash('Section archived successfully!', 'success')

    # Redirect back to the manage section page or wherever appropriate
    return redirect(url_for('manage_section'))



@app.route('/subjects/add', methods=['POST'])
@login_required
def add_subject():
    form_subject = SubjectForm()
    
    if form_subject.validate_on_submit():
        new_subject = Subject(
            abbreviation=form_subject.abbreviation.data,
            title=form_subject.title.data,
            unit=form_subject.unit.data,
            section_id=form_subject.section_id.data
        )
        db.session.add(new_subject)
        db.session.commit()
        flash('Subject added successfully!', 'success')
    else:
        flash('Failed to add subject. Please check the form inputs.', 'danger')
    
    return redirect(url_for('manage_section'))


@app.route('/assign_teacher_to_subject/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def assign_teacher_to_subject(subject_id):
    # Fetch subject from the database
    subject = Subject.query.get_or_404(subject_id)
    
    # Create form instance
    form = AssignTeacherToSubjectForm()

    # Fetch teachers from the database
    teachers = Teacher.query.all()

    # Set choices for teacher_id field in the form
    form.set_teacher_choices(teachers)

    # Validate form submission
    if form.validate_on_submit():
        selected_teacher_id = form.teacher_id.data
        teacher = Teacher.query.get(selected_teacher_id)
        
        if teacher:
            # Check if the teacher is already associated with the subject
            if teacher not in subject.teachers:
                subject.teachers.append(teacher)
                db.session.commit()
                flash('Teacher assigned to subject successfully!', 'success')
            else: 
                flash('Teacher is already assigned to this subject!', 'warning')
        else:
            flash('Teacher not found!', 'error')

        # Redirect to the view_subjects route with both section_id and course_id parameters
        return redirect(url_for('view_subjects', section_id=subject.sections[0].id, course_id=subject.course_id))


    # Render the template with the form
    return render_template('admin/assign_teacher_to_subject.html', form=form, subject=subject, teachers=teachers)


@app.route('/admin/subject_bank', methods=['GET', 'POST'])
@login_required
def subject_bank():
    if request.method == 'POST':
        # Get form data
        course_id = request.form.get('course_id')
        abbreviation = request.form.get('abbreviation')
        title = request.form.get('title')
        unit = request.form.get('unit')
        
        # Create a new subject
        subject = Subject(abbreviation=abbreviation, title=title, unit=unit, course_id=course_id)
        
        # Add the subject to the database
        db.session.add(subject)
        db.session.commit()
        
        flash('Subject added successfully', 'success')
        return redirect(url_for('subject_bank'))

    # Fetch all courses from the database
    courses = Course.query.all()
    
    # Fetch subjects for each course
    course_subjects = {}
    for course in courses:
        course_subjects[course.id] = course.subjects
    
    return render_template('admin/subject_bank.html', courses=courses, course_subjects=course_subjects)

@app.route('/admin/subject_bank/edit/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def edit_subject(subject_id):
    if request.method == 'GET':
        try:
            # Fetch subject data from the database
            subject = Subject.query.get_or_404(subject_id)
            subject_data = {
                'id': subject.id,
                'abbreviation': subject.abbreviation,
                'title': subject.title,
                'unit': subject.unit
            }
            return jsonify(subject_data), 200
        except SQLAlchemyError as e:
            return jsonify({'error': str(e)}), 500
    elif request.method == 'POST':
        try:
            # Fetch subject data from the database
            subject = Subject.query.get_or_404(subject_id)

            # Get JSON data from the request body
            data = request.json
            abbreviation = data.get('abbreviation')
            title = data.get('title')
            unit = data.get('unit')

            # Check if abbreviation is not null
            if not abbreviation:
                return jsonify({'error': 'Abbreviation cannot be empty'}), 400
            
            # Update subject attributes
            subject.abbreviation = abbreviation
            subject.title = title
            subject.unit = unit
            
            # Commit changes to the database
            db.session.commit()
            
            flash('Subject updated successfully', 'success')
            return jsonify({'message': 'Subject updated successfully'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500



@app.route('/admin/subject_bank/delete/<int:subject_id>', methods=['POST'])
@login_required
def delete_subject(subject_id):
    # Find the subject in the database by its ID
    subject = Subject.query.get_or_404(subject_id)

    try:
        # Delete related schedules
        Schedule.query.filter_by(subject_id=subject_id).delete()
        
        # Delete the subject from the database
        db.session.delete(subject)
        db.session.commit()
        
        flash('Subject deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete subject: ' + str(e), 'error')

    return redirect(url_for('subject_bank'))



@app.route('/my_subjects', methods=['GET'])
@login_required
def my_subjects():
    if current_user.role != 'teacher':
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('dashboard'))

    teacher = Teacher.query.filter_by(teacher_id=current_user.id).first()
    if teacher:
        subjects = teacher.subjects

        # Group subjects by their sections
        subjects_by_section = defaultdict(list)
        for subject in subjects:
            for section in subject.sections:
                subjects_by_section[section].append(subject)

        return render_template('teacher/my_subjects.html', subjects_by_section=subjects_by_section)
    else:
        flash('You are not assigned to teach any subjects.', 'warning')
        return redirect(url_for('dashboard'))

@app.route('/my_schedule', methods=['GET'])
@login_required
def my_schedule():
    if current_user.role != 'teacher':
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('dashboard'))

    teacher = Teacher.query.filter_by(teacher_id=current_user.id).first()
    if teacher:
        subjects = teacher.subjects

        # Group subjects by their sections
        subjects_by_section = defaultdict(list)
        for subject in subjects:
            for section in subject.sections:
                subjects_by_section[section].append(subject)

        # Retrieve schedules for the subjects
        schedules_by_subject = {}
        for subject in subjects:
            for section in subject.sections:
                schedules = Schedule.query.filter_by(subject_id=subject.id).all()
                schedules_by_subject[subject] = schedules

        return render_template('teacher/my_schedule.html', subjects_by_section=subjects_by_section, schedules_by_subject=schedules_by_subject)
    else:
        flash('You are not assigned to teach any subjects.', 'warning')
        return redirect(url_for('dashboard'))

    
@app.route('/subject/<int:subject_id>/my_students', methods=['GET'])
@login_required
def my_students(subject_id):
    if current_user.role != 'teacher':
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('dashboard'))

    subject = Subject.query.get(subject_id)

    if not subject:
        flash('Subject not found.', 'danger')
        return redirect(url_for('dashboard'))

    # Retrieve the enrolled students for the subject's section
    enrolled_students = Student.query.join(Enrollment).filter(
        Enrollment.section_id.in_(
            db.session.query(section_subject_association.c.section_id).filter(
                section_subject_association.c.subject_id == subject_id
            )
        )
    ).all()

    # Fetch grades for the enrolled students in the specified subject
    grades = {}
    for student in enrolled_students:
        student_grades = Grades.query.filter_by(student_id=student.id, subject_id=subject_id).first()
        if student_grades:
            grades[student.id] = student_grades

    # Format final grades
    final_grades_formatted = {}
    for student_id, grade in grades.items():
        final_grade = grade.final_grade
        if final_grade is not None:
            final_grades_formatted[student_id] = "{:.2f}".format(float(final_grade))
        else:
            final_grades_formatted[student_id] = ""

    form1 = Period1Form()  # Instantiate Period1Form
    form2 = Period2Form()  # Instantiate Period2Form
    form3 = Period3Form()  # Instantiate Period3Form

    return render_template('teacher/my_students.html', subject=subject, enrolled_students=enrolled_students, grades=grades, final_grades_formatted=final_grades_formatted, form1=form1, form2=form2, form3=form3)

from sqlalchemy import and_

@app.route('/add_schedule/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def add_schedule(subject_id):
    subject = Subject.query.get(subject_id)
    form = ScheduleForm(request.form)  # Instantiate the schedule form

    if form.validate_on_submit():
        # Extract schedule details from the form
        day_of_week = '/'.join(request.form.getlist('day_of_week'))
        start_time = form.start_time.data
        end_time = form.end_time.data
        room = form.room.data

        try:
            # Check for existing schedule for the same subject
            existing_schedule = Schedule.query.filter(and_(Schedule.day_of_week == day_of_week, Schedule.subject_id == subject_id)).first()
            if existing_schedule:
                flash(f'A schedule already exists for {subject.title}. Please choose a different time.', 'error')
            else:
                # Create a new schedule object
                new_schedule = Schedule(day_of_week=day_of_week, start_time=start_time, end_time=end_time, room=room, subject_id=subject_id)

                # Add the new schedule to the database
                db.session.add(new_schedule)
                db.session.commit()

                flash('Schedule added successfully', 'success')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error adding schedule: {str(e)}")
            flash('An error occurred while adding the schedule. Please try again later.', 'error')

        # Redirect to the subjects page after adding the schedule
        return redirect(url_for('view_subjects', section_id=subject.sections[0].id, course_id=subject.course_id))


    return render_template('admin/add_schedule.html', subject=subject, form=form)



@app.route('/update_schedule/<int:schedule_id>', methods=['GET', 'POST'])
@login_required
def update_schedule(schedule_id):
    # Retrieve the schedule from the database
    schedule = Schedule.query.get_or_404(schedule_id)
    
    # Create a form and populate it with the existing schedule data
    form = ScheduleForm(request.form, obj=schedule)

    if form.validate_on_submit():
        # Update schedule details with form data
        schedule.day_of_week = '/'.join(request.form.getlist('day_of_week'))
        schedule.start_time = form.start_time.data
        schedule.end_time = form.end_time.data
        schedule.room = form.room.data
        
        try:
            # Commit changes to the database
            db.session.commit()
            flash('Schedule updated successfully', 'success')
            # Redirect to the subjects page after successful update
            return redirect(url_for('view_subjects', section_id=schedule.subject.section_id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the schedule. Please try again later.', 'error')
            app.logger.error(f"Error updating schedule: {str(e)}")

    # Pass schedule and subject information to the template
    return render_template('admin/update_schedule.html', form=form, schedule=schedule)


  
@app.route('/view_subjects', methods=['GET'])
@login_required
def view_subjects():
    schedule = Schedule.query.first()   
    section_id = request.args.get('section_id', type=int)
    current_app.logger.info(f"section_id: {section_id}")
    
    section = Section.query.get(section_id)
    
    # Fetch subjects associated with the section using the many-to-many relationship
    subjects = Subject.query.join(section_subject_association).filter(
        section_subject_association.c.section_id == section_id
    ).all()

    # Fetch schedules for each subject
    for subject in subjects:
        subject.schedules = Schedule.query.filter_by(subject_id=subject.id).all()

    current_app.logger.info(f"Number of subjects found: {len(subjects)}")

    form = ScheduleForm()
    
    return render_template('admin/view_subjects.html', subjects=subjects, section=section, form=form, schedule=schedule)




################################################################################################################################################################################################################    
@app.route('/admin/modules', methods=['GET', 'POST'])
@login_required
def modules():
    form_module = ModuleForm()
    courses = Course.query.all()
    form_module.course_id.choices = [(course.id, course.title) for course in courses]

    if form_module.validate_on_submit():
        title = form_module.title.data
        year = form_module.year.data
        course_id = form_module.course_id.data
        pdf_file = form_module.pdf_file.data
        pdf_filename = f"{title.replace(' ', '_')}.pdf"
        os.makedirs(os.path.join('uploads', 'documents'), exist_ok=True)
        pdf_file.save(os.path.join('uploads', 'documents', pdf_filename))
        new_module = Module(
            title=title,
            year=year,
            course_id=course_id,
            pdf_filename=pdf_filename,
        )
        db.session.add(new_module)
        db.session.commit()
        flash('Created successfully!', 'success')
        return redirect(url_for('modules'))

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 8
    offset = (page - 1) * per_page
    modules = Module.query.offset(offset).limit(per_page).all()  # Execute the query
    
    # Calculate total count for pagination
    total_modules_count = Module.query.count()

    # Extract distinct years from the modules
    years = list(set([module.year for module in modules]))

    pagination = Pagination(page=page, per_page=per_page, total=total_modules_count, css_framework='bootstrap4')
    
    return render_template('admin/modules.html', form_module=form_module, modules=modules, pagination=pagination, courses=courses, years=years)


@app.route('/student/modules', methods=['GET'])
@login_required
def student_modules():
    if current_user.role != 'student':
        return redirect(url_for('dashboard'))  
    
    page = request.args.get('page', 1, type=int)
    per_page = 8
    offset = (page - 1) * per_page
    modules = Module.query.offset(offset).limit(per_page).all()  # Execute the query
    
    # Calculate total count for pagination
    total_modules_count = Module.query.count()

    pagination = Pagination(page=page, per_page=per_page, total=total_modules_count, css_framework='bootstrap4')
    
    return render_template('student/view_modules.html', modules=modules, pagination=pagination)

@app.route('/teacher/modules', methods=['GET'])
@login_required
def teacher_modules():
    if current_user.role != 'teacher':
        return redirect(url_for('dashboard')) 
    
    page = request.args.get('page', 1, type=int)
    per_page = 8
    offset = (page - 1) * per_page
    modules = Module.query.offset(offset).limit(per_page).all()  # Execute the query
    
    # Calculate total count for pagination
    total_modules_count = Module.query.count()

    pagination = Pagination(page=page, per_page=per_page, total=total_modules_count, css_framework='bootstrap4')
    return render_template('teacher/view_modules.html', modules=modules, pagination=pagination)


@app.route('/download_module/<pdf_filename>', methods=['GET'])
@login_required
def download_module(pdf_filename):
    directory = os.path.join('uploads', 'documents')
    flash('Downloaded successfully!', 'success')
    return send_from_directory(directory, pdf_filename, as_attachment=True)

###################################################################################ENROLLMENT###############################################################################################################
@app.route('/enroll', methods=['GET', 'POST'])
@login_required
def enroll():
    student_form = StudentForm()
    student_id = request.args.get('student_id', type=int)
    student_form.student_id.data = student_id
    form = EnrollmentForm()
    courses = Course.query.all()
    sections = Section.query.all()

    if courses:
        form.course_id.choices = [(course.id, course.title) for course in courses]

    if sections:
        form.section_id.choices = [(section.id, section.name) for section in sections]


    students = Student.query.all()
    form.student_id.choices = [(student.id, student.first_name) for student in students]
    existing_enrollments = Enrollment.query.all()

    if form.validate_on_submit():


        existing_enrollment = Enrollment.query.filter_by(student_id=student_id, section_id=form.section_id.data).first()

        if existing_enrollment:
            flash('Student is already enrolled in this section.', 'danger')
        else:
            new_enrollment = Enrollment(
            student_id=form.student_id.data,
            year=form.year.data,
            course_id=form.course_id.data,
            section_id=form.section_id.data,
            
)

            db.session.add(new_enrollment)
            db.session.commit()
            flash(f'Students enrolled successfully!', 'success')
            return redirect(url_for('enroll'))

    return render_template('admin/enroll.html', form=form, student_form=student_form, existing_enrollments=existing_enrollments)

@app.route('/enrolled_subjects/<int:student_id>', methods=['GET'])
@login_required
def enrolled_subjects(student_id):
    enrolled_subjects = {}

    # Fetch enrolled subjects for the specified student
    existing_enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    for enrollment in existing_enrollments:
        section_id = enrollment.section_id
        enrolled_subjects[student_id] = Subject.query.filter_by(section_id=section_id).all()

    return render_template('admin/enrolled_subjects.html', enrolled_subjects=enrolled_subjects.get(student_id, []))

###########################################################################################################################################################################################################
@app.route('/add_grades/<int:student_id>/period1', methods=['GET', 'POST'])
@login_required
def add_grades_period1(student_id):
    form = Period1Form()
    subject_id = request.form.get('subject_id')
    grade = Grades.query.filter_by(student_id=student_id, subject_id=subject_id).first()

    if request.method == 'POST' and form.validate_on_submit():
        if grade:
            # If grade exists, update the existing grade
            form.populate_obj(grade)
            compute_grade(grade)
            db.session.commit()
            flash('Period 1 grade updated successfully!', 'success')
        else:
            # If grade doesn't exist, create a new one
            grade = Grades(student_id=student_id)
            form.populate_obj(grade)
            grade.subject_id = subject_id
            compute_grade(grade)
            db.session.add(grade)
            db.session.commit()
            flash('Period 1 grade added successfully!', 'success')
        
        return redirect(url_for('my_students', subject_id=subject_id))
    
    return render_template('web/my_students.html', form=form, subject_id=subject_id)

@app.route('/add_grades/<int:student_id>/period2', methods=['GET', 'POST'])
@login_required
def add_grades_period2(student_id):
    form = Period2Form()
    subject_id = request.form.get('subject_id')
    grade = Grades.query.filter_by(student_id=student_id, subject_id=subject_id).first()

    if request.method == 'POST' and form.validate_on_submit():
        if grade:
            # If grade exists, update the existing grade
            form.populate_obj(grade)
            compute_grade(grade)
            db.session.commit()
            flash('Period 2 grade updated successfully!', 'success')
        else:
            # If grade doesn't exist, create a new one
            grade = Grades(student_id=student_id)
            form.populate_obj(grade)
            grade.subject_id = subject_id
            compute_grade(grade)
            db.session.add(grade)
            db.session.commit()
            flash('Period 2 grade added successfully!', 'success')
        
        return redirect(url_for('my_students', subject_id=subject_id))
    
    return render_template('web/my_students.html', form=form, subject_id=subject_id)

@app.route('/add_grades/<int:student_id>/period3', methods=['GET', 'POST'])
@login_required
def add_grades_period3(student_id):
    form = Period3Form()
    subject_id = request.form.get('subject_id')
    grade = Grades.query.filter_by(student_id=student_id, subject_id=subject_id).first()

    if request.method == 'POST' and form.validate_on_submit():
        if grade:
            # If grade exists, update the existing grade
            form.populate_obj(grade)
            compute_grade(grade)
            db.session.commit()
            flash('Period 3 grade updated successfully!', 'success')
        else:
            # If grade doesn't exist, create a new one
            grade = Grades(student_id=student_id)
            form.populate_obj(grade)
            grade.subject_id = subject_id
            compute_grade(grade)
            db.session.add(grade)
            db.session.commit()
            flash('Period 3 grade added successfully!', 'success')
        
        return redirect(url_for('my_students', subject_id=subject_id))
    
    return render_template('web/my_students.html', form=form, subject_id=subject_id)



def compute_grade(grade):
    if grade.period_1 and grade.period_2 and grade.period_3:
        period_1 = int(grade.period_1)
        period_2 = int(grade.period_2)
        period_3 = int(grade.period_3)
        total = period_1 + period_2 + period_3
        result = total / 3.0
        grade.final_grade = str(result)
        grade.is_passed = result >= 75
    else:
        grade.final_grade = None
        grade.is_passed = False



@app.route('/grades/student_view', methods=['GET'])
@login_required
def student_view_grades():
    if current_user.is_authenticated and current_user.role == 'student':
        student = current_user.student
        grades = Grades.query.filter_by(student_id=student.id).all()
        enrollments = Enrollment.query.filter_by(student_id=student.id).all()

        if not grades:
            flash('No grades available for this student.', 'info')

        if not enrollments:
            flash('No enrollments found for this student.', 'info')

        # Query all teachers
        teachers = Teacher.query.all()

        # Dictionary to store teacher names and their subjects
        teacher_subjects = {}

        # Loop through each teacher
        for teacher in teachers:
            # Get the teacher's name
            teacher_name = f"{teacher.last_name} {teacher.middle_name} {teacher.first_name} {teacher.suffix}".strip()

            # Get the subjects taught by the teacher
            subjects_taught = [subject.title for subject in teacher.subjects]

            # Store the teacher's subjects in the dictionary
            teacher_subjects[teacher_name] = subjects_taught

        return render_template('student/view_grades.html', student=student, grades=grades, enrollments=enrollments, teacher_subjects=teacher_subjects)
    else:
        return redirect(url_for('dashboard'))


###############################################################################################################################################################
@app.route('/student/view_schedule', methods=['GET'])
@login_required
def view_schedule():
    if current_user.is_authenticated and current_user.role == 'student':
        student = current_user.student
        enrollments = Enrollment.query.filter_by(student_id=student.id).all()

        # Create a dictionary to store schedules for each subject
        subject_schedules = {}

        # If there are no enrollments, inform the user and render the template
        if not enrollments:
            flash('No enrollments found for this student.', 'info')
            return render_template('student/view_schedule.html', subject_schedules={})

        # Iterate over each enrollment
        for enrollment in enrollments:
            # Get the section for the enrollment
            section = enrollment.section
            # Get the subjects for the section
            subjects = section.subjects
            # Store the subjects and their schedules in the dictionary
            for subject in subjects:
                # Get the schedules for the subject
                schedules = Schedule.query.filter_by(subject_id=subject.id).all()
                # Store the schedules in the dictionary
                subject_schedules[subject] = schedules

        return render_template('student/view_schedule.html', subject_schedules=subject_schedules)
    else:
        return redirect(url_for('dashboard'))
    



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)