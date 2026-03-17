import json
import time
from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from deadlinemain.models import Student, DeadlineItem, DeadlineLog

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
        
        self.dashboard_meta_url = '/api/dashboard_meta/'
        self.dashboard_deadlines_url = '/api/dashboard_deadlines/'

        self.now_int = int(time.time())
        day_second = 86400
        self.deadline_int = self.now_int + day_second
        self.update_time_int = self.now_int - 3600 # 1 hour ago
        
        self.deadline = DeadlineItem.objects.create(
            student=self.student,
            deadline_title='API Test Deadline',
            content='Testing the dashboard data endpoint',
            deadline=self.deadline_int,
            status='0',
            update_time=self.update_time_int
        )
        
        self.log_create_time_int = self.update_time_int
        self.log = DeadlineLog.objects.create(
            deadline=self.deadline,
            deadline_content='Created the Deadline',
            create_time=self.log_create_time_int
        )

    def test_dashboard_meta_formatting(self):
        response = self.client.get(self.dashboard_meta_url)
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertTrue(resp_data.get('success'))
        self.assertEqual(resp_data['data']['student']['name'], 'Test User')

    def test_dashboard_deadlines_formatting(self):
        response = self.client.get(self.dashboard_deadlines_url)
        self.assertEqual(response.status_code, 200)
        
        resp_data = response.json()
        self.assertTrue(resp_data.get('success'), f"Response error: {resp_data.get('error')}")
        
        # Verify deadlines array exists
        deadlines = resp_data['data'].get('deadlines', [])
        self.assertTrue(len(deadlines) > 0)
        
        # Get our deadline
        our_deadline = next(t for t in deadlines if t['id'] == self.deadline.id)
        
        # Verify formatting
        time_format_HM = '%Y-%m-%d %H:%M'
        time_format_HMS = '%Y-%m-%d %H:%M:%S'
        
        expected_deadline_str = datetime.fromtimestamp(self.deadline_int).strftime(time_format_HM)
        self.assertEqual(our_deadline['deadline'], expected_deadline_str)
        
        # Verify log formatting
        logs = our_deadline.get('logs', [])
        self.assertTrue(len(logs) > 0)
        expected_log_create_time_str = datetime.fromtimestamp(self.log_create_time_int).strftime(time_format_HMS)
        self.assertEqual(logs[0]['create_time'], expected_log_create_time_str)
        
        # Validate timezone format output if still isoformat is present
        self.assertIn('Z', our_deadline['update_time'])
