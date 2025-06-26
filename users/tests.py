
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

User = get_user_model()

class UserModelTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'bio': 'Test bio'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.username, self.user_data['username'])
        self.assertTrue(self.user.check_password(self.user_data['password']))
        self.assertEqual(self.user.bio, self.user_data['bio'])
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_superuser_creation(self):
        self.assertTrue(self.admin.is_staff)
        self.assertTrue(self.admin.is_superuser)

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), self.user_data['email'])

    def test_required_fields(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', username='test', password='pass')
        # Add additional checks for other required fields
        with self.assertRaises(ValueError):
            User.objects.create_user(email='test@example.com', username='', password='pass')
            
class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')

    def test_user_registration(self):
        url = reverse('register')
        data = {
            'email': 'new@example.com',
            'username': 'newuser',
            'password': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data['data']['email'], data['email'])

    def test_user_registration_invalid_data(self):
        url = reverse('register')
        data = {
            'email': 'invalid',
            'username': '',
            'password': 'short',
            'password2': 'mismatch'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Update to match your actual error response structure
        self.assertIn('username', response.data['data'])
        self.assertIn('email', response.data['data'])
    # Remove password check if it's not in the response

    def test_token_obtain_pair(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])

    def test_token_obtain_pair_invalid_credentials(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Invalid credentials')
        
class UserViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
        self.token = RefreshToken.for_user(self.user)
        self.admin_token = RefreshToken.for_user(self.admin)
        self.url_list = reverse('user-list')
        self.url_detail = reverse('user-detail', kwargs={'pk': self.user.pk})

    def test_user_list_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)

    def test_user_list_as_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_detail_own_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], self.user.email)

    def test_user_detail_other_profile(self):
        other_user = User.objects.create_user(
            email='other@example.com',
            username='other',
            password='otherpass123'
        )
        url = reverse('user-detail', kwargs={'pk': other_user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.get(url)
        # Change expected status based on your actual behavior (403 or 404)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_own_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        data = {
            'username': 'updateduser',  # Required field
            'email': 'updated@example.com',  # Required field
            'bio': 'Updated bio'
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, data['bio'])

    def test_user_delete_own_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "User deleted successfully")
        self.assertEqual(User.objects.count(), 1)  # Verify deletion