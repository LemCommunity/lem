from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from factory import LazyFunction
from factory.django import DjangoModelFactory
from faker import Faker
from faker.providers import internet, misc

faker = Faker()
faker.add_provider(internet)
faker.add_provider(misc)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]

    username = LazyFunction(lambda: faker.user_name())
    email = LazyFunction(lambda: faker.email())
    first_name = LazyFunction(lambda: faker.first_name())
    last_name = LazyFunction(lambda: faker.last_name())
    password = LazyFunction(lambda: make_password(faker.password()))
