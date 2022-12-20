import pytest

from backend.apps.forum.models import Category
from backend.apps.forum.tests.factories import CategoryFactory


@pytest.mark.django_db(transaction=True)
class TestCategoryModel:
    @pytest.fixture(autouse=True)
    def category_module(self, request) -> Category:
        return CategoryFactory.build(name=request.param)

    @pytest.mark.parametrize(
        "category_module, expected",
        [
            ("books", "Books"),
            ("ebooks", "Ebooks"),
        ],
        indirect=["category_module"],
    )
    def test_category_capitalize_name(self, category_module, expected):
        assert category_module.capitalize_name == expected


# @pytest.mark.django_db(transaction=True)
# class TestPostModel:
#     @pytest.fixture(autouse=True)
#     def post_module(self, request) -> Post:
#         return PostFactory.build(title=request.param)

#     @pytest.mark.parametrize(
#         "post_module, expected",
#         [
#             ("test", "Test"),
#             ("testpost", "Testpost"),
#         ],
#         indirect=["post_module"],
#     )
#     def test_post_capitalize_title(self, post_module, expected):
#         assert post_module.capitalize_title == expected
