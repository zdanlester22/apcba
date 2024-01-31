from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()





class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    # Establishing a one-to-one relationship with user_account
    user_account = db.relationship('user_account', backref='user', uselist=False, lazy=True)


class user_account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255))
    age = db.Column(db.Integer)
    birthday = db.Column(db.Integer)  # Assuming birthday is an IntegerField
    place_of_birth = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    civil_status = db.Column(db.String(50))
    nationality = db.Column(db.String(50))
    current_country = db.Column(db.String(100))
    current_region = db.Column(db.String(100))
    current_province = db.Column(db.String(100))
    current_municipality = db.Column(db.String(100))
    current_complete_address = db.Column(db.Text)
    permanent_country = db.Column(db.String(100))
    permanent_region = db.Column(db.String(100))
    permanent_province = db.Column(db.String(100))
    permanent_municipality = db.Column(db.String(100))
    permanent_complete_address = db.Column(db.Text)
    school_issued_mobile = db.Column(db.String(20))
    school_email = db.Column(db.String(120))
    personal_country_code = db.Column(db.String(10))
    personal_tel_no = db.Column(db.String(20))
    personal_mobile_1 = db.Column(db.String(20))
    personal_mobile_2 = db.Column(db.String(20))
    personal_mobile_3 = db.Column(db.String(20))
    personal_email = db.Column(db.String(120))
    religion = db.Column(db.String(50))
    facebook = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    school_level = db.Column(db.String(100))
    school_name = db.Column(db.String(255))
    course = db.Column(db.String(100))
    year_graduated = db.Column(db.String(50))
    last_school_attended = db.Column(db.String(255))
    father_last_name = db.Column(db.String(255))
    father_first_name = db.Column(db.String(255))
    father_middle_name = db.Column(db.String(255))
    father_occupation = db.Column(db.String(255))
    father_contact_no = db.Column(db.String(20))
    mother_last_name = db.Column(db.String(255))
    mother_first_name = db.Column(db.String(255))
    mother_middle_name = db.Column(db.String(255))
    mother_occupation = db.Column(db.String(255))
    mother_contact_no = db.Column(db.String(20))
    num_brothers = db.Column(db.Integer)
    num_sisters = db.Column(db.Integer)
    guardian_occupation = db.Column(db.String(255))
    guardian_relationship = db.Column(db.String(50))
    guardian_contact_no = db.Column(db.String(20))
    emergency_contact_name = db.Column(db.String(255))
    emergency_contact_relationship = db.Column(db.String(50))
    emergency_contact_no = db.Column(db.String(20))
    emergency_contact_address = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)


class Announcement(db.Model):
    __tablename__ = 'announcement'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref='announcements')


class Certificate(db.Model):
    __tablename__ = 'certificate'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    pdf = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', back_populates='sections', lazy=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))  
    teacher = db.relationship('Teacher', back_populates='section', uselist=False)
    subjects = db.relationship('Subject', back_populates='section', lazy=True)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    abbreviation = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', back_populates='subjects', lazy=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
    section = db.relationship('Section', back_populates='subjects')
    grades = db.relationship('Grades', back_populates='subject', lazy=True)
    schedules = db.relationship('Schedule', back_populates='subject', lazy=True)


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    section = db.relationship('Section', back_populates='teacher', uselist=False)


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref='modules')
    pdf_filename = db.Column(db.String(255), nullable=False)


class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)

    enrolled_student_rel = db.relationship('Student', backref='enrollment', single_parent=True)
    enrolled_course_rel = db.relationship('Course', backref='enrollments_course')
    enrolled_section_rel = db.relationship('Section', backref='enrollments_section')


class Enrollies(db.Model):
    __tablename__ = 'enrollies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    level = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255))
    contact_number = db.Column(db.String(15))
    date_of_birth = db.Column(db.Date)
    place_of_birth = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    nationality = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    previous_school_info = db.Column(db.String(100))
    grade_last_completed = db.Column(db.String(10))
    academic_achievements = db.Column(db.String(255))
    proof_of_address = db.Column(db.String(255))
    parent_names = db.Column(db.String(200))
    parent_contact_info = db.Column(db.String(30))
    parent_occupation = db.Column(db.String(100))
    special_needs = db.Column(db.String(255))


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    grades = db.relationship('Grades', back_populates='student', lazy=True)
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_type = db.Column(db.String(20), nullable=False)
    abbreviation = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    Class = db.Column(db.String(100))
    year = db.Column(db.String(20), nullable=False)
    school_year = db.Column(db.String(20), nullable=False)
    semesters = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    sections = db.relationship('Section', back_populates='course', lazy=True)
    subjects = db.relationship('Subject', back_populates='course', lazy=True)


class Grades(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    period_1 = db.Column(db.String(5))
    period_2 = db.Column(db.String(5))
    period_3 = db.Column(db.String(5))
    final_grade = db.Column(db.String(5))
    is_passed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    student = db.relationship('Student', back_populates='grades')
    subject = db.relationship('Subject', back_populates='grades')


class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day_of_week = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject = db.relationship('Subject', back_populates='schedules', lazy=True)





