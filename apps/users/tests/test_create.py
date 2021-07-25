from django.urls import reverse

from apps.users.constants import CheckPasswordCts
from apps.users.tests.factory import UsersFakeFactory
from apps.users.tests.test_views import UserViewSetTestCase


class UserCreateTestCase(UserViewSetTestCase):

    def _base_request(self, data):
        url = reverse(
            '{namespace}:{basename}-list'.format(
                namespace=self.namespace,
                basename=self.basename
            )
        )
        response = self.client.post(url, data=data, format='json')
        # import pdb; pdb.set_trace()
        return response
    
    def test_create_password_not_equal(self):
        data = {
            "username": "johndoe-test-creation",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe-test-creation@ine.test",
            "password": "SuperSecurePasswd",
            "repeat_password": "SuperSecurePasswd1",
            "groups": [
                "sales",
                "support",
            ]
        }

        response = self._base_request(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], CheckPasswordCts.EQUALS)
    
    def test_create_password_not_len(self):
        data = {
            "username": "johndoe-test-creation",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe-test-creation@ine.test",
            "password": "Super.1",
            "repeat_password": "Super.1",
            "groups": [
                "sales",
                "support",
            ]
        }

        response = self._base_request(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], CheckPasswordCts.LEN)
    
    def test_create_password_not_has_digit(self):
        data = {
            "username": "johndoe-test-creation",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe-test-creation@ine.test",
            "password": "Super.notdigit",
            "repeat_password": "Super.notdigit",
            "groups": [
                "sales",
                "support",
            ]
        }

        response = self._base_request(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], CheckPasswordCts.HAS_DIGIT)
    
    def test_create_password_not_has_uppercase(self):
        data = {
            "username": "johndoe-test-creation",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe-test-creation@ine.test",
            "password": "super.notupper1",
            "repeat_password": "super.notupper1",
            "groups": [
                "sales",
                "support",
            ]
        }

        response = self._base_request(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], CheckPasswordCts.HAS_UPPERCASE)
    
    def test_create_password_not_has_special_sym(self):
        data = {
            "username": "johndoe-test-creation",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe-test-creation@ine.test",
            "password": "Supernotupper1",
            "repeat_password": "Supernotupper1",
            "groups": [
                "sales",
                "support",
            ]
        }

        response = self._base_request(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['detail'],
            CheckPasswordCts.HAS_SPECIAL_SYM.format(sym=CheckPasswordCts.SPECIAL_SYM)
        )
    
    def test_create_ok_with_superuser(self):
        data = {
            "username": "johndoe-test-creation-superuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe-test-creation-superuser@ine.test",
            "password": "Supernotupper1.",
            "repeat_password": "Supernotupper1.",
            "groups": [
                "sales",
                "support",
            ]
        }

        response = self._base_request(data)

        self.assertEqual(response.status_code, 201)

    def test_create_ok_with_staffuser(self):
        self.user = UsersFakeFactory.make_staff_user()
        self.client.force_authenticate(user=self.user)

        data = {
            "username": "johndoe-test-creation-staff",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe-test-creation-staff@ine.test",
            "password": "Supernotupper1.",
            "repeat_password": "Supernotupper1.",
            "groups": [
                "sales",
                "support",
            ]
        }

        response = self._base_request(data)

        self.assertEqual(response.status_code, 201)
    
    def test_create_not_permission(self):
        self.user = UsersFakeFactory.make_user()
        self.client.force_authenticate(user=self.user)

        data = {
            "username": "johndoe-test-creation-staff",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe-test-creation-staff@ine.test",
            "password": "Supernotupper1.",
            "repeat_password": "Supernotupper1.",
            "groups": [
                "sales",
                "support",
            ]
        }

        response = self._base_request(data)

        self.assertEqual(response.status_code, 403)
