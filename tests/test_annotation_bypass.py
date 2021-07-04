from datetime import date

import pytest
from django.db.models import F
from django.db.models.expressions import CombinedExpression
from django.db.models.functions import ExtractYear

from expression_filter import AnnotationBypass
from tests.models import Book

db_test = pytest.mark.django_db


@db_test
def test_db_works():
    # If this fails, check your setup
    Book.objects.create(
        title='one', publish_date=date.today(), page_count=1, word_count=1
    )
    assert Book.objects.count() == 1
    book = Book.objects.get(title='one')
    assert book.page_count == 1


@db_test
def test_basic_function():
    Book.objects.create(
        title='one',
        publish_date=date(year=2002, month=6, day=16),
        page_count=80,
        word_count=10000,
    )
    Book.objects.create(
        title='two',
        publish_date=date(year=2010, month=2, day=5),
        page_count=100,
        word_count=10000,
    )
    Book.objects.create(
        title='three',
        publish_date=date(year=2015, month=7, day=20),
        page_count=150,
        word_count=10000,
    )

    year = ExtractYear(F('publish_date'))
    from_annotation = list(
        Book.objects.annotate(publish_year=year).filter(publish_year=2010)
    )
    from_bypass = list(Book.objects.filter(AnnotationBypass(year, 'exact', 2010)))

    assert from_annotation == from_bypass
