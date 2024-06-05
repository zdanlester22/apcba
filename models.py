from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import LargeBinary
db = SQLAlchemy()




class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=False)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    suffix = db.Column(db.String(10))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    # Establishing a one-to-one relationship with user_account
    user_account = db.relationship('UserAccount', backref='user', uselist=False, lazy=True)
    student = db.relationship('Student', backref='user', uselist=False)


class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    lrn = db.Column(db.String(12))
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    suffix = db.Column(db.String(10))
    email = db.Column(db.String(100), nullable=False, unique=True)
    track_strand = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    year = db.Column(db.String(20), nullable=False)
    contact_number = db.Column(db.String(15))
    date_of_birth = db.Column(db.Date)
    place_of_birth = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    nationality = db.Column(db.String(50))
    parent_names = db.Column(db.String(200))
    parent_contact_info = db.Column(db.String(30))




class Announcement(db.Model):
    __tablename__ = 'announcement'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref='announcements')
    archived = db.Column(db.Boolean, default=False)


class Certificate(db.Model):
    __tablename__ = 'certificate'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    pdf = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


section_subject_association = db.Table(
    'section_subject_association',
    db.Column('section_id', db.Integer, db.ForeignKey('sections.id')),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'))
)


class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    school_year = db.Column(db.String(20), nullable=False)
    course = db.relationship('Course', back_populates='sections', lazy=True)
    is_archived = db.Column(db.Boolean, default=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'))
    teacher = db.relationship('Teacher', back_populates='section', uselist=False)
    enrollments = db.relationship('Enrollment', backref='section', lazy=True)
    subjects = db.relationship('Subject', secondary=section_subject_association, back_populates='sections', lazy='dynamic')
    is_archived = db.Column(db.Boolean, default=False)


    


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    abbreviation = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    semester = db.Column(db.String(50))
    year = db.Column(db.String(50))
    course = db.relationship('Course', backref='subjects')
    grades = db.relationship('Grades', back_populates='subject', lazy=True)
    schedules = db.relationship('Schedule', back_populates='subject', lazy=True)
    teachers = db.relationship('Teacher', secondary='subject_teacher_association', back_populates='subjects')
    sections = db.relationship('Section', secondary=section_subject_association, back_populates='subjects', lazy='dynamic')

    


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    suffix = db.Column(db.String(10))
    active = db.Column(db.Boolean, default=True, nullable=False)
    section = db.relationship('Section', back_populates='teacher', uselist=False)
    subjects = db.relationship('Subject', secondary='subject_teacher_association', back_populates='teachers')




subject_teacher_association = db.Table('subject_teacher_association',
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id')), 
    db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'))  
)






class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref='modules')
    pdf_data = db.Column(LargeBinary, nullable=False)
    archived = db.Column(db.Boolean, default=False)


class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    is_finished = db.Column(db.Boolean, default=False)  # New field to track if finished
    enrolled_student_rel = db.relationship('Student', back_populates='enrollments', single_parent=True)
    enrolled_course_rel = db.relationship('Course', backref='enrollments_course')
    enrolled_section_rel = db.relationship('Section', backref='enrollments_section')


    


class Enrollies(db.Model):
    __tablename__ = 'enrollies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    suffix = db.Column(db.String(10))
    email = db.Column(db.String(100), nullable=False, unique=True)
    track_strand = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    previous_school_info = db.Column(db.String(100))
    parent_names = db.Column(db.String(200), nullable=False)
    parent_contact_info = db.Column(db.String(30), nullable=False)
    is_archived = db.Column(db.Boolean, default=False)
    is_rejected = db.Column(db.Boolean, default=False)


class SeniorEnrollies(db.Model):
    __tablename__ = 'seniorenrollies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    suffix = db.Column(db.String(10))
    email = db.Column(db.String(100), nullable=False, unique=True)
    lrn = db.Column(db.String(15))
    track_strand = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    year = db.Column(db.String(20), nullable=False)
    contact_number = db.Column(db.String(15))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    previous_school_info = db.Column(db.String(100))
    parent_names = db.Column(db.String(200))
    parent_contact_info = db.Column(db.String(30))
    is_archived = db.Column(db.Boolean, default=False)
    is_rejected = db.Column(db.Boolean, default=False)
    
class TesdaEnrollies(db.Model):
    __tablename__ = 'tesdaenrollies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    suffix = db.Column(db.String(10))
    email = db.Column(db.String(100), nullable=False, unique=True)
    track_strand = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    year = db.Column(db.String(20), nullable=False)
    contact_number = db.Column(db.String(15))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    previous_school_info = db.Column(db.String(100))
    parent_names = db.Column(db.String(200))
    parent_contact_info = db.Column(db.String(30))
    is_archived = db.Column(db.Boolean, default=False)
    is_rejected = db.Column(db.Boolean, default=False)


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    suffix = db.Column(db.String(10))
    active = db.Column(db.Boolean, default=True, nullable=False)
    is_graduate = db.Column(db.Boolean, default=False, nullable=False)  # Add this line
    grades = db.relationship('Grades', back_populates='student', lazy=True)
    enrollments = db.relationship('Enrollment', back_populates='enrolled_student_rel', lazy=True)



class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_type = db.Column(db.String(20), nullable=False)
    abbreviation = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    Class = db.Column(db.String(100))
    year = db.Column(db.String(20), nullable=False)
    semesters = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    sections = db.relationship('Section', back_populates='course', lazy=True)
    archived = db.Column(db.Boolean, default=False)



class Grades(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    period_1 = db.Column(db.String(20))
    period_2 = db.Column(db.String(20))
    period_3 = db.Column(db.String(20))
    final_grade = db.Column(db.String(30))
    is_passed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    student = db.relationship('Student', back_populates='grades')
    subject = db.relationship('Subject', back_populates='grades')


class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day_of_week = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.String(8), nullable=False)  
    end_time = db.Column(db.String(8), nullable=False)    
    room = db.Column(db.String(50))  
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject = db.relationship('Subject', back_populates='schedules', lazy=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher = db.relationship('Teacher', backref='schedules', lazy=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    section = db.relationship('Section', backref='schedules', lazy=True)





    





