from django.urls import reverse

from apps.users.constants import CheckPasswordCts
from apps.users.tests.factory import UsersFakeFactory
from apps.users.tests.test_views import UserViewSetTestCase


class UserCreateTestCase(UserViewSetTestCase):

    def setUp(self):
        super().setUp()
        self.data = UsersFakeFactory.base_data_create_test()

    def _base_request(self, data):
        url = reverse(
            '{namespace}:{basename}-list'.format(
                namespace=self.namespace,
                basename=self.basename
            )
        )
        response = self.client.post(url, data=data, format='json')
        return response

    def test_create_password_not_equal(self):
        data = self.data
        data['password'] = "SuperSecurePasswd"
        data['repeat_password'] = "SuperSecurePasswd1"

        response = self._base_request(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], CheckPasswordCts.EQUALS)

    def test_create_password_not_len(self):
        data = self.data
        data['password'] = "Super.1"
        data['repeat_password'] = "Super.1"

        response = self._base_request(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], CheckPasswordCts.LEN)

    def test_create_password_not_has_digit(self):
        data = self.data
        data['password'] = "Super.notdigit"
        data['repeat_password'] = "Super.notdigit"

        response = self._base_request(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], CheckPasswordCts.HAS_DIGIT)

    def test_create_password_not_has_uppercase(self):
        data = self.data
        data['password'] = "super.notupper1"
        data['repeat_password'] = "super.notupper1"

        response = self._base_request(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], CheckPasswordCts.HAS_UPPERCASE)

    def test_create_password_not_has_special_sym(self):
        data = self.data
        data['password'] = "Supernotupper1"
        data['repeat_password'] = "Supernotupper1"

        response = self._base_request(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['detail'],
            CheckPasswordCts.HAS_SPECIAL_SYM.format(sym=CheckPasswordCts.SPECIAL_SYM)
        )

    def test_create_ok_with_superuser(self):
        data = self.data

        response = self._base_request(data)

        self.assertEqual(response.status_code, 201)

    def test_create_ok_with_staffuser(self):
        self.user = UsersFakeFactory.make_staff_user()
        self.client.force_authenticate(user=self.user)

        data = self.data

        response = self._base_request(data)

        self.assertEqual(response.status_code, 201)

    def test_create_not_permission(self):
        self.user = UsersFakeFactory.make_user()
        self.client.force_authenticate(user=self.user)

        data = self.data

        response = self._base_request(data)

        self.assertEqual(response.status_code, 403)
