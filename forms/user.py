from wtforms import Form, StringField, PasswordField, BooleanField, validators

class RegisterForm(Form):
    email = StringField('Email Address', [
        validators.Length(min=6, max=35, message="Email must be between 6 and 35 characters"),
        validators.Email(message="Please enter a valid email address"),
        validators.DataRequired(message="Email is required")
    ])
    
    password = PasswordField('Password', [
        validators.Length(min=8, message="Password must be at least 8 characters"),
        validators.DataRequired(message="Password is required"),
        validators.Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', 
            message="Password must contain at least one lowercase letter, one uppercase letter, and one number"
        )
    ])
    
    confirm_password = PasswordField('Confirm Password', [
        validators.DataRequired(message="Please confirm your password"),
        validators.EqualTo('password', message="Passwords must match")
    ])
    
    
    
class LoginForm(Form):
    email = StringField('Email Address', [
        validators.Length(min=6, max=35, message="Email must be between 6 and 35 characters"),
        validators.Email(message="Please enter a valid email address"),
        validators.DataRequired(message="Email is required")
    ])
    
    password = PasswordField('Password', [
        validators.Length(min=8, message="Password must be at least 8 characters"),
        validators.DataRequired(message="Password is required"),
        validators.Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', 
            message="Password must contain at least one lowercase letter, one uppercase letter, and one number"
        )
    ])