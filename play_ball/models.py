from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from itsdangerous.exc import SignatureExpired, BadTimeSignature

from flask_login import UserMixin
import enum
import os

db = SQLAlchemy()

# Association tables for many-to-many relationships
players_parents = db.Table('players_parents',
    db.Column('parents_id', db.Integer, db.ForeignKey('parents.id'), primary_key=True),
    db.Column('players_id', db.Integer, db.ForeignKey('players.id'), primary_key=True)
)

teams_players = db.Table('teams_players',
    db.Column('teams_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True),
    db.Column('players_id', db.Integer, db.ForeignKey('players.id'), primary_key=True)
)

teams_coaches = db.Table('teams_coaches',
    db.Column('teams_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True),
    db.Column('coaches_id', db.Integer, db.ForeignKey('coaches.id'), primary_key=True)
)

class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    jersey_number = db.Column(db.Integer, nullable=False)
    parents = db.relationship('Parents', secondary=players_parents, back_populates='players')
    teams = db.relationship('Teams', secondary=teams_players, back_populates='players')

class Users(db.Model, UserMixin):
	#one to one on coach, and one to one to parents
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30))
    #email will be the userid - not nullable
    email = db.Column(db.String(120), unique=True)
    passwd = db.Column(db.String(100), nullable=True)
    #
    # Foreign key to Address, allowing it to be nullable
    parent_id =  db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=True)
    # Define the relationship to Parent
    # uselist=False ensures a one-to-one relationship
    # back_populates links it to the 'user' attribute in Parents
    parent =  db.relationship("Parents", back_populates="user", uselist=False)
    #
    coach_id =  db.Column(db.Integer, db.ForeignKey('coaches.id'),  nullable=True)
    # uselist=False ensures a one-to-one relationship
    # back_populates links it to the 'user' attribute in Coaches
    coach =  db.relationship("Coaches", back_populates="user", uselist=False)

    def get_reset_token(self):
        print(f"Secrete is {current_app.config['SECRET_KEY'] }")
        # Generate a 16-byte (128-bit) random salt
        salt = os.urandom(16)
        s = Serializer(secret_key=current_app.config['SECRET_KEY'], salt=salt)
        return s.dumps({'user_id': self.email })

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            #3600 is one hour
            user_id = s.loads(token, max_age=3600)['user_id']
        except SignatureExpired:
            #This exception is raised if the token's timestamp indicates that it has exceeded the max_age.
            print("Token has expired on verify_reset_token.")
            return None
        except BadTimeSignature:
            #This exception is raised if the token's signature is invalid or if the token has been tampered with.
            print("Invalid or tampered token on verify_reset_token.")
            return None
        return User.query.get(user_id)

class Parents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Define the back_populates relationship to Users  1-to-1 - this is the nullable side
    user = db.relationship("Users", back_populates="parent", uselist=False)
    players = db.relationship('Players', secondary=players_parents, back_populates='parents')

class Coaches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Define the back_populates relationship to Users  1-to-1 - this is the nullable side
    user = db.relationship("Users", back_populates="coach", uselist=False)
    photo = db.Column(db.LargeBinary)
    thumbnail = db.Column(db.LargeBinary)
    teams = db.relationship('Teams', secondary=teams_coaches, back_populates='coaches')

class Seasons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_name = db.Column(db.String(100), nullable=False)
    base_date = db.Column(db.Date, nullable=False)
    
    teams = db.relationship('Teams', back_populates='season')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    #many-to-one on season uses the next two rows
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id')) # Foreign key
    season = db.relationship('Seasons', back_populates='teams')
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id')) # Foreign key
    level = db.relationship('Levels', back_populates='teams')
    coaches = db.relationship('Coaches', secondary=teams_coaches, back_populates='teams')
    players = db.relationship('Players', secondary=teams_players, back_populates='teams')

class Levels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String(100), nullable=False)
    target_age = db.Column(db.Integer, nullable=False)
    # Define a DECIMAL column for price with a total of 9 digits and 2 decimal places
    registration = db.Column(db.DECIMAL(9, 2), nullable=False)
    team_fee = db.Column(db.DECIMAL(9, 2), nullable=False)
    uniform = db.Column(db.DECIMAL(9, 2), nullable=False)
    
    teams = db.relationship('Teams', back_populates='level')

#For accounting
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
#    transactions = db.relationship('Transaction', backref='customer', lazy=True)

class Account_Types(enum.Enum):
    ASSET = 'asset'
    LIABILITY = 'liability'
    EQUITY = 'equity'
    REVENUE = 'revenue'
    EXPENSE ='expense'

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    account_type = db.Column(db.Enum(Account_Types, values_callable=lambda x: [e.value for e in x]), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def find_by_name(name):
        """Static method to find a User by name."""
        return Account.query.filter_by(name=name).first()

class Journal(db.Model):
    __tablename__ = 'journals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    allow_manual_entries = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def find_by_name(name):
        """Static method to find a User by name."""
        return Journal.query.filter_by(name=name).first()

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    #many-to-one to user this is the many side
    #Sales and charges are on coaches and parents, never on the players
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String(255), nullable=True)
    reference = db.Column(db.String(50), nullable=True)
    transaction_date = db.Column(db.Date, nullable=False)
    journal_id = db.Column(db.Integer, nullable=False) #, db.ForeignKey('journal.id')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    transaction = db.relationship('Transaction', backref='entries')
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    account = db.relationship('Account', backref='entries')
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    entry_type = db.Column(db.Enum('debit', 'credit'), nullable=False)
    memo = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Action_Types(enum.Enum):
    INSERT = 'insert'
    UPDATE = 'update'
    DELETE = 'delete'

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(100), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.Enum(), nullable=False)
    action = db.Column(db.Enum(Action_Types, values_callable=lambda x: [e.value for e in x]), nullable=False)
    user_id = db.Column(db.Integer)
    change_summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
