import unittest
from app import app  # Assuming `app` is your Flask app instance

class FlaskAppTests(unittest.TestCase):

    def test_home_page(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
