from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField,  validators
from wtforms.validators import DataRequired,Optional,Email
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import StringField, SubmitField, IntegerField, DateField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Length, InputRequired, EqualTo
from wtforms.fields import FloatField, TimeField



class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name')
    last_name = StringField('Last Name', validators=[DataRequired()])
    suffix = StringField('Suffix')
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')],
                       validators=[DataRequired()])

    
class UpdateUserForm(FlaskForm):
    new_email = StringField('New Email')
    new_first_name = StringField('New First Name', validators=[DataRequired()])
    new_middle_name = StringField('New Middle Name')
    new_last_name = StringField('New Last Name', validators=[DataRequired()])
    new_suffix = StringField('New Suffix')
    new_password = PasswordField('New Password')
    submit = SubmitField('Update User')


    

class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post Announcement')

class CertificateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    pdf = FileField('PDF File', validators=[FileAllowed(['pdf'], 'PDFs only!')])
    submit = SubmitField('Upload Certificate')


class UserAccountForm(FlaskForm):
    name = StringField('Full Name')
    email = StringField('Email')
    track_strand = StringField('Track & Strand')  
    address = StringField('Home Address')
    year = StringField('Year')
    lrn = StringField('LRN (Learner Reference Number)')
    contact_number = StringField('Contact Number')
    date_of_birth = StringField('Date of Birth')
    place_of_birth = StringField('Place of Birth')
    gender = StringField('Gender')
    nationality = StringField('Nationality')
    parent_names = StringField('Names of Parents/Guardians')
    parent_contact_info = StringField('Contact Information of Parents/Guardians')




class CourseForm(FlaskForm):
    abbreviation = StringField('Abbreviation', validators=[DataRequired()])
    title = StringField('Title Name', validators=[DataRequired()])
    year_choices = [('Grade 11', 'Grade 11'), ('Grade 12', 'Grade 12'), ('First Year', 'First Year'), ('Second Year', 'Second Year'), ('Third Year', 'Third Year'), ('Fourth Year', 'Fourth Year')]
    year = SelectField('Year', choices=year_choices, validators=[validators.DataRequired()])
    Class = StringField('Class', validators=[DataRequired()])
    semesters = SelectField('Semesters', choices=[('1st Semester', '1st Semester'), ('2nd Semester', '2nd Semester')], validators=[DataRequired()])
    course_type = SelectField('Type', choices=[('SHS', 'SHS'), ('College', 'College'), ('TESDA', 'TESDA')], validators=[DataRequired()])
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Create Course')

class SubjectForm(FlaskForm):
    abbreviation = StringField('Abbreviation', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    unit = IntegerField('Unit', validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])

    
class FilterForm(FlaskForm):
    school_year = StringField('School Year')
    semester = IntegerField('Semester')
    course_type = SelectField('Course Type', choices=[('', 'All'), ('SHS', 'SHS'), ('College', 'College')])

class SectionForm(FlaskForm):
    name = StringField('Section Name', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    year_choices = [('Grade 11', 'Grade 11'), ('Grade 12', 'Grade 12'), ('First Year', 'First Year'), ('Second Year', 'Second Year'), ('Third Year', 'Third Year'), ('Fourth Year', 'Fourth Year')]
    year = SelectField('Year', choices=year_choices, validators=[validators.DataRequired()])
    school_year = StringField('School year', validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    teacher_id = SelectField('Teacher', coerce=int, validators=[DataRequired()])

    def set_teacher_choices(self, teachers):
        self.teacher_id.choices = [
            (teacher.id, f"{teacher.first_name} {teacher.middle_name} {teacher.last_name} {teacher.suffix}".strip())
            for teacher in teachers
        ]


class TeacherForm(FlaskForm):
    teacher_id = IntegerField('Teacher ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Teacher')

class StudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Student')

class UpdateStudentForm(FlaskForm):
    student_id = StringField('Student ID', render_kw={'readonly': True})  # Read-only field for student_id
    updated_name = StringField('Updated Name', validators=[DataRequired()])
    submit = SubmitField('Update Student')

class ModuleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    pdf_file = FileField('PDF File', validators=[DataRequired()])

class EnrollmentForm(FlaskForm):
    student_id = SelectField('Student', choices=[], coerce=int)
    course_id = SelectField('Course', choices=[], coerce=int)
    section_id = SelectField('Section', choices=[], coerce=int)
    year = IntegerField('Year', validators=[DataRequired()])
    
    def set_student_choices(self, students):
        self.student_id.choices = [
            (student.id, f"{student.first_name} {student.middle_name} {student.last_name}".strip())
            for student in students
        ]


class EnrolliesForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    suffix = StringField('Suffix', validators=[Optional()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    track_strand_choices = [
        ('BTVTED','Bachelor of Technical Vocational Teachers Education (BTVTED)'),
        ('Hospitality and tourism Technology', '3 Years Diploma Hospitality and tourism Technology'),
        ('Hotel and Restaurant Services', '1 Year Hotel and Restaurant Services')
    ]
    track_strand = SelectField('Track & Strand', choices=track_strand_choices, validators=[DataRequired()])

    address = StringField('Home Address', validators=[DataRequired()])
    year_choices = [
        ('First Year', 'First Year'), 
        ('Second Year', 'Second Year'), 
        ('Third Year', 'Third Year'), 
        ('Fourth Year', 'Fourth Year')
    ]
    year = SelectField('Year', choices=year_choices, validators=[DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    date_of_birth = StringField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    previous_school_info = StringField('Previous School Information', validators=[Optional()])
    parent_names = StringField('Names of Parents/Guardians', validators=[DataRequired()])
    parent_contact_info = StringField('Contact Information of Parents/Guardians', validators=[DataRequired()])



class SeniorEnrolliesForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name')
    last_name = StringField('Last Name', validators=[DataRequired()])
    suffix = StringField('Suffix')
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Home Address', validators=[DataRequired()])
    year_choices = [('Grade 11', 'Grade 11'), ('Grade 12', 'Grade 12')]
    year = SelectField('Year', choices=year_choices, validators=[DataRequired()])
    lrn = StringField('LRN (Learner Reference Number)', validators=[DataRequired(), Length(min=12, max=12)])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    date_of_birth = StringField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    previous_school_info = StringField('Previous School Information')
    parent_names = StringField('Names of Parents/Guardians', validators=[DataRequired()])
    parent_contact_info = StringField('Contact Information of Parents/Guardians', validators=[DataRequired()])

    track_strand_choices = [
        ('GAs', 'General Academic Strand (GAs)'),
        ('STEM', 'STEM (Science, Technology, Engineering, Mathematics)'),
        ('ABM', 'ABM (Accountancy, Business, Management)'),
        ('TVL-Home Economics-Housekeeping', 'TVL-Home Economics'),
        ('TVL-ICT', 'TVL-ICT (Computer System Services NC II)'),
        ('HUMMS', 'HUMMS (Humanities and Social Sciences)'),
    ]
    track_strand = SelectField('Track & Strand', choices=track_strand_choices, validators=[DataRequired()])


class TesdaEnrolliesForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name')
    last_name = StringField('Last Name', validators=[DataRequired()])
    suffix = StringField('Suffix')
    email = StringField('Email', validators=[DataRequired(), Email()])
    track_strand_choices = [
        ('Contact Center Services'),
        ('Events Management NC III'),
        ('TVL-Home Economics-Housekeeping'),
        ('Shielded Metal Arc Welding NC II & Pipefitting NC II')
       
    ]
    track_strand = SelectField('Track & Strand', choices=track_strand_choices, validators=[DataRequired()])

    address = StringField('Home Address', validators=[DataRequired()])
    year_choices = [ ('First Year', 'First Year'), ('Second Year', 'Second Year'), ('Third Year', 'Third Year'), ('Fourth Year', 'Fourth Year')]
    year = SelectField('Year', choices=year_choices, validators=[validators.DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    date_of_birth = StringField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    previous_school_info = StringField('Previous School Information')
    parent_names = StringField('Names of Parents/Guardians', validators=[DataRequired()])
    parent_contact_info = StringField('Contact Information of Parents/Guardians', validators=[DataRequired()])


    
class Period1Form(FlaskForm):
    period_1 = StringField('Period 1')
    submit = SubmitField('Submit')

class Period2Form(FlaskForm):
    period_2 = StringField('Period 2')
    submit = SubmitField('Submit')

class Period3Form(FlaskForm):
    period_3 = StringField('Period 3')
    submit = SubmitField('Submit')

class ScheduleForm(FlaskForm):
    day_of_week = StringField('Day of Week', validators=[InputRequired()])
    start_time = StringField('Start Time', validators=[InputRequired()])
    end_time = StringField('End Time', validators=[InputRequired()])
    room = StringField('Room')
    submit = SubmitField('Add Schedule')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Change Password')

class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AssignTeacherToSubjectForm(FlaskForm):
    teacher_id = SelectField('Teacher', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Teacher')
    
    def set_teacher_choices(self, teachers):
        self.teacher_id.choices = [(teacher.id, teacher.first_name) for teacher in teachers]

class ForgetpasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Change Password')