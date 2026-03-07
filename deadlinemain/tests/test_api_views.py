import json
import time
from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from deadlinemain.models import Student, DeadlineTask, DeadlineLog

class ApiViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            student_id='20261234',
            name='Test User',
            email='test@example.com',
            auth_pwd='password'
        )
        session = self.client.session
        session['student_id'] = self.student.student_id
        session.save()
        
        self.dashboard_data_url = '/api/dashboard_data/'

        self.now_int = int(time.time())
        day_second = 86400
        self.deadline_int = self.now_int + day_second
        self.update_time_int = self.now_int - 3600 # 1 hour ago
        
        self.task = DeadlineTask.objects.create(
            student=self.student,
            task_title='API Test Task',
            content='Testing the dashboard data endpoint',
            deadline=self.deadline_int,
            status='0',
            update_time=self.update_time_int
        )
        
        self.log_create_time_int = self.update_time_int
        self.log = DeadlineLog.objects.create(
            task=self.task,
            task_content='Created the task',
            create_time=self.log_create_time_int
        )

    def test_dashboard_data_formatting(self):
        response = self.client.get(self.dashboard_data_url)
        self.assertEqual(response.status_code, 200)
        
        resp_data = response.json()
        self.assertTrue(resp_data.get('success'), f"Response error: {resp_data.get('error')}")
        
        # Verify tasks array exists
        tasks = resp_data['data'].get('tasks', [])
        self.assertTrue(len(tasks) > 0)
        
        # Get our task
        our_task = next(t for t in tasks if t['id'] == self.task.id)
        
        # Verify formatting
        time_format_HM = '%Y-%m-%d %H:%M'
        time_format_HMS = '%Y-%m-%d %H:%M:%S'
        
        expected_deadline_str = datetime.fromtimestamp(self.deadline_int).strftime(time_format_HM)
        self.assertEqual(our_task['deadline'], expected_deadline_str)
        
        expected_update_time_str = datetime.fromtimestamp(self.update_time_int).strftime(time_format_HM)
        self.assertEqual(our_task['update_time_display'], expected_update_time_str)
        
        # Verify log formatting
        logs = our_task.get('logs', [])
        self.assertTrue(len(logs) > 0)
        expected_log_create_time_str = datetime.fromtimestamp(self.log_create_time_int).strftime(time_format_HMS)
        self.assertEqual(logs[0]['create_time'], expected_log_create_time_str)
        
        # Validate timezone format output if still isoformat is present
        self.assertIn('Z', our_task['update_time'])
