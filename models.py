from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association tables for many-to-many relationships
parent_player = db.Table('parent_player',
    db.Column('parent_id', db.Integer, db.ForeignKey('parent.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)

team_player = db.Table('team_player',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)

team_coach = db.Table('team_coach',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True),
    db.Column('coach_id', db.Integer, db.ForeignKey('coach.id'), primary_key=True)
)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    jersey_number = db.Column(db.Integer, nullable=False)
    parents = db.relationship('Parent', secondary=parent_player, back_populates='players')
    teams = db.relationship('Team', secondary=team_player, back_populates='players')

class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    players = db.relationship('Player', secondary=parent_player, back_populates='parents')

class Coach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    teams = db.relationship('Team', secondary=team_coach, back_populates='coaches')

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamName = db.Column(db.String(100), nullable=False)
    season = db.Column(db.String(20), nullable=False)
    coaches = db.relationship('Coach', secondary=team_coach, back_populates='teams')
    players = db.relationship('Player', secondary=team_player, back_populates='teams')
