import json

from django.conf import settings

import requests

__all__ = ['SubscriptionService']


class SubscriptionService():
    '''
    Client to conect to a microservice.
    '''
    BASE_URL = settings.SUBSCRIPTION_SERVICE_URL
    USER_URL = '{base_url}/api/v1/users/{id}'
    TIMEOUT = 10
    HEADERS = {'content-type': 'application/json'}

    def get_subscription_state(self, id):
        url = self.USER_URL.format(base_url=self.BASE_URL, id=id)
        response = requests.get(
            url=url, headers=self.HEADERS, timeout=self.TIMEOUT
        )
        return response


class SubscriptionServiceMock():

    def get_subscription_state(self, id):
        response = requests.Response()
        response.status_code = 200
        data = {
            'id': id,
            'subscription': 'active'
        }
        response._content = json.dumps(data, indent=2).encode('utf-8')
        return response


if settings.SUBSCRIPTION_SERVICE_DEBUG:
    SubscriptionService = SubscriptionServiceMock # NOQA
