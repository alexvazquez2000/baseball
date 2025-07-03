from flask_sqlalchemy import SQLAlchemy

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
    name = db.Column(db.String(64), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    jersey_number = db.Column(db.Integer, nullable=False)
    parents = db.relationship('Parents', secondary=players_parents, back_populates='players')
    teams = db.relationship('Teams', secondary=teams_players, back_populates='players')

class Parents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    players = db.relationship('Players', secondary=players_parents, back_populates='parents')

class Coaches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    photo = db.Column(db.LargeBinary)
    thumbnail = db.Column(db.LargeBinary)
    teams = db.relationship('Teams', secondary=teams_coaches, back_populates='coaches')

class Seasons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_name = db.Column(db.String(100), nullable=False)
    base_date = db.Column(db.Date, nullable=False)
    teams = db.relationship('Teams', back_populates='season')

class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamName = db.Column(db.String(100), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id')) # Foreign key
    season = db.relationship('Seasons', back_populates='teams')
    coaches = db.relationship('Coaches', secondary=teams_coaches, back_populates='teams')
    players = db.relationship('Players', secondary=teams_players, back_populates='teams')
