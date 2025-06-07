from django.test import TestCase


class ProjectManagementTests(TestCase):
    def test_project_creation(self) -> None:
        response = self.client.post("/projects/create/", {"name": "Test Project"})
        assert response.status_code == 201
        self.assertContains(response, "Test Project")

    def test_project_listing(self) -> None:
        response = self.client.get("/projects/")
        assert response.status_code == 200
        self.assertContains(response, "Projects")

    def test_project_detail(self) -> None:
        response = self.client.get("/projects/1/")
        assert response.status_code == 200
        self.assertContains(response, "Project Details")

    def test_project_update(self) -> None:
        response = self.client.post("/projects/1/update/", {"name": "Updated Project"})
        assert response.status_code == 200
        self.assertContains(response, "Updated Project")

    def test_project_deletion(self) -> None:
        response = self.client.post("/projects/1/delete/")
        assert response.status_code == 204
