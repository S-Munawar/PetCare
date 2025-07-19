from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from petcare import mongo
from flask_login import current_user
from datetime import date
from bson.objectid import ObjectId

# --- A comprehensive list of country codes ---
country_codes = [
    ('+91', 'India (+91)'),
    ('+1', 'United States (+1)'),
    ('+44', 'United Kingdom (+44)'),
    ('+971', 'United Arab Emirates (+971)'),
    ('+93', 'Afghanistan (+93)'),
    ('+355', 'Albania (+355)'),
    ('+213', 'Algeria (+213)'),
    ('+376', 'Andorra (+376)'),
    ('+244', 'Angola (+244)'),
    ('+54', 'Argentina (+54)'),
    ('+374', 'Armenia (+374)'),
    ('+61', 'Australia (+61)'),
    ('+43', 'Austria (+43)'),
    ('+994', 'Azerbaijan (+994)'),
    ('+973', 'Bahrain (+973)'),
    ('+880', 'Bangladesh (+880)'),
    ('+375', 'Belarus (+375)'),
    ('+32', 'Belgium (+32)'),
    ('+501', 'Belize (+501)'),
    ('+229', 'Benin (+229)'),
    ('+975', 'Bhutan (+975)'),
    ('+591', 'Bolivia (+591)'),
    ('+387', 'Bosnia and Herzegovina (+387)'),
    ('+267', 'Botswana (+267)'),
    ('+55', 'Brazil (+55)'),
    ('+673', 'Brunei (+673)'),
    ('+359', 'Bulgaria (+359)'),
    ('+226', 'Burkina Faso (+226)'),
    ('+257', 'Burundi (+257)'),
    ('+855', 'Cambodia (+855)'),
    ('+237', 'Cameroon (+237)'),
    ('+238', 'Cape Verde (+238)'),
    ('+236', 'Central African Republic (+236)'),
    ('+235', 'Chad (+235)'),
    ('+56', 'Chile (+56)'),
    ('+86', 'China (+86)'),
    ('+57', 'Colombia (+57)'),
    ('+269', 'Comoros (+269)'),
    ('+242', 'Congo (+242)'),
    ('+682', 'Cook Islands (+682)'),
    ('+506', 'Costa Rica (+506)'),
    ('+385', 'Croatia (+385)'),
    ('+53', 'Cuba (+53)'),
    ('+357', 'Cyprus (+357)'),
    ('+420', 'Czech Republic (+420)'),
    ('+45', 'Denmark (+45)'),
    ('+253', 'Djibouti (+253)'),
    ('+1-767', 'Dominica (+1-767)'),
    ('+1-809', 'Dominican Republic (+1-809)'),
    ('+593', 'Ecuador (+593)'),
    ('+20', 'Egypt (+20)'),
    ('+503', 'El Salvador (+503)'),
    ('+240', 'Equatorial Guinea (+240)'),
    ('+291', 'Eritrea (+291)'),
    ('+372', 'Estonia (+372)'),
    ('+251', 'Ethiopia (+251)'),
    ('+679', 'Fiji (+679)'),
    ('+358', 'Finland (+358)'),
    ('+33', 'France (+33)'),
    ('+241', 'Gabon (+241)'),
    ('+220', 'Gambia (+220)'),
    ('+995', 'Georgia (+995)'),
    ('+49', 'Germany (+49)'),
    ('+233', 'Ghana (+233)'),
    ('+30', 'Greece (+30)'),
    ('+299', 'Greenland (+299)'),
    ('+1-473', 'Grenada (+1-473)'),
    ('+502', 'Guatemala (+502)'),
    ('+224', 'Guinea (+224)'),
    ('+245', 'Guinea-Bissau (+245)'),
    ('+592', 'Guyana (+592)'),
    ('+509', 'Haiti (+509)'),
    ('+504', 'Honduras (+504)'),
    ('+852', 'Hong Kong (+852)'),
    ('+36', 'Hungary (+36)'),
    ('+354', 'Iceland (+354)'),
    ('+62', 'Indonesia (+62)'),
    ('+98', 'Iran (+98)'),
    ('+964', 'Iraq (+964)'),
    ('+353', 'Ireland (+353)'),
    ('+972', 'Israel (+972)'),
    ('+39', 'Italy (+39)'),
    ('+225', 'Ivory Coast (+225)'),
    ('+1-876', 'Jamaica (+1-876)'),
    ('+81', 'Japan (+81)'),
    ('+962', 'Jordan (+962)'),
    ('+7', 'Kazakhstan (+7)'),
    ('+254', 'Kenya (+254)'),
    ('+686', 'Kiribati (+686)'),
    ('+965', 'Kuwait (+965)'),
    ('+996', 'Kyrgyzstan (+996)'),
    ('+856', 'Laos (+856)'),
    ('+371', 'Latvia (+371)'),
    ('+961', 'Lebanon (+961)'),
    ('+266', 'Lesotho (+266)'),
    ('+231', 'Liberia (+231)'),
    ('+218', 'Libya (+218)'),
    ('+423', 'Liechtenstein (+423)'),
    ('+370', 'Lithuania (+370)'),
    ('+352', 'Luxembourg (+352)'),
    ('+853', 'Macau (+853)'),
    ('+389', 'Macedonia (+389)'),
    ('+261', 'Madagascar (+261)'),
    ('+265', 'Malawi (+265)'),
    ('+60', 'Malaysia (+60)'),
    ('+960', 'Maldives (+960)'),
    ('+223', 'Mali (+223)'),
    ('+356', 'Malta (+356)'),
    ('+692', 'Marshall Islands (+692)'),
    ('+222', 'Mauritania (+222)'),
    ('+230', 'Mauritius (+230)'),
    ('+52', 'Mexico (+52)'),
    ('+691', 'Micronesia (+691)'),
    ('+373', 'Moldova (+373)'),
    ('+377', 'Monaco (+377)'),
    ('+976', 'Mongolia (+976)'),
    ('+382', 'Montenegro (+382)'),
    ('+212', 'Morocco (+212)'),
    ('+258', 'Mozambique (+258)'),
    ('+95', 'Myanmar (+95)'),
    ('+264', 'Namibia (+264)'),
    ('+674', 'Nauru (+674)'),
    ('+977', 'Nepal (+977)'),
    ('+31', 'Netherlands (+31)'),
    ('+64', 'New Zealand (+64)'),
    ('+505', 'Nicaragua (+505)'),
    ('+227', 'Niger (+227)'),
    ('+234', 'Nigeria (+234)'),
    ('+850', 'North Korea (+850)'),
    ('+47', 'Norway (+47)'),
    ('+968', 'Oman (+968)'),
    ('+92', 'Pakistan (+92)'),
    ('+680', 'Palau (+680)'),
    ('+507', 'Panama (+507)'),
    ('+675', 'Papua New Guinea (+675)'),
    ('+595', 'Paraguay (+595)'),
    ('+51', 'Peru (+51)'),
    ('+63', 'Philippines (+63)'),
    ('+48', 'Poland (+48)'),
    ('+351', 'Portugal (+351)'),
    ('+1-787', 'Puerto Rico (+1-787)'),
    ('+974', 'Qatar (+974)'),
    ('+40', 'Romania (+40)'),
    ('+7', 'Russia (+7)'),
    ('+250', 'Rwanda (+250)'),
    ('+685', 'Samoa (+685)'),
    ('+378', 'San Marino (+378)'),
    ('+239', 'Sao Tome and Principe (+239)'),
    ('+966', 'Saudi Arabia (+966)'),
    ('+221', 'Senegal (+221)'),
    ('+381', 'Serbia (+381)'),
    ('+248', 'Seychelles (+248)'),
    ('+232', 'Sierra Leone (+232)'),
    ('+65', 'Singapore (+65)'),
    ('+421', 'Slovakia (+421)'),
    ('+386', 'Slovenia (+386)'),
    ('+677', 'Solomon Islands (+677)'),
    ('+252', 'Somalia (+252)'),
    ('+27', 'South Africa (+27)'),
    ('+82', 'South Korea (+82)'),
    ('+211', 'South Sudan (+211)'),
    ('+34', 'Spain (+34)'),
    ('+94', 'Sri Lanka (+94)'),
    ('+249', 'Sudan (+249)'),
    ('+597', 'Suriname (+597)'),
    ('+268', 'Swaziland (+268)'),
    ('+46', 'Sweden (+46)'),
    ('+41', 'Switzerland (+41)'),
    ('+963', 'Syria (+963)'),
    ('+886', 'Taiwan (+886)'),
    ('+992', 'Tajikistan (+992)'),
    ('+255', 'Tanzania (+255)'),
    ('+66', 'Thailand (+66)'),
    ('+670', 'Timor-Leste (+670)'),
    ('+228', 'Togo (+228)'),
    ('+676', 'Tonga (+676)'),
    ('+1-868', 'Trinidad and Tobago (+1-868)'),
    ('+216', 'Tunisia (+216)'),
    ('+90', 'Turkey (+90)'),
    ('+993', 'Turkmenistan (+993)'),
    ('+688', 'Tuvalu (+688)'),
    ('+256', 'Uganda (+256)'),
    ('+380', 'Ukraine (+380)'),
    ('+598', 'Uruguay (+598)'),
    ('+998', 'Uzbekistan (+998)'),
    ('+678', 'Vanuatu (+678)'),
    ('+58', 'Venezuela (+58)'),
    ('+84', 'Vietnam (+84)'),
    ('+967', 'Yemen (+967)'),
    ('+260', 'Zambia (+260)'),
    ('+263', 'Zimbabwe (+263)'),
]

# --- Registration Forms ---

class RegistrationForm(FlaskForm):
    """Base registration form for standard users."""
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email("This field requires a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    country_code = SelectField('Country Code', choices=country_codes, validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=8, max=15)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=200)])
    submit = SubmitField('Register')

    def validate_username(self, username_to_check):
        if mongo.db.users.find_one({"username": username_to_check.data.title()}):
            raise ValidationError('Username already registered!')

    def validate_email(self, email_to_check):
        if mongo.db.users.find_one({"email": email_to_check.data.lower()}):
            raise ValidationError('Email address already registered!')

class VetRegistrationForm(RegistrationForm):
    """Specific registration form for Vets, inheriting from the base form."""
    vet_license = StringField('Vet License', validators=[DataRequired(), Length(min=10, max=10)])
    qualification = StringField('Highest Qualification', validators=[DataRequired(), Length(min=2, max=50)])

    def validate_vet_license(self, vet_license_to_check):
        if mongo.db.users.find_one({"vet_license": vet_license_to_check.data}):
            raise ValidationError('Vet License already registered!')
        if not mongo.db.vetlicenses.find_one({"vet_license": vet_license_to_check.data}):
            raise ValidationError('This Vet License is not valid!')

# --- Login Forms ---

class LoginForm(FlaskForm):
    """Login form for Pet Owners and Admins."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class VetLoginForm(FlaskForm):
    """Dedicated login form for Vets requiring a license."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    vet_license = StringField('Vet License', validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Login as Veterinarian')

# --- Profile Completion & Editing Forms ---

class CompleteUserRegistrationForm(FlaskForm):
    """Form for a new Google user to complete their pet owner profile."""
    country_code = SelectField('Country Code', choices=country_codes, validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=8, max=15)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=200)])
    submit = SubmitField('Complete Profile')

class CompleteVetRegistrationForm(FlaskForm):
    """Form for a new Google user to complete their vet profile."""
    vet_license = StringField('Vet License', validators=[DataRequired(), Length(min=10, max=10)])
    qualification = StringField('Highest Qualification', validators=[DataRequired(), Length(min=2, max=50)])
    country_code = SelectField('Country Code', choices=country_codes, validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=8, max=15)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=200)])
    submit = SubmitField('Complete Registration')

    def validate_vet_license(self, vet_license_to_check):
        existing_vet = mongo.db.users.find_one({"vet_license": vet_license_to_check.data})
        if existing_vet and existing_vet['_id'] != ObjectId(current_user.id):
            raise ValidationError('Vet License already registered to another user!')
        if not mongo.db.vetlicenses.find_one({"vet_license": vet_license_to_check.data}):
            raise ValidationError('This Vet License is not valid! Please contact an admin.')

class EditProfileForm(FlaskForm):
    """A single form to handle profile edits for both Users and Vets."""
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', render_kw={'readonly': True})
    country_code = SelectField('Country Code', choices=country_codes, validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=8, max=15, message="Phone number must be between 8 and 15 digits.")])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=200)])
    qualification = StringField('Highest Qualification (for Vets)', validators=[Length(max=50)])
    password = PasswordField('New Password (optional)')
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Update Profile')

    def validate_username(self, username_to_check):
        if username_to_check.data.title() != current_user.username:
            if mongo.db.users.find_one({"username": username_to_check.data.title()}):
                raise ValidationError('That username is taken. Please choose a different one.')

# --- Data Management Forms (Pets & Vets) ---

class AddPet(FlaskForm):
    """Form to add a new pet."""
    dog_breeds = [("Labrador Retriever", "Labrador Retriever"), ("German Shepherd", "German Shepherd"), ("Golden Retriever", "Golden Retriever"), ("Bulldog", "Bulldog"), ("Poodle", "Poodle"), ("Beagle", "Beagle"), ("Other", "Other")]
    cat_breeds = [("Domestic Shorthair", "Domestic Shorthair"), ("Siamese", "Siamese"), ("Persian", "Persian"), ("Maine Coon", "Maine Coon"), ("Bengal", "Bengal"), ("Sphynx", "Sphynx"), ("Other", "Other")]
    horse_breeds = [("Thoroughbred", "Thoroughbred"), ("Quarter Horse", "Quarter Horse"), ("Arabian", "Arabian"), ("Paint Horse", "Paint Horse"), ("Appaloosa", "Appaloosa"), ("Morgan", "Morgan"), ("Other", "Other")]

    pet_name = StringField('Pet Name', validators=[DataRequired()])
    pet_species = SelectField('Pet Species', choices=[("Dog", "Dog"), ("Cat", "Cat"), ("Horse", "Horse")], validators=[DataRequired()])
    pet_breed = SelectField('Breed', choices=[], validators=[DataRequired()])
    pet_gender = SelectField("Pet Gender", choices=[("Male", "Male"), ("Female", "Female")], validators=[DataRequired()])
    pet_dob = DateField('Date of Birth', validators=[DataRequired()])
    submit = SubmitField('Add Pet')

class AddVet(FlaskForm):
    """Form for an Admin to add a new Vet License."""
    vet_license = StringField('Vet Licence', validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Add Vet')