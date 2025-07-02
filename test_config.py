
import unittest
import os
from unittest.mock import patch
from config import Config

class TestConfig(unittest.TestCase):
    #@unittest.skip("DB_MYSQL is not being set, so config.py ends up calling load_dotenv() and these values are overwritten")
    def test_config_with_environment_variables(self):
        """Test configuration when environment variables are set."""
        with patch.dict(os.environ, {
            'FLASK_SECRET_KEY': 'test-secret',
            'DB_MYSQL': 'mysql://test:test@localhost/testdb'
        }):
            config = Config()
            #FIXME: the unittest.mock.patch os.environ is not available when Config() runs, so it is ignored
            self.assertEqual(config.SECRET_KEY, 'test-secret')
            self.assertEqual(config.SQLALCHEMY_DATABASE_URI, 'mysql://test:test@localhost/testdb')
            self.assertFalse(config.SQLALCHEMY_TRACK_MODIFICATIONS)

    def test_config_defaults(self):
        """Test configuration defaults."""
        with patch.dict(os.environ, {}, clear=True):
            config = Config()
            self.assertFalse(config.SQLALCHEMY_TRACK_MODIFICATIONS)
            self.assertIn('pool_recycle', config.SQLALCHEMY_ENGINE_OPTIONS)
            self.assertIn('pool_pre_ping', config.SQLALCHEMY_ENGINE_OPTIONS)

if __name__ == '__main__':
    unittest.main()
