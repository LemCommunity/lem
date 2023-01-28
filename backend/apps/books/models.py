from django.core.validators import RegexValidator
from django.db import models


class Genre(models.Model):
    """Genre database model"""

    GENRES = (
        ("LF", "Literary Fiction"),
        ("My", "Mystery"),
        ("Th", "Thriller"),
        ("Ho", "Horror"),
        ("Hi", "Historical"),
        ("Ro", "Romance"),
        ("We", "Western"),
        ("Bi", "Bildungsroman"),
        ("SpF", "Speculative Fiction"),
        ("SF", "Science Fiction"),
        ("Fa", "Fantasy"),
        ("Dy", "Dystopian"),
        ("MR", "Magical Realism"),
        ("RL", "Realist Literature"),
    )

    name = models.CharField(max_length=25, choices=GENRES)


class Book(models.Model):
    """Book database model"""

    TYPE_OF_COVER = (
        ("PB", "Paperback"),
        ("HC", "Hardcover Casewrap"),
        ("HDJ", "Hardcover Dust Jacket"),
    )
    PUBLICATION_FORMATS = (
        ("ebook", "E-Book format"),
        ("textbook", "Textbook format"),
    )

    title = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z0-9]*$",
                message="Title must be Alphanumeric",
                code="invalid_title",
            ),
        ],
    )
    original_title = models.CharField(
        max_length=255,
        blank=True,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z0-9]*$",
                message="Title must be Alphanumeric",
                code="invalid_title",
            ),
        ],
    )
    # author field
    year_of_publication = models.IntegerField()
    publisher = models.ForeignKey("BookPublisher", on_delete=models.CASCADE)
    issue_number = models.IntegerField(default=1)
    number_of_page = models.IntegerField()
    type_of_cover = models.CharField(max_length=55, choices=TYPE_OF_COVER)
    describe = models.TextField()
    publication_formats = models.CharField(max_length=55, choices=PUBLICATION_FORMATS)
    language_provided = models.ForeignKey("BookLanguage", on_delete=models.CASCADE)
    original_language = models.CharField(max_length=55)
    dimensions = models.ForeignKey("BookSize", on_delete=models.CASCADE)
    catalog_number = models.IntegerField()
    ISBN_id = models.IntegerField()
    genre = models.ManyToManyField(Genre)


class BookLanguage(models.Model):
    """Language of book database model"""

    language = models.CharField(max_length=50)
    shortcut_language = models.CharField(max_length=10)


class BookPublisher(models.Model):
    """Publisher for books database model"""

    publisher = models.CharField(max_length=50)


class BookSize(models.Model):
    """Dimension of books database model"""

    x_size = models.IntegerField(default=0)
    y_size = models.IntegerField(default=0)


class Review(models.Model):
    """Review database model"""

    # author field
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
