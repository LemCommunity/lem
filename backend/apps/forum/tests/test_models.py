import pytest

from backend.apps.forum.models.models import Category, Post


@pytest.mark.django_db(transaction=True)
class TestCategoryModel:
    @pytest.mark.parametrize(
        ("name, result"),
        [("test", "Test"), ("testcategory", "Testcategory")],
    )
    def test_capitalize_name(self, name, result):
        # Create a new Category instance
        category = Category.objects.create(name=name)

        # Check that the name field is correctly set
        assert category.capitalize_name == result

    @pytest.mark.parametrize(
        "name",
        ["Test", "Testcategory"],
    )
    def test_category_alphabetic(self, name):
        category = Category.objects.create(name=name)
        category.clean()


@pytest.mark.django_db(transaction=True)
class TestPostModel:
    @pytest.mark.parametrize(
        ("name, result"),
        [("test", "Test"), ("testpost", "Testpost")],
    )
    def test_capitalize_title(self, title, result):
        # Create a new Post instance
        post = Post.objects.create(title=title)

        # Check that the title field is correctly set
        assert post.capitalize_title == result

    @pytest.mark.parametrize(
        "name",
        ["Test", "Testpost"],
    )
    def test_post_alphabetic(self, title):
        post = Post.objects.create(title=title)
        post.clean()
