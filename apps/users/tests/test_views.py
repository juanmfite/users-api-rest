from rest_framework.test import APITestCase

from apps.users.models import User
from apps.users.tests.factory import UsersFakeFactory


class UserViewSetTestCase(APITestCase):
    ModelClass = User
    basename = 'users'
    namespace = 'users'

    def setUp(self):
        self.user = UsersFakeFactory.make_super_user()
        self.client.force_authenticate(user=self.user)
