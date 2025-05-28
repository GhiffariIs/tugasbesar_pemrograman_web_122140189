from pyramid import testing
import unittest
from aturmation_backend.models.user import User
from aturmation_backend.views.default import create_user, get_user, update_user, delete_user

class TestViews(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()
        self.user_data = {'username': 'testuser', 'password': 'testpass'}

    def tearDown(self):
        testing.tearDown()

    def test_create_user(self):
        response = create_user(self.request, self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created', response.json['message'])

    def test_get_user(self):
        user = User(username='testuser', password='testpass')
        user.save()  # Assuming a save method exists
        self.request.matchdict = {'user_id': user.id}
        response = get_user(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'testuser')

    def test_update_user(self):
        user = User(username='testuser', password='testpass')
        user.save()  # Assuming a save method exists
        self.request.matchdict = {'user_id': user.id}
        updated_data = {'username': 'updateduser'}
        response = update_user(self.request, updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('User updated', response.json['message'])

    def test_delete_user(self):
        user = User(username='testuser', password='testpass')
        user.save()  # Assuming a save method exists
        self.request.matchdict = {'user_id': user.id}
        response = delete_user(self.request)
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()