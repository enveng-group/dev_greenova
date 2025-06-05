from django.test import TestCase

class ProjectManagementTests(TestCase):
    def test_project_creation(self):
        response = self.client.post('/projects/create/', {'name': 'Test Project'})
        self.assertEqual(response.status_code, 201)
        self.assertContains(response, 'Test Project')

    def test_project_listing(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Projects')

    def test_project_detail(self):
        response = self.client.get('/projects/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Project Details')

    def test_project_update(self):
        response = self.client.post('/projects/1/update/', {'name': 'Updated Project'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Updated Project')

    def test_project_deletion(self):
        response = self.client.post('/projects/1/delete/')
        self.assertEqual(response.status_code, 204)