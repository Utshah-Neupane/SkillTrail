from container import app, db
from container.models import User

with app.app_context():

    if not User.query.filter_by(username = "Admin").first():
        u1 = User(username = "Admin",
            password_hash = '123456',
            email_address = 'admin@gmail.com')
        
        db.session.add(u1)
    
    db.session.commit()


    # user1 = User.query.filter_by(username = "Admin").first()

    # print(user1.email_address)