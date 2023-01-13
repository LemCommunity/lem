from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from factory import LazyAttribute, SelfAttribute, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.generic.models import Reaction
from apps.users.tests.factories import UserFactory

faker = Faker()


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = Faker("name")


class ReactionFactory(DjangoModelFactory):
    class Meta:
        exclude = ["content_object"]
        abstract = True

    object_id = SelfAttribute("content_object.id")
    content_type = LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
    )


class TaggedUserFactory(ReactionFactory):
    class Meta:
        model = Reaction

    user = SubFactory(UserFactory)


class TaggedGroupFactory(ReactionFactory):
    class Meta:
        model = Reaction

    content_object = SubFactory(GroupFactory)
