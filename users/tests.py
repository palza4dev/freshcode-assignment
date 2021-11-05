import json, bcrypt, jwt

from django.test  import TestCase, Client

from users.models import User

class SigninTest(TestCase):
    def setUp(self):
        password = 'abc1234!'
        User.objects.create(
            id           = 1,
            email        = 'user1@gmail.com',
            password     = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            role         = 'admin'
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signinview_post_success(self):
        client = Client()
        
        user = {
            'email'    : 'user1@gmail.com',
            'password' : 'abc1234!',
            'role'     : 'admin'
        }
        response     = client.post('/users/signin', json.dumps(user), content_type='application/json')
        access_token = response.json()['access_token']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'access_token' : access_token
            }
        )

    def test_signinview_post_invalid_email(self):
        client = Client()
        
        user = {
            'email'    : 'user2@gmail.com',
            'password' : 'abc1234!',
            'role'     : 'admin'
        }
        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 
            {
                'message' : 'INVALID_EMAIL'
            }
        )
    
    def test_signinview_post_invalid_password(self):
        client = Client()
        
        user = {
            'email'    : 'user1@gmail.com',
            'password' : 'abc1234@',
            'role'     : 'admin'
        }
        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 
            {
                'message' : 'INVALID_PASSWORD'
            }
        )

    def test_signinview_post_key_error_email(self):
        client = Client()
        
        user = {
            'password' : 'abc1234!',
            'role'     : 'admin'
        }
        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message' : 'KEY_ERROR'
            }
        )

    def test_signinview_post_key_error_password(self):
        client = Client()
        
        user = {
             'email' : 'user1@gmail.com',
             'role'  : 'admin'
        }
        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message' : 'KEY_ERROR'
            }
        )

    def test_signinview_post_jsondecod_error(self):
        client = Client()

        response = client.post('/users/signin')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message' : 'JSON_DECODE_ERROR'
            }
        )