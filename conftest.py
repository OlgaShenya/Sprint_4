import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    collector = BooksCollector()
    return collector

@pytest.fixture
def collector_with_favorite(collector):
    collector.add_new_book("Sherlock")
    collector.add_book_in_favorites("Sherlock")
    return collector