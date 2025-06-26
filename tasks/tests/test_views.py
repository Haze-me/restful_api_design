
# import pytest
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
# from tasks.models import Task
# from users.models import User
# import json
# from datetime import datetime, timedelta

# @pytest.fixture
# def api_client():
#     return APIClient()

# @pytest.fixture
# def test_user():
#     return User.objects.create_user(
#         username='testuser',
#         email='test@example.com',
#         password='testpass123'
#     )

# @pytest.fixture
# def test_task(test_user):
#     return Task.objects.create(
#         title='Test Task',
#         description='Test Description',
#         status='todo',
#         user=test_user
#     )

# @pytest.mark.django_db
# class TestTaskViews:
#     def test_task_list_authenticated(self, api_client, test_user, test_task):
#         api_client.force_authenticate(user=test_user)
#         url = reverse('task-list')
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data['data']) == 1
#         assert response.data['data'][0]['title'] == test_task.title

#     def test_task_list_unauthenticated(self, api_client):
#         url = reverse('task-list')
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_create_task(self, api_client, test_user):
#         api_client.force_authenticate(user=test_user)
#         url = reverse('task-list')
#         due_date = (datetime.now() + timedelta(days=1)).isoformat()
#         data = {
#             'title': 'New Task',
#             'description': 'New Description',
#             'status': 'todo',
#             'due_date': due_date
#         }
#         response = api_client.post(url, data, format='json')
#         assert response.status_code == status.HTTP_201_CREATED
#         assert Task.objects.count() == 1
#         assert Task.objects.first().title == 'New Task'

#     def test_create_task_invalid_due_date(self, api_client, test_user):
#         api_client.force_authenticate(user=test_user)
#         url = reverse('task-list')
#         due_date = (datetime.now() - timedelta(days=1)).isoformat()
#         data = {
#             'title': 'New Task',
#             'description': 'New Description',
#             'status': 'todo',
#             'due_date': due_date
#         }
#         response = api_client.post(url, data, format='json')
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert 'due_date' in response.data['data']

#     def test_task_detail(self, api_client, test_user, test_task):
#         api_client.force_authenticate(user=test_user)
#         url = reverse('task-detail', kwargs={'pk': test_task.pk})
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['data']['title'] == test_task.title

#     def test_update_task(self, api_client, test_user, test_task):
#         api_client.force_authenticate(user=test_user)
#         url = reverse('task-detail', kwargs={'pk': test_task.pk})
#         data = {'title': 'Updated Task', 'status': 'in_progress'}
#         response = api_client.patch(url, data, format='json')
#         assert response.status_code == status.HTTP_200_OK
#         test_task.refresh_from_db()
#         assert test_task.title == 'Updated Task'
#         assert test_task.status == 'in_progress'

#     def test_delete_task(self, api_client, test_user, test_task):
#         api_client.force_authenticate(user=test_user)
#         url = reverse('task-detail', kwargs={'pk': test_task.pk})
#         response = api_client.delete(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert Task.objects.count() == 0