from collections.abc import Sequence
from typing import Any

from django.contrib.auth import get_user_model
from factory import LazyFunction, post_generation
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

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)
