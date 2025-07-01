
import unittest
from flask import Flask
from forms import ParentForm, ChildForm, TeamForm
from models import db, Players

class TestForms(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.init_app(self.app)
        db.create_all()
        
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_parent_form_validation(self):
        """Test ParentForm validation."""
        with self.app.test_request_context():
            # Test valid form
            form = ParentForm(data={'name': 'Test Parent'})
            self.assertTrue(form.validate())
            
            # Test invalid form (missing name)
            form = ParentForm(data={'name': ''})
            self.assertFalse(form.validate())
            self.assertIn('This field is required.', form.name.errors)

    def test_child_form_validation(self):
        """Test ChildForm validation."""
        with self.app.test_request_context():
            # Test valid form
            form = ChildForm(data={'name': 'Test Child'})
            self.assertTrue(form.validate())
            
            # Test invalid form (missing name)
            form = ChildForm(data={'name': ''})
            self.assertFalse(form.validate())
            self.assertIn('This field is required.', form.name.errors)

    def test_team_form_validation(self):
        """Test TeamForm validation."""
        with self.app.test_request_context():
            # Test valid form
            form = TeamForm(data={'teamName': 'Test Team'})
            self.assertTrue(form.validate())
            
            # Test invalid form (missing team name)
            form = TeamForm(data={'teamName': ''})
            self.assertFalse(form.validate())
            self.assertIn('This field is required.', form.teamName.errors)

if __name__ == '__main__':
    unittest.main()
