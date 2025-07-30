from container import db, bcrypt

class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(length=30), nullable = False, unique = True)
    email_address = db.Column(db.String(length=50), nullable = False, unique = True)
    password_hash = db.Column(db.String(length=60), nullable = False)
    
    @property
    def password(self):
        raise AttributeError("Password is not readable!")


    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


    def check_password_correction(self, password_to_check):
        return bcrypt.check_password_hash(self.password_hash, password_to_check)
