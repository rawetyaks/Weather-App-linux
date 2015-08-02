# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
import codecs

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'auth_user'

    # User Name
    name    = db.Column(db.UnicodeText(128),  nullable=False)

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    password = db.Column(db.UnicodeText(192),  nullable=False)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, email, password):

        self.name     = name
        self.email    = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)

class TranslationStrings(Base):
    ___tablename__ = "translations"

    # id for unique weather effects
    super_id = db.Column(db.Text(128), nullable=True)

    # english label
    eng_label = db.Column(db.Text(128),  nullable=False)

    # tuscarora label
    tus_label = db.Column(db.Text(128),  nullable=True)

    def __init__(self, sid, eng_label, tus_label):
        self.super_id = sid
        self.eng_label = codecs.decode(eng_label, "utf-8")
        self.tus_label = codecs.decode(tus_label, "utf-8")

    def __repr__(self):
        utf8_eng_label = codecs.encode(self.eng_label, "utf-8")
        utf8_tus_label = codecs.encode(self.tus_label, "utf-8")
        return "[" + utf8_eng_label + ", " + utf8_tus_label + "]"