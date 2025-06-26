
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from .models import Task

class TaskModelTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test description',
            'status': 'todo',
            'user': self.user
        }
        self.task = Task.objects.create(**self.task_data)

    def test_task_creation(self):
        self.assertEqual(self.task.title, self.task_data['title'])
        self.assertEqual(self.task.description, self.task_data['description'])
        self.assertEqual(self.task.status, self.task_data['status'])
        self.assertEqual(self.task.user, self.user)
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)

    def test_task_str_representation(self):
        self.assertEqual(str(self.task), self.task_data['title'])

    def test_task_status_choices(self):
        valid_statuses = [choice[0] for choice in Task.Status.choices]
        self.assertIn(self.task.status, valid_statuses)

class TaskViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='otherpass123'
        )
        self.token = RefreshToken.for_user(self.user)
        self.other_token = RefreshToken.for_user(self.other_user)
        
        self.task = Task.objects.create(
            title='Test Task',
            description='Test description',
            status='todo',
            user=self.user
        )
        self.other_task = Task.objects.create(
            title='Other Task',
            description='Other description',
            status='in_progress',
            user=self.other_user
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        self.url_list = reverse('task-list')
        self.url_detail = reverse('task-detail', kwargs={'pk': self.task.pk})
        self.url_other_detail = reverse('task-detail', kwargs={'pk': self.other_task.pk})

    def test_task_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['title'], self.task.title)

    def test_task_list_filtering(self):
        # Test status filter
        response = self.client.get(self.url_list, {'status': 'todo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        
        # Test search filter
        response = self.client.get(self.url_list, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        
        # Test no results
        response = self.client.get(self.url_list, {'status': 'done'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 0)

    def test_task_create(self):
        data = {
            'title': 'New Task',
            'description': 'New description',
            'status': 'in_progress'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(response.data['data']['title'], data['title'])
        self.assertEqual(response.data['data']['user'], self.user.id)

    def test_task_create_invalid_data(self):
        data = {
            'title': '',
            'status': 'invalid_status'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data['data'])
        self.assertIn('status', response.data['data'])

    def test_task_detail(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['title'], self.task.title)

    def test_task_detail_unauthorized(self):
        response = self.client.get(self.url_other_detail)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_update(self):
        data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'status': 'in_progress'
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, data['title'])
        self.assertEqual(self.task.status, data['status'])

    def test_task_partial_update(self):
        data = {'status': 'done'}
        response = self.client.patch(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, data['status'])


def test_task_detail_unauthorized(self):
    """Should return 403 when accessing another user's task"""
    response = self.client.get(self.url_other_detail)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

def test_task_update_unauthorized(self):
    """Should return 403 when updating another user's task"""
    data = {'title': 'Unauthorized Update'}
    response = self.client.put(self.url_other_detail, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

def test_task_delete_unauthorized(self):
    """Should return 403 when deleting another user's task"""
    response = self.client.delete(self.url_other_detail)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    