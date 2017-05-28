from todo_api.app import app
from todo_api.models import User, Todo

from peewee import *

import unittest
import os
from playhouse.test_utils import test_database

test_db = SqliteDatabase(':memory:')
test_db.connect()
test_db.create_tables([User, Todo], safe=True)

testuser_data = {
    'username': 'testuser',
    'email': 'test@gmail.com',
    'password': 'testpassword',
    'verify_password': 'testpassword'
}

testuser2_data = {
    'username': 'testuser2',
    'email': 'test2@gmail.com',
    'password': 'test2password',
    'verify_password': 'test2password'
}

testuser3_data = {
    'username': 'testuser2',
    'email': 'test2@gmail.com',
    'password': 'test2password',
    'verify_password': 'y'
}

testuser4_data = {
    'username': 'testuser4',
    'email': 'test@gmail.com',
    'password': 'test2password',
    'verify_password': 'y'
}

testuser5_data = {
    'username': 'testuser',
    'email': 'test5@gmail.com',
    'password': 'test2password',
    'verify_password': 'y'
}

todo1_data = {
    'name': 'do the dishes',
}

todo2_data = {
    'name': 'feed the cat',
    'completed': True
}


class TestWithData(unittest.TestCase):
    def create_user_data(self):
        self.user = User.create_user(**testuser_data)

    def create_todo_data(self):
        self.todo1 = Todo.create(**todo1_data)
        self.todo2 = Todo.create(**todo2_data)

    def create_auth_user_data(self):
        self.user = User.create_user(**testuser_data)
        self.user = User.select().get()
        token = self.user.generate_auth_token()
        token_decode = token.decode('ascii')
        self.auth_header = {
            'Authorization': 'Token ' + token_decode
        }


class TestUserApi(TestWithData):
    """
    tests the string output for employees and
    also how to guess the employee from a name
    """
    def run(self, result=None):
        with test_database(test_db, (User, Todo)):
            super(TestUserApi, self).run(result)

    def setUp(self):
        """
        testdata is created
        and an employee is set up for the first test
        """
        self.create_user_data()
        self.user = User.select().get()
        self.tester = app.test_client(self)

    def test_resource_users_get(self):
        resp = self.tester.get('/api/v1/users',
                                content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn( '"username": "testuser"', resp.get_data(as_text=True))

    def test_resource_users_post(self):
        resp = self.tester.post('/api/v1/users',
                                data=testuser2_data)
        self.assertEqual(resp.status_code, 201)
        self.assertIn( '"username": "testuser2"', resp.get_data(as_text=True))

    def test_resource_users_post_verify_password_notvalid(self):
        resp = self.tester.post('/api/v1/users',
                                data=testuser3_data)
        self.assertEqual(resp.status_code, 400)

    def test_resource_users_post_double_email_notvalid(self):
        resp = self.tester.post('/api/v1/users',
                                data=testuser4_data)
        self.assertEqual(resp.status_code, 400)

    def test_resource_users_post_double_username_notvalid(self):
        resp = self.tester.post('/api/v1/users',
                                data=testuser5_data)
        self.assertEqual(resp.status_code, 400)

    def test_user_login(self):
        resp = self.tester.post('/api/v1/login',
                                data={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', resp.get_data(as_text=True))

    def test_user_login_password_not_valid(self):
        resp = self.tester.post('/api/v1/login',
                                data={'username': 'testuser', 'password': 'y'})
        self.assertEqual(resp.status_code, 400)

    def test_user_login_username_not_valid(self):
        resp = self.tester.post('/api/v1/login',
                                data={'username': 'x', 'password': 'y'})
        self.assertEqual(resp.status_code, 400)



class TestTodoApi(TestWithData):
    """
    tests the string output for employees and
    also how to guess the employee from a name
    """
    def run(self, result=None):
        with test_database(test_db, (User, Todo)):
            super(TestTodoApi, self).run(result)

    def setUp(self):
        """
        testdata is created
        and an employee is set up for the first test
        """
        self.create_auth_user_data()
        self.create_todo_data()
        self.tester = app.test_client(self)

    def test_resource_todos_get(self):
        resp = self.tester.get(
            '/api/v1/todos',
            headers=self.auth_header)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.todo1.name, resp.get_data(as_text=True))
        self.assertIn(self.todo2.name, resp.get_data(as_text=True))

    def test_resource_todos_get_unauthorized(self):
        resp = self.tester.get(
            '/api/v1/todos')
        self.assertEqual(resp.status_code, 401)

    def test_resource_todos_post(self):
        resp = self.tester.post(
            '/api/v1/todos',
            headers=self.auth_header,
            data={'name': 'some new task'})
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Todo.select().where(Todo.name == 'some new task').count(), 1)

    def test_resource_todos_post_unauthorized(self):
        resp = self.tester.post(
            '/api/v1/todos',
            data=todo1_data)
        self.assertEqual(resp.status_code, 401)

    def test_resource_todo_get(self):
        resp = self.tester.get(
            '/api/v1/todos/' + str(self.todo2.id),
            headers=self.auth_header)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.todo2.name, resp.get_data(as_text=True))

    def test_resource_todo_get_unauthorized(self):
        resp = self.tester.get(
            '/api/v1/todos/' + str(self.todo1.id))
        self.assertEqual(resp.status_code, 401)

    def test_resource_todo_get_404(self):
        resp = self.tester.get(
            '/api/v1/todos/' + '8',
            headers=self.auth_header)
        self.assertEqual(resp.status_code, 404)

    def test_resource_todo_delete(self):
        resp = self.tester.delete(
            '/api/v1/todos/' + str(self.todo2.id),
            headers=self.auth_header)
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Todo.select().where(Todo.id == self.todo2.id).count(), 0)

    def test_resource_todo_delete_unauthorized(self):
        resp = self.tester.delete(
            '/api/v1/todos/' + str(self.todo1.id))
        self.assertEqual(resp.status_code, 401)

    def test_resource_todo_put(self):
        resp = self.tester.put(
            '/api/v1/todos/' + str(self.todo1.id),
            headers=self.auth_header,
            data={'name': 'something else'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Todo.get(Todo.id == self.todo1.id).name, 'something else')

    def test_resource_todo_put_unauthorized(self):
        resp = self.tester.put(
            '/api/v1/todos/' + str(self.todo1.id),
            data={'name': 'something else'})
        self.assertEqual(resp.status_code, 401)


class BasicTest(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_welcome(self):
        response = self.tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_initialize(self):
        initialize()
        tester = os.path.exists("todos.sqlite")
        self.assertTrue(tester)


class QueryTest(unittest.TestCase):
    def test_get_todo_or_404(self):
        pass


if __name__ == '__main__':
    unittest.main()