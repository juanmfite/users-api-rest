from rest_framework import serializers
from django.contrib.auth.models import Group

from apps.users.models import User
from apps.users.exceptions import BaseAPIException
from apps.users.utils import CheckPassword


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for User class.
    """

    class Meta:
        model = Group
        fields = ['name']


class UserBaseSerializer(serializers.ModelSerializer):
    """
    Serializer for User class.
    """

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
        ]


class UserCreateSerializer(UserBaseSerializer):
    """
    Serializer for User class.
    """
    repeat_password = serializers.CharField(write_only=True, required=False)
    groups = serializers.ListField(write_only=True)
    created = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserBaseSerializer.Meta.fields + [
            'repeat_password',
            'groups',
            'updated',
            'created',
            'email',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    read_only_fields = (
        'id',
        'updated',
        'created'
    )

    def get_created(self, obj):
        return obj.date_joined

    def create(self, data):
        groups = data.pop('groups')
        repeat_password = data.pop('repeat_password')
        password = data.pop('password')

        if User.objects.filter(email=data['email']).exists():
            raise BaseAPIException('Email is not available.')

        CheckPassword(password, repeat_password).all_validations()

        user = User.objects.create(**data)
        user.set_password(password)
        user.save()

        self._add_user_to_groups(user, groups)
        return user

    def _add_user_to_groups(self, user, groups):
        if groups:
            for group in groups:
                obj, _ = Group.objects.get_or_create(name=group)
                obj.user_set.add(user)


class UserUpdateSerializer(UserCreateSerializer):
    old_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = UserCreateSerializer.Meta.fields + ['old_password']

    def update(self, instance, data, auth_user=None):
        old_password = data.pop('old_password', None)
        password = data.pop('password', None)
        groups = data.pop('groups', None)
        auth_user = data.pop('auth_user')

        groups = self.custom_validations(
            instance, old_password, password,
            groups, data.get('email', None), auth_user
        )

        User.objects.filter(pk=instance.pk).update(**data)
        instance.refresh_from_db()
        instance.set_password(password)
        instance.save()

        self._add_user_to_groups(instance, groups)
        return instance

    def custom_validations(
        self, instance, old_password, password, groups, email, auth_user
    ):
        '''
        This method check:
        - Staff users can change user's passwords freely without knowing their previous password.
          If you are not staff, you need to also provide your old password in order to change it.
        - Only staff users can manipulate groups. Normal users are not allowed to change their
          own groups.
        - Users are free to change their email as long as the new email doesn't conflict with
          another user.
        - To execute an update on a user you need to be authenticated either as the affected
          user or as a staff user.

        Only return the groups or a empty list if does not have permission.
        '''
        if not auth_user.staff_or_superuser:
            if instance != auth_user:
                raise BaseAPIException('Does not have permission to modified this User.')

            CheckPassword(password, old_password).is_different()

            if not instance.check_password(old_password):
                raise BaseAPIException('Old Password is wrong.')

            groups = []

        if User.objects.filter(email=email).exists():
            raise BaseAPIException('Email is not available.')

        return groups


class UserPartialUpdateSerializer(UserUpdateSerializer):

    class Meta:
        model = User
        fields = UserCreateSerializer.Meta.fields + ['old_password']
        extra_kwargs = {
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            'password': {'required': False},
            'old_password': {'required': False},
            'groups': {'required': False},
        }


class UserDetailMinimalSerializer(UserBaseSerializer):
    """
    Serializer for User detail with minimal information.
    """

    read_only_fields = (
        'id',
        'username',
        'first_name',
        'last_name',
    )

class UserDetailSerializer(UserBaseSerializer):
    """
    Serializer for User detail with full information.
    """
    groups = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    password = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserBaseSerializer.Meta.fields + [
            'groups',
            'updated',
            'created',
            'email',
            'password',
        ]
    
    read_only_fields = (
        'id',
        'username',
        'first_name',
        'last_name',
        'groups',
        'updated',
        'created',
        'email',
        'password',
    )

    def get_groups(self, obj):
        groups = [group.name for group in obj.groups.all()]
        return groups

    def get_created(self, obj):
        return obj.date_joined
    
    def get_password(self, obj):
        return '********'
