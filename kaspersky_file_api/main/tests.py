import subprocess
from time import sleep
from uuid import uuid4

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Search


class YourTestClass(TestCase):
    @classmethod
    def setUpClass(cls):
        # Запустить my_script.py в фоновом режиме перед началом тестов
        subprocess.Popen(['python', 'worker.py'])

    @classmethod
    def tearDownClass(cls):
        # Остановить my_script.py после окончания тестов
        subprocess.Popen(['pkill', '-f', 'worker.py'])

    def setUp(self):
        self.client = APIClient()

    def test_not_finished_search(self):
        """ Тестирует выдачу при незавершенном поиске """
        test_search = Search.objects.create(
            tag=uuid4(),
            finished=False
        )
        test_search.save()

        response = self.client.get(reverse(
            'get_search_status_and_paths_api_view',
            args=[test_search.tag]
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['finished'])
        self.assertIsNone(response.data.get('paths'))

    def test_finished_search(self):
        """ Тестирует выдачу при завершенном поиске """
        test_search = Search.objects.create(
            tag=uuid4(),
            finished=True
        )
        test_search.paths.create(path='test_path_1')
        test_search.paths.create(path='test_path_2')
        test_search.save()

        response = self.client.get(
            reverse('get_search_status_and_paths_api_view',
                    args=[test_search.tag]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        search_data = response.data
        self.assertTrue(search_data['finished'])
        self.assertEqual(len(search_data['paths']), 2)
        self.assertIn('test_path_1', search_data['paths'])
        self.assertIn('test_path_2', search_data['paths'])

    def test_get_search_status_and_paths_not_found(self):
        # Отправка GET запроса для несуществующего объекта
        response = self.client.get(
            reverse('get_search_status_and_paths_api_view',
                    args=['non_existent_tag']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_search(self):
        """ Проверка что действительно в бд создается задача поиска """
        test_data = {
            'text': 'a',
        }

        response = self.client.post(reverse('create_search_api_view'),
                                    data=test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        search_id = response.data['search_id']
        search = Search.objects.get(tag=str(search_id))
        self.assertIsNotNone(search)
        sleep(2)
        response = self.client.get(reverse('get_search_status_and_paths_api_view', args=[search.tag]))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['finished'])
        self.assertEqual(
            response.data.get('paths'),
            [
                "/kaspersky_app/test_directory/dir_1/file_0e3e2253-8d13-4552-95be-f3ffe5206ac0"
            ]
        )