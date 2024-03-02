from flask import Flask, render_template, request, redirect, url_for, flash,  send_file,  send_from_directory, current_app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from models import db, User, Announcement, Certificate, UserAccount, Course, Subject, Section,Teacher,Student, Module, Comment, Enrollment, Enrollies, Grades, Schedule
from forms import LoginForm,  AnnouncementForm, CertificateForm, UpdateUserForm, UserAccountForm, CourseForm, SubjectForm,FilterForm, SectionForm, ChangePasswordForm
from forms import TeacherForm, StudentForm, ModuleForm, UpdateStudentForm, EnrollmentForm, EnrolliesForm, GradeForm, ScheduleForm, RegistrationForm, CommentForm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
import os
from flask_mail import Mail, Message

#'mysql+mysqlconnector://root:@localhost/apcba'
#'postgresql://apcba_raur_user:RdGTEi7roBWoYfW56OYbOHipLEFzUX4e@dpg-cnaanhgl5elc73962nlg-a.oregon-postgres.render.com/apcba_raur'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://apcba_raur_user:RdGTEi7roBWoYfW56OYbOHipLEFzUX4e@dpg-cnaanhgl5elc73962nlg-a.oregon-postgres.render.com/apcba_raur'
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'nicssanyo@gmail.com'
app.config['MAIL_PASSWORD'] = 'sanaymagisa24'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

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

        # Send email directly to your email address
        msg = Message(subject="New Comment",
                      sender=email,
                      recipients=["zdanlester@gmail.com"])  # Your email address
        msg.body = f"New comment from {name} ({email}):\n\n{comment_text}"
        mail.send(msg)

        return 'Comment submitted successfully!'

    return render_template('web/index.html', form=form)

@app.route('/web/websiteabout')
def websiteabout():
    return render_template('web/websiteabout.html')

@app.route('/web/websitecontact')
def websitecontact():
    return render_template('web/websitecontact.html')

@app.route('/web/portaluserlogin')
def portaluserlogin():
    return render_template('web/portaluserlogin.html')

@app.route('/web/websiteenroll')
def websiteenroll():
    return render_template('web/websiteenroll.html')

@app.route('/student/student_dashboard')
def student_dashboard():
    return render_template('student/student_dashboard.html')

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
      
        user = User.query.get(current_user.id)

       
        if not check_password_hash(user.password, form.old_password.data):
            flash('Incorrect current password. Please try again.', 'danger')
            return redirect(url_for('change_password'))

        
        hashed_password = generate_password_hash(form.new_password.data)

       
        user.password = hashed_password
        db.session.commit()

        flash('Password updated successfully!', 'success')
        return redirect(url_for('dashboard')) 
    return render_template('change_password.html', form=form)


@app.route('/web/enrollies', methods=['GET', 'POST'])
def enrollies():
    form = EnrolliesForm()

    if form.validate_on_submit():
        try:

            date_of_birth = datetime.strptime(form.date_of_birth.data, "%Y-%m-%d")
            password = date_of_birth.strftime("%Y-%m-%d")

            new_enrollies = Enrollies(
                name=form.name.data,
                email=form.email.data,
                level=form.level.data,
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
            user = User(
                name=form.name.data,
                password=password,
                email=form.email.data,
                role='student'
            )
            db.session.add(user)
            db.session.commit()

            student = Student(
                student_id=user.id,
                name=form.name.data
            )
            db.session.add(student)
            db.session.commit()

            flash('Enrollment successful!', 'success')
            return redirect(url_for('enrollies'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error during enrollment: {str(e)}")

    enrollies_list = Enrollies.query.all()
    return render_template('web/enrollies.html', form=form, enrollies_list=enrollies_list)

@app.route('/admin/view_enrollies')
def view_enrollies():
    enrollies_list = Enrollies.query.filter_by(is_archived=False).all()
    return render_template('admin/view_enrollies.html', enrollies_list=enrollies_list)

@app.route('/admin/view_archived_enrollies')
def view_archived_enrollies():
    archived_enrollies_list = Enrollies.query.filter_by(is_archived=True).all()
    return render_template('admin/view_archived_enrollies.html', archived_enrollies_list=archived_enrollies_list)

@app.route('/admin/archive_enrollie/<int:enrollie_id>')
@login_required
def archive_enrollie(enrollie_id):
    enrollie = Enrollies.query.get(enrollie_id)
    if enrollie:
        enrollie.is_archived = True
        db.session.commit()
    return redirect(url_for('view_enrollies'))

@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
def users():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('admin/dashboard'))

    # Fetch user data from the database
    users_data = User.query.all()

    # Search functionality
    search_query = request.args.get('q', default='', type=str)

    if search_query:
        users_data = User.query.filter(
            or_(
                User.username.ilike(f"%{search_query}%"),
                User.id.ilike(f"%{search_query}%"),
                User.name.ilike(f"%{search_query}%"),
            )
        ).all()


    # Handle form submissions
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

    return render_template('admin/users.html', users=users_data, search_query=search_query, teacher_form=teacher_form, student_form=student_form)


@app.route('/admin/teachers')
@login_required
def view_teachers():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    teachers_data = Teacher.query.all()

    return render_template('admin/view_teachers.html', teachers=teachers_data)

@app.route('/admin/students', methods=['GET'])
@login_required
def view_students():
    if current_user.role != 'admin':

        return redirect(url_for('dashboard'))

    students_data = (
        db.session.query(Student, Section.name.label('section_name'))
        .outerjoin(Enrollment, Student.id == Enrollment.student_id)
        .add_columns(Student.student_id, Student.id, Student.name, db.func.count(Enrollment.id).label('enrollment_count'))
        .group_by(Student.student_id, Student.id, Student.name, Section.name)
        .all()
    )

    sections_data = Section.query.all()

    return render_template('admin/view_students.html', students=students_data, sections=sections_data)

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

@app.route('/web/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        if user:
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
    return render_template('web/login.html', form=form, )
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = AnnouncementForm()

    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data, content=form.content.data, author_id=current_user.id)
        db.session.add(announcement)
        db.session.commit()

    announcements = Announcement.query.order_by(Announcement.timestamp.desc()).all()

    if current_user.role == 'student':
        template = 'student/student_dashboard.html'
    elif current_user.role == 'teacher':
        template = 'teacher/teacher_dashboard.html'
    elif current_user.role == 'admin':
        template = 'admin/dashboard.html'
    else:
        return redirect(url_for('index'))

    return render_template(template, user=current_user, form=form, announcements=announcements,)

@app.route('/admin/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = form.password.data  # In a real application, you should hash the password

        # Create a new user with the provided information and set the user_id
        user = User(
            email=form.email.data,
            name=form.name.data,
            password=hashed_password,
            role=form.role.data,
        )

        # Add the user to the database
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('register'))

    return render_template('admin/register.html', form=form)


@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('dashboard'))

    user_to_update = User.query.get(user_id)
    if not user_to_update:
        flash('User not found.', 'danger')
        return redirect(url_for('dashboard'))

    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.new_email.data:
            user_to_update.email = form.new_email.data
        if form.new_password.data:
            user_to_update.password = form.new_password.data  # In a real application, you should hash the password
        if form.new_role.data:
            user_to_update.role = form.new_role.data

        db.session.commit()
        flash(f'User updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('admin/update_user.html', form=form, user=user_to_update)


@app.route('/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('users'))

    user_to_delete = User.query.get(user_id)
    if not user_to_delete:
        return redirect(url_for('users'))

    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('users'))

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
        
    if current_user.role == 'student':
        title_filter = request.args.get('title', default='', type=str)
        certificates = Certificate.query.filter_by(user_id=current_user.id).order_by(Certificate.id.desc()).all()
        template = 'student/student_certificate.html'
    elif current_user.role == 'teacher':
        title_filter = request.args.get('title', default='', type=str)
        certificates = Certificate.query.order_by(Certificate.id.desc()).all()
        template = 'teacher/teacher_certificate.html'
    elif current_user.role == 'admin':
        title_filter = request.args.get('title', default='', type=str)
        certificates = Certificate.query.filter(Certificate.title.ilike(f'%{title_filter}%')).order_by(Certificate.id.desc()).all()
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
    return redirect(url_for('certificate'))

@app.route('/admin/download_certificate/<int:certificate_id>')
@login_required
def download_certificate(certificate_id):
    certificate = Certificate.query.get(certificate_id)

    if not certificate or current_user.id != certificate.user_id:
        return redirect(url_for('certificate'))

    certificate_path = os.path.join('uploads', 'documents', certificate.pdf)
    return send_file(certificate_path, as_attachment=True)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
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
        return redirect(url_for('account'))

    return render_template('account.html', form=form)
#######################################################################################################################################################################################
@app.route('/courses', methods=['GET', 'POST'])
@login_required
def view_course():
    form_course = CourseForm()
    form_subject = SubjectForm()
    filter_form = FilterForm()
    form_subject.set_course_choices(Course.query.all())
    
    if form_course.validate_on_submit():
        new_course = Course(
            course_type=form_course.course_type.data,
            abbreviation=form_course.abbreviation.data,
            title=form_course.title.data,
            school_year=form_course.school_year.data,
            year=form_course.year.data,
            Class=form_course.Class.data,
            semesters=form_course.semesters.data,
            is_active=form_course.is_active.data
        )
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('view_course'))
    school_year_filter = request.args.get('school_year', type=str)
    semester_filter = request.args.get('semester', type=int)
    course_type_filter = request.args.get('course_type', type=str)
    courses_query = Course.query
    if school_year_filter:
        courses_query = courses_query.filter_by(school_year=school_year_filter)
    if semester_filter:
        courses_query = courses_query.filter_by(semesters=semester_filter)
    if course_type_filter:
        courses_query = courses_query.filter_by(course_type=course_type_filter)

    courses = courses_query.all()

    if form_subject.validate_on_submit():
        new_subject = Subject(
            abbreviation=form_subject.abbreviation.data,
            title=form_subject.title.data,
            unit=form_subject.unit.data,
            course_id=form_subject.course_id.data,
        )
        db.session.add(new_subject)
        db.session.commit()
        return redirect(url_for('view_course'))

    return render_template('admin/view_course.html', courses=courses, form_course=form_course, form_subject=form_subject, filter_form=filter_form)

@app.route('/update_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)

    if form.validate_on_submit():
        course.course_type = form.course_type.data
        course.abbreviation = form.abbreviation.data
        course.title = form.title.data
        course.school_year = form.school_year.data
        course.year = form.year.data
        course.Class = form.Class.data
        course.semesters = form.semesters.data
        course.is_active = form.is_active.data

        db.session.commit()
        return redirect(url_for('view_course'))

    return render_template('admin/update_course.html', form=form, course=course)

@app.route('/update_subject/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def update_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = SubjectForm(obj=subject)
    form.course_id.choices = [(course.id, course.title) for course in Course.query.all()]

    if form.validate_on_submit():
        subject.abbreviation = form.abbreviation.data
        subject.title = form.title.data
        subject.unit = form.unit.data
        subject.course_id = form.course_id.data

        db.session.commit()
        return redirect(url_for('view_course'))

    return render_template('admin/update_subject.html', form=form, subject=subject)
##########################################################################################################################################################################################
@app.route('/sections', methods=['GET', 'POST'])
@login_required
def manage_section():
    form_section = SectionForm()
    course_id_filter = request.args.get('course_id', type=int)
    section_name_filter = request.args.get('section_name', type=str)
    sections_query = Section.query
    if course_id_filter:
        sections_query = sections_query.filter_by(course_id=course_id_filter)
    if section_name_filter:
        sections_query = sections_query.filter(Section.name.ilike(f'%{section_name_filter}%'))
    sections = sections_query.all()
    courses = Course.query.all()
    form_section.course_id.choices = [(course.id, course.title) for course in courses]
    teachers = Teacher.query.all()
    form_section.set_teacher_choices(teachers)

    if form_section.validate_on_submit():
        selected_teacher_id = form_section.teacher_id.data

        new_section = Section(
            name=form_section.name.data,
            capacity=form_section.capacity.data,
            course_id=form_section.course_id.data,
            teacher_id=selected_teacher_id
        )
        db.session.add(new_section)
        db.session.commit()

        course = Course.query.get(form_section.course_id.data)
        if course:
            subjects_from_course = Subject.query.filter_by(course_id=course.id).all()
            for subject in subjects_from_course:
                subject.section_id = new_section.id
                db.session.add(subject)
        
        db.session.commit()
        return redirect(url_for('manage_section'))

    return render_template('admin/manage_section.html', sections=sections, courses=courses,
                           form_section=form_section)

@app.route('/view_subjects', methods=['GET'])
@login_required
def view_subjects():
    section_id = request.args.get('section_id', type=int)
    course_id = request.args.get('course_id', type=int)
    current_app.logger.info(f"section_id: {section_id}, course_id: {course_id}")
    subjects = Subject.query.filter_by(section_id=section_id, course_id=course_id).all()

    for subject in subjects:
        subject.schedules = Schedule.query.filter_by(subject_id=subject.id).all()

    current_app.logger.info(f"Number of subjects found: {len(subjects)}")

    return render_template('admin/view_subjects.html', subjects=subjects)
################################################################################################################################################################################################################    
@app.route('/view_modules', methods=['GET', 'POST'])
@login_required
def view_modules():
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
    modules = Module.query.all()
    if current_user.role == 'admin':
        template = 'admin/view_modules.html'
    elif current_user.role == 'teacher':
        template = 'teacher/view_modules.html'
    elif current_user.role == 'student':
        template = 'student/view_modules.html'
    else:
        return redirect(url_for('index'))

    return render_template(template, form_module=form_module, modules=modules)

@app.route('/download_module/<pdf_filename>', methods=['GET'])
@login_required
def download_module(pdf_filename):
    directory = os.path.join('uploads', 'documents')
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
    form.student_id.choices = [(student.id, student.name) for student in students]
    existing_enrollments = Enrollment.query.all()

    if form.validate_on_submit():


        existing_enrollment = Enrollment.query.filter_by(student_id=student_id, section_id=form.section_id.data).first()

        if existing_enrollment:
            flash('Student is already enrolled in this section.', 'danger')
        else:
            new_enrollment = Enrollment(
            student_id=form.student_id.data,
            course_id=form.course_id.data,
            section_id=form.section_id.data,
            is_approved=form.is_approved.data
)

            db.session.add(new_enrollment)
            db.session.commit()

            flash('Enrollment successful.', 'success')

    return render_template('admin/enroll.html', form=form, student_form=student_form, existing_enrollments=existing_enrollments)
###########################################################################################################################################################################################################
@app.route('/grades/<int:student_id>', methods=['GET', 'POST'])
@login_required
def view_grades(student_id):
    student = Student.query.get_or_404(student_id)
    subjects = Subject.query.all()
    grades = Grades.query.all()

    form = GradeForm()

    if request.method == 'POST':
        grades = []

        for subject in subjects:
            period_1 = request.form.get(f'period_1_{subject.id}')
            period_2 = request.form.get(f'period_2_{subject.id}')
            period_3 = request.form.get(f'period_3_{subject.id}')

            form.period_1.data = period_1
            form.period_2.data = period_2
            form.period_3.data = period_3

            if not form.validate():
                print(f'Validation Errors for Subject {subject.id}: {form.errors}')

            final_grade = (float(period_1) + float(period_2) + float(period_3)) / 3.0
            is_passed = final_grade >= 75

            grade = Grades(
                student_id=student.id,
                subject_id=subject.id,
                period_1=period_1,
                period_2=period_2,
                period_3=period_3,
                final_grade=final_grade,
                is_passed=is_passed
            )
            grades.append(grade)

        db.session.add_all(grades)
        db.session.commit()
        return redirect(url_for('view_grades', student_id=student_id))

    return render_template('admin/view_grades.html', student=student, subjects=subjects, form=form)


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

        return render_template('student/view_grades.html', student=student, grades=grades, enrollments=enrollments)
    else:

        return redirect(url_for('dashboard'))

###############################################################################################################################################################
@app.route('/add_schedule/<int:section_id>', methods=['GET', 'POST'])
@login_required
def add_schedule(section_id):
    form = ScheduleForm()

    section = Section.query.get_or_404(section_id)
    subjects = Subject.query.filter_by(section_id=section.id).all()

    if form.validate_on_submit():
        day_of_week = form.day_of_week.data
        start_time = form.start_time.data
        end_time = form.end_time.data

        try:
            for subject in subjects:
                new_schedule = Schedule(day_of_week=day_of_week, start_time=start_time, end_time=end_time, subject_id=subject.id)
                db.session.add(new_schedule)

            db.session.commit()
            current_app.logger.info("Schedules added successfully")
            return redirect(url_for('view_subjects', section_id=section_id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error adding schedules: {str(e)}")
   
    return render_template('admin/add_schedule.html', form=form, section=section, subjects=subjects)

@app.route('/view_schedule')
@login_required
def view_schedule():
    try:
        user_enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
        course_ids = [enrollment.course_id for enrollment in user_enrollments]
        section_ids = [enrollment.section_id for enrollment in user_enrollments]
        schedules = Schedule.query.filter(Schedule.subject.has(Subject.course_id.in_(course_ids)), Schedule.subject.has(Subject.section_id.in_(section_ids))).all()
        
        return render_template('student/view_schedule.html', schedules=schedules)
    except Exception as e:
        current_app.logger.error(f"Error retrieving schedules: {str(e)}")

        return redirect(url_for('dashboard'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

