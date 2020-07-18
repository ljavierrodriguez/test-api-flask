from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    profile = db.relationship("Profile", backref="test", uselist=False)

    def save(self):
        db.session.add(self) # INSERT INTO
        db.session.commit()

    def update(self):
        db.session.commit() # UPDATE 

    def delete(self):
        db.session.delete(self) # DELETE FROM
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "profile": self.profile.serialize()
        }



class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(300), default="")
    facebook = db.Column(db.String(100), default="") 
    twitter = db.Column(db.String(100), default="")
    test_id = db.Column(db.Integer, db.ForeignKey("tests.id"), nullable=False)

    def save(self):
        db.session.add(self) # INSERT INTO
        db.session.commit()

    def update(self):
        db.session.commit() # UPDATE 

    def delete(self):
        db.session.delete(self) # DELETE FROM
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "bio": self.bio,
            "facebook": self.facebook,
            "twitter": self.twitter
        }