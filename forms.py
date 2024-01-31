from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired,Optional,Email
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import StringField, SubmitField, IntegerField, DateField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Length, InputRequired
from wtforms.fields import FloatField, TimeField



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')],
                       validators=[DataRequired()])
    

class UpdateUserForm(FlaskForm):
    new_username = StringField('New Username')
    new_name = StringField('New Name', validators=[DataRequired()])
    new_contact = StringField('New Contact', validators=[DataRequired()])
    new_password = PasswordField('New Password')
    new_role = SelectField('New Role', choices=[('admin', 'Admin'), ('teacher', 'Teacher'), ('student', 'Student')])
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
   # Program Information
    course = StringField('Course')
    year_level = StringField('Year Level')
    lrn = StringField("DedEd Learner's Reference Number (LRN)")
    curriculum_year = StringField('Curriculum Year')
    
    # Personal Data
    last_name = StringField('Last Name', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', validators=[DataRequired()])
    
    # Place of Birth
    place_of_birth = StringField('Place of Birth', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    civil_status = StringField('Civil Status', validators=[DataRequired()])
    nationality = StringField('Nationality', validators=[DataRequired()])
    
    # Current Address
    current_country = StringField('Country', validators=[DataRequired()])
    current_region = StringField('Region', validators=[DataRequired()])
    current_province = StringField('Province', validators=[DataRequired()])
    current_municipality = StringField('Municipality', validators=[DataRequired()])
    current_complete_address = TextAreaField('Complete Address (Rm# Bldg./House#, Street, Brgy.)')
    
    # Permanent Address
    permanent_country = StringField('Country', validators=[DataRequired()])
    permanent_region = StringField('Region', validators=[DataRequired()])
    permanent_province = StringField('Province', validators=[DataRequired()])
    permanent_municipality = StringField('Municipality', validators=[DataRequired()])
    permanent_complete_address = TextAreaField('Complete Address (Rm# Bldg./House#, Street, Brgy.)')
    
    # Contact Information
    school_issued_mobile = StringField('School Issued Mobile No.', validators=[DataRequired()])
    school_email = StringField('School Email', validators=[DataRequired(), Email()])
    
    personal_country_code = StringField('Country Code', validators=[DataRequired()])
    personal_tel_no = StringField('Tel No.')
    personal_mobile_1 = StringField('Personal Mobile No. 1', validators=[DataRequired()])
    personal_mobile_2 = StringField('Personal Mobile No. 2')
    personal_mobile_3 = StringField('Personal Mobile No. 3')
    personal_email = StringField('Personal Email', validators=[DataRequired(), Email()])
    
    # Religion and Social Media
    religion = StringField('Religion', validators=[DataRequired()])
    facebook = StringField('Facebook')
    twitter = StringField('Twitter')
    
    # Educational Data
    school_level = StringField('School Level', validators=[DataRequired()])
    school_name = StringField('Name of School', validators=[DataRequired()])
    course = StringField('Course', validators=[DataRequired()])
    year_graduated = StringField('Year Graduated')
    last_school_attended = StringField('Last School Attended', validators=[DataRequired()])
    
    # Economic Data
    father_last_name = StringField("Father's Last Name", validators=[DataRequired()])
    father_first_name = StringField("Father's First Name", validators=[DataRequired()])
    father_middle_name = StringField("Father's Middle Name", validators=[DataRequired()])
    father_occupation = StringField("Father's Occupation", validators=[DataRequired()])
    father_contact_no = StringField("Father's Contact No.", validators=[DataRequired()])
    mother_last_name = StringField("Mother's Last Name", validators=[DataRequired()])
    mother_first_name = StringField("Mother's First Name", validators=[DataRequired()])
    mother_middle_name = StringField("Mother's Middle Name", validators=[DataRequired()])
    mother_occupation = StringField("Mother's Occupation", validators=[DataRequired()])
    mother_contact_no = StringField("Mother's Contact No.", validators=[DataRequired()])
    num_brothers = IntegerField('No. of Brothers', validators=[DataRequired()])
    num_sisters = IntegerField('No. of Sisters', validators=[DataRequired()])
    guardian_occupation = StringField('Guardian Occupation', validators=[DataRequired()])
    guardian_relationship = StringField('Guardian Relationship', validators=[DataRequired()])
    guardian_contact_no = StringField('Guardian Contact No.', validators=[DataRequired()])
    emergency_contact_name = StringField('Emergency Contact Name', validators=[DataRequired()])
    emergency_contact_relationship = StringField('Emergency Contact Relationship', validators=[DataRequired()])
    emergency_contact_no = StringField('Emergency Contact No.', validators=[DataRequired()])
    emergency_contact_address = StringField('Emergency Contact Address', validators=[DataRequired()])

class CourseForm(FlaskForm):
    abbreviation = StringField('Abbreviation', validators=[DataRequired()])
    title = StringField('Title Name', validators=[DataRequired()])
    school_year = StringField('School Year', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    Class = StringField('Class', validators=[DataRequired()])
    semesters = SelectField('Semesters', choices=[('1st Semester', '1st Semester'), ('2nd Semester', '2nd Semester')], validators=[DataRequired()])
    course_type = SelectField('Type', choices=[('SHS', 'SHS'), ('College', 'College')], validators=[DataRequired()])
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Create Course')

class SubjectForm(FlaskForm):
    abbreviation = StringField('Abbreviation', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    unit = IntegerField('Unit', validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    def set_course_choices(self, courses):
        self.course_id.choices = [(course.id, course.title) for course in courses]


    
class FilterForm(FlaskForm):
    school_year = StringField('School Year')
    semester = IntegerField('Semester')
    course_type = SelectField('Course Type', choices=[('', 'All'), ('shs', 'SHS'), ('college', 'College')])

class SectionForm(FlaskForm):
    name = StringField('Section Name', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    teacher_id = SelectField('Teacher', coerce=int, validators=[DataRequired()])

    def set_teacher_choices(self, teachers):
        self.teacher_id.choices = [(teacher.teacher_id, teacher.name) for teacher in teachers]


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
    year = IntegerField('Year', validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    pdf_file = FileField('PDF File', validators=[DataRequired()])

class EnrollmentForm(FlaskForm):
    student_id = SelectField('Student ID', validators=[DataRequired()])
    course_id = SelectField('Select Course', coerce=int)
    section_id = SelectField('Select Section', coerce=int)
    is_approved = BooleanField('Is Approved')
    submit = SubmitField('Enroll')

class EnrolliesForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    level = SelectField('Choose your level', choices=[('college', 'College'), ('senior_high', 'Senior High School')],
                        validators=[DataRequired()])
    address = StringField('Home Address', validators=[DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    place_of_birth = StringField('Place of Birth', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    nationality = StringField('Nationality', validators=[DataRequired()])
    religion = StringField('Religion', validators=[DataRequired()])
    previous_school_info = StringField('Previous School Information')
    grade_last_completed = StringField('Grade/Class Last Completed')
    academic_achievements = TextAreaField('Academic Achievements')
    proof_of_address = StringField('Proof of Address')
    parent_names = StringField('Names of Parents/Guardians', validators=[DataRequired()])
    parent_contact_info = StringField('Contact Information of Parents/Guardians', validators=[DataRequired()])
    parent_occupation = StringField('Occupation of Parents/Guardians', validators=[DataRequired()])
    medical_history = TextAreaField('Medical History', validators=[DataRequired()])
    immunization_records = TextAreaField('Immunization Records', validators=[DataRequired()])
    medical_certificate = FileField('Medical Certificate', validators=[DataRequired()])
    photos = FileField('Recent ID-size Photos')
    form_138 = FileField('Form 138 (Report Card) or Permanent Record')
    moral_character_certificate = FileField('Good Moral Character Certificate')
    special_needs = TextAreaField('Special Needs or Accommodations')

class GradeForm(FlaskForm):
    period_1 = StringField('Period 1', validators=[InputRequired()])
    period_2 = StringField('Period 2', validators=[InputRequired()])
    period_3 = StringField('Period 3', validators=[InputRequired()])
    final_grade = FloatField('Final Grade', render_kw={'readonly': True})
    is_passed = StringField('Status', render_kw={'readonly': True})

    submit = SubmitField('Submit')

class ScheduleForm(FlaskForm):
    day_of_week = StringField('Day of Week', validators=[InputRequired()])
    start_time = TimeField('Start Time', validators=[InputRequired()])
    end_time = TimeField('End Time', validators=[InputRequired()])
    submit = SubmitField('Add Schedule')