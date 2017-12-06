# test_todo_app.py
import unittest
import os
import json
from app import create_app, db

class TodoTestCase(unittest.TestCase):
    """This class represents the todo test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.todo = {'name': 'Go to Borabora for vacation'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        """This helper method helps register a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        """This helper method helps log in a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def test_todo_creation(self):
        """Test API can create a todo (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create a todo by making a POST request
        res = self.client().post(
            '/todos/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.todo)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to Borabora', str(res.data))


    def test_api_can_get_all_todos(self):
        """Test API can get a todo (GET request)."""
        res = self.client().post('/todos/', data=self.todo)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/todos/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_todo_by_id(self):
        """Test API can get a single todo by using it's id."""
        rv = self.client().post('/todos/', data=self.todo)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/todos/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Borabora', str(result.data))

    def test_todo_can_be_edited(self):
        """Test API can edit an existing todo. (PUT request)"""
        rv = self.client().post(
            '/todos/',
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/todos/1',
            data={
                "name": "Dont just eat, but also pray and love :-)"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/todos/1')
        self.assertIn('Dont just eat', str(results.data))

    def test_todos_deletion(self):
        """Test API can delete an existing todo. (DELETE request)."""
        rv = self.client().post(
            '/todos/',
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/todos/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/todos/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
