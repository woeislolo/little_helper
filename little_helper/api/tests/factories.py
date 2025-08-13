import factory

from django.contrib.auth import get_user_model


User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    # username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password123")

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        super()._after_postgeneration(instance, create, results)
        if create:
            instance.save()