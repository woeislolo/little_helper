import pytest

from django.db.utils import IntegrityError

from help_requests.models import *
from users.models import *


@pytest.mark.django_db
class TestCustomUser:

    def setup_method(self):
        self.base_user = CustomUser.objects.create(
            email='base@test.com',
            phone_number='79998887766',
            name='user_user',
            )
        
        self.staff_user = CustomUser.objects.create(
            email='staff@test.com',
            phone_number='79998887755',
            name='staff_staff',
            is_staff=True
            )

    def test_create_customuser_default_values(self):
        user = CustomUser.objects.create(
            email='test@test.com'
            )
        
        assert user.phone_number == None
        assert user.name == ''
        assert user.is_active == True
        assert user.is_staff == False

    def test_cant_create_customuser_with_existing_email(self):
        with pytest.raises(IntegrityError) as e:
            CustomUser.objects.create(email='base@test.com')

    def test_create_customuser_with_existing_phone_number(self):
        user = CustomUser.objects.create(
            email='base1@test.com',
            phone_number='79998887766',
            )
        
        assert user.phone_number == '79998887766'

    def test_create_customuser_with_existing_name(self):
        user = CustomUser.objects.create(
            email='base1@test.com',
            name='user_user',
            )
        
        assert user.name == 'user_user'

    def test_phone_number_max_length(self):
        max_length = self.base_user._meta.get_field("phone_number").max_length

        assert max_length == 20

    def test_name_max_length(self):
        max_length = self.base_user._meta.get_field("name").max_length

        assert max_length == 150
