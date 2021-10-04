from django.test import TestCase
from django.urls import reverse


class PasswordResetViewTests(TestCase):
    def test_user_cant_access_the_password_reset_view_more_than_5_times(self):
        url = reverse("admin_password_reset")

        for i in range(5):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            print(i)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
