from decimal import Decimal

from mixer.backend.django import Mixer


class UsersFakeFactory(object):
    '''
    Use to create fake objects from this app
    '''

    default_user = {
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@ine.test",
    }

    superuser_user = {
        "username": "johndoe_superuser",
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe_staff@ine.test",
        "is_superuser": True
    }

    staff_user = {
        "username": "johndoe_staff",
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe_staff@ine.test",
        "is_superuser": True
    }

    @classmethod
    def make_user(cls, *args, **kwargs):
        params = cls.default_user.copy()
        params.update(kwargs)
        instance = Mixer().blend('users.User', **params)
        return instance
    
    @classmethod
    def make_super_user(cls, *args, **kwargs):
        params = cls.superuser_user.copy()
        params.update(kwargs)
        instance = Mixer().blend('users.User', **params)
        instance.set_password('SuperPass.1')
        instance.save()
        return instance
    
    @classmethod
    def make_staff_user(cls, *args, **kwargs):
        params = cls.staff_user.copy()
        params.update(kwargs)
        instance = Mixer().blend('users.User', **params)
        instance.set_password('SuperPass.1')
        instance.save()
        return instance
