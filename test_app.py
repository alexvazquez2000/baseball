
import unittest
import os
import tempfile
import json
from unittest.mock import patch, MagicMock
from app import app, db
from models import Players, Parents, Coaches, Teams
from datetime import date
import io

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Clean up after each test method."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def login_user(self):
        """Helper method to simulate logged-in user."""
        with self.app.session_transaction() as sess:
            sess['access_token'] = 'fake_token'
            sess['auth_provider'] = 'google'

class TestModels(BaseTestCase):
    def test_player_creation(self):
        """Test creating a player."""
        player = Players(
            name="John Doe",
            date_of_birth=date(2010, 5, 15),
            jersey_number=42
        )
        db.session.add(player)
        db.session.commit()
        
        self.assertEqual(player.name, "John Doe")
        self.assertEqual(player.jersey_number, 42)
        self.assertEqual(Players.query.count(), 1)

    def test_parent_creation(self):
        """Test creating a parent."""
        parent = Parents(
            name="Jane Doe",
            email="jane@example.com",
            phone="555-1234"
        )
        db.session.add(parent)
        db.session.commit()
        
        self.assertEqual(parent.name, "Jane Doe")
        self.assertEqual(parent.email, "jane@example.com")
        self.assertEqual(Parents.query.count(), 1)

    def test_coach_creation(self):
        """Test creating a coach."""
        coach = Coaches(
            name="Coach Smith",
            email="coach@example.com",
            phone="555-5678"
        )
        db.session.add(coach)
        db.session.commit()
        
        self.assertEqual(coach.name, "Coach Smith")
        self.assertEqual(Coaches.query.count(), 1)

    def test_team_creation(self):
        """Test creating a team."""
        team = Teams(
            teamName="Rangers",
            season="2025-Spring"
        )
        db.session.add(team)
        db.session.commit()
        
        self.assertEqual(team.teamName, "Rangers")
        self.assertEqual(team.season, "2025-Spring")
        self.assertEqual(Teams.query.count(), 1)

    def test_player_parent_relationship(self):
        """Test many-to-many relationship between players and parents."""
        player = Players(
            name="John Doe",
            date_of_birth=date(2010, 5, 15),
            jersey_number=42
        )
        parent = Parents(
            name="Jane Doe",
            email="jane@example.com",
            phone="555-1234"
        )
        
        player.parents.append(parent)
        db.session.add(player)
        db.session.add(parent)
        db.session.commit()
        
        self.assertEqual(len(player.parents), 1)
        self.assertEqual(len(parent.players), 1)
        self.assertEqual(player.parents[0].name, "Jane Doe")

    def test_team_player_relationship(self):
        """Test many-to-many relationship between teams and players."""
        team = Teams(teamName="Rangers", season="2025-Spring")
        player = Players(
            name="John Doe",
            date_of_birth=date(2010, 5, 15),
            jersey_number=42
        )
        
        team.players.append(player)
        db.session.add(team)
        db.session.add(player)
        db.session.commit()
        
        self.assertEqual(len(team.players), 1)
        self.assertEqual(len(player.teams), 1)
        self.assertEqual(team.players[0].name, "John Doe")

class TestAuthentication(BaseTestCase):
    def test_login_page_access(self):
        """Test accessing login page without authentication."""
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_protected_route_redirect(self):
        """Test that protected routes redirect to login."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)

    def test_logout_clears_session(self):
        """Test that logout clears the session."""
        with self.app.session_transaction() as sess:
            sess['access_token'] = 'fake_token'
        
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)
        
        with self.app.session_transaction() as sess:
            self.assertNotIn('access_token', sess)

    @patch('app.get_user_info')
    def test_welcome_page_with_auth(self, mock_get_user_info):
        """Test welcome page with authenticated user."""
        mock_get_user_info.return_value = {
            'email': 'test@example.com',
            'name': 'Test User'
        }
        
        self.login_user()
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

class TestPlayerRoutes(BaseTestCase):
    def test_list_players_authenticated(self):
        """Test listing players when authenticated."""
        self.login_user()
        
        # Create test player
        player = Players(
            name="Test Player",
            date_of_birth=date(2010, 1, 1),
            jersey_number=1
        )
        db.session.add(player)
        db.session.commit()
        
        response = self.app.get('/players')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Player', response.data)

    def test_add_player(self):
        """Test adding a new player."""
        self.login_user()
        
        response = self.app.post('/player', data={
            'id': '',
            'name': 'New Player',
            'date_of_birth': '2010-01-01',
            'jersey_number': '99'
        })
        
        self.assertEqual(response.status_code, 302)
        player = Players.query.filter_by(name='New Player').first()
        self.assertIsNotNone(player)
        self.assertEqual(player.jersey_number, 99)

    def test_edit_player(self):
        """Test editing an existing player."""
        self.login_user()
        
        # Create test player
        player = Players(
            name="Original Name",
            date_of_birth=date(2010, 1, 1),
            jersey_number=1
        )
        db.session.add(player)
        db.session.commit()
        
        response = self.app.post('/player', data={
            'id': str(player.id),
            'name': 'Updated Name',
            'date_of_birth': '2010-01-01',
            'jersey_number': '2'
        })
        
        self.assertEqual(response.status_code, 302)
        updated_player = Players.query.get(player.id)
        self.assertEqual(updated_player.name, 'Updated Name')
        self.assertEqual(updated_player.jersey_number, 2)

class TestParentRoutes(BaseTestCase):
    def test_list_parents_authenticated(self):
        """Test listing parents when authenticated."""
        self.login_user()
        
        # Create test parent
        parent = Parents(
            name="Test Parent",
            email="test@example.com",
            phone="555-0000"
        )
        db.session.add(parent)
        db.session.commit()
        
        response = self.app.get('/parents')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Parent', response.data)

    def test_add_parent(self):
        """Test adding a new parent."""
        self.login_user()
        
        response = self.app.post('/parent/add', data={
            'name': 'New Parent',
            'email': 'new@example.com',
            'phone': '555-1111'
        })
        
        self.assertEqual(response.status_code, 302)
        parent = Parents.query.filter_by(name='New Parent').first()
        self.assertIsNotNone(parent)
        self.assertEqual(parent.email, 'new@example.com')

    def test_search_parents_ajax(self):
        """Test parent search functionality."""
        self.login_user()
        
        # Create test parents
        parent1 = Parents(name="John Smith", email="john@example.com", phone="555-0001")
        parent2 = Parents(name="Jane Doe", email="jane@example.com", phone="555-0002")
        db.session.add(parent1)
        db.session.add(parent2)
        db.session.commit()
        
        response = self.app.get('/parents/search?q=John')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'John Smith')

class TestCoachRoutes(BaseTestCase):
    def test_list_coaches_authenticated(self):
        """Test listing coaches when authenticated."""
        self.login_user()
        
        # Create test coach
        coach = Coaches(
            name="Test Coach",
            email="coach@example.com",
            phone="555-0000"
        )
        db.session.add(coach)
        db.session.commit()
        
        response = self.app.get('/coaches')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Coach', response.data)

    def test_add_coach(self):
        """Test adding a new coach."""
        self.login_user()
        
        response = self.app.post('/coach', data={
            'id': '',
            'name': 'New Coach',
            'email': 'newcoach@example.com',
            'phone': '555-2222'
        })
        
        self.assertEqual(response.status_code, 302)
        coach = Coaches.query.filter_by(name='New Coach').first()
        self.assertIsNotNone(coach)
        self.assertEqual(coach.email, 'newcoach@example.com')

    def test_add_coach_with_photo(self):
        """Test adding a coach with photo."""
        self.login_user()
        
        # Create fake image data
        fake_photo = io.BytesIO(b"fake image data")
        fake_photo.name = 'test.jpg'
        
        response = self.app.post('/coach', data={
            'id': '',
            'name': 'Coach with Photo',
            'email': 'photo@example.com',
            'phone': '555-3333',
            'photo': (fake_photo, 'test.jpg')
        }, content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 302)
        coach = Coaches.query.filter_by(name='Coach with Photo').first()
        self.assertIsNotNone(coach)
        self.assertIsNotNone(coach.photo)

class TestTeamRoutes(BaseTestCase):
    def test_list_teams_authenticated(self):
        """Test listing teams when authenticated."""
        self.login_user()
        
        # Create test team
        team = Teams(
            teamName="Test Team",
            season="2025-Spring"
        )
        db.session.add(team)
        db.session.commit()
        
        response = self.app.get('/teams')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Team', response.data)

class TestAjaxRoutes(BaseTestCase):
    def test_add_parent_ajax(self):
        """Test adding parent to player via AJAX."""
        self.login_user()
        
        # Create test data
        player = Players(
            name="Test Player",
            date_of_birth=date(2010, 1, 1),
            jersey_number=1
        )
        parent = Parents(
            name="Test Parent",
            email="test@example.com",
            phone="555-0000"
        )
        db.session.add(player)
        db.session.add(parent)
        db.session.commit()
        
        response = self.app.post(f'/player/{player.id}/add_parent_ajax',
                               json={'parent_id': parent.id},
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Verify relationship was created
        updated_player = Players.query.get(player.id)
        self.assertEqual(len(updated_player.parents), 1)

    def test_remove_parent_ajax(self):
        """Test removing parent from player via AJAX."""
        self.login_user()
        
        # Create test data with relationship
        player = Players(
            name="Test Player",
            date_of_birth=date(2010, 1, 1),
            jersey_number=1
        )
        parent = Parents(
            name="Test Parent",
            email="test@example.com",
            phone="555-0000"
        )
        player.parents.append(parent)
        db.session.add(player)
        db.session.add(parent)
        db.session.commit()
        
        response = self.app.post(f'/player/{player.id}/remove_parent_ajax',
                               json={'parent_id': parent.id},
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Verify relationship was removed
        updated_player = Players.query.get(player.id)
        self.assertEqual(len(updated_player.parents), 0)

class TestPDFGeneration(BaseTestCase):
    def test_generate_pdf(self):
        """Test PDF generation functionality."""
        self.login_user()
        
        response = self.app.get('/generate-pdf')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')

if __name__ == '__main__':
    unittest.main()
