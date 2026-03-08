import json
import time
from datetime import datetime

from django.test import TestCase, Client

from deadlinemain.models import Student, DeadlineItem


class DashboardViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a test student
        self.student = Student.objects.create(
            student_id='20261234',
            name='Test User',
            email='test@example.com',
            auth_pwd='password'
        )
        session = self.client.session
        session['student_id'] = self.student.student_id
        session.save()
        
        # Test URLs
        self.add_deadline_url = '/add_deadline/'
        self.update_deadline_status_url = '/update_deadline_status/'

    def test_add_deadline_success(self):
        # We define a deadline strictly in the yyyy-mm-dd HH:MM format
        deadline_str = '2026-10-31 23:59'
        payload = {
            'deadline_title': 'Integration Test Task',
            'content': 'This is a test content',
            'deadline': deadline_str
        }
        
        response = self.client.post(
            self.add_deadline_url, 
            data=json.dumps(payload), 
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertTrue(resp_data.get('success'), f"Response error: {resp_data.get('error')}")
        
        # Verify the deadline was created in DB and timestamp was generated correctly
        deadline = DeadlineItem.objects.first()
        self.assertIsNotNone(deadline)
        self.assertEqual(deadline.deadline_title, 'Integration Test Task')
        self.assertEqual(deadline.status, '0')
        
        # Verify integer timestamps
        self.assertIsInstance(deadline.deadline, int)
        self.assertIsInstance(deadline.update_time, int)
        
        # Verify the integer holds the correct parsed time
        expected_dt = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')
        expected_timestamp = int(expected_dt.timestamp())
        self.assertEqual(deadline.deadline, expected_timestamp)
        
    def test_update_deadline_status(self):
        initial_timestamp = int(time.time()) - 1000  # Some time in the past
        deadline = DeadlineItem.objects.create(
            student=self.student,
            deadline_title='Task to complete',
            content='Wait for it',
            deadline=initial_timestamp + 86400,
            status='0',
            update_time=initial_timestamp
        )
        
        payload = {
            'id': deadline.id,
            'status': '1'
        }
        
        response = self.client.post(
            self.update_deadline_status_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get('success'))
        
        # Refresh from DB
        deadline.refresh_from_db()
        self.assertEqual(deadline.status, '1')
        
        # Ensure update_time was updated to a recent integer Unix timestamp
        self.assertIsInstance(deadline.update_time, int)
        self.assertGreater(deadline.update_time, initial_timestamp)
