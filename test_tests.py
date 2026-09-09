
import pytest


class TestBooksCollector:

    @pytest.mark.parametrize("name", ["Sherlock", "A" * 40])
    def test_add_new_book_valid_name_book_added(self, collector, name):
        collector.add_new_book(name)
        assert name in collector.books_genre and collector.books_genre[name] == ""

    @pytest.mark.parametrize("name", ["A" * 41, "A" * 55, ""])
    def test_add_new_book_invalid_name_book_not_added(self, collector, name):
        collector.add_new_book(name)
        assert name not in collector.books_genre

    def test_add_new_book_duplicate_name_book_not_added(self, collector):
        collector.add_new_book("Sherlock")
        collector.add_new_book("Sherlock")
        assert len(collector.books_genre) == 1

    @pytest.mark.parametrize("book_name, input_genre, expected_genre", [
        ("Sherlock", 'Детективы', 'Детективы'),
        ("Great Gatsby", 'Драма', "")
    ])
    def test_set_book_genre_valid_and_invalid(self, collector, book_name, input_genre, expected_genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, input_genre)
        assert collector.books_genre[book_name] == expected_genre

    def test_set_book_genre_nonexistent_book_genre_not_set(self, collector):
        collector.set_book_genre("Sherlock", 'Детективы')
        assert "Sherlock" not in collector.books_genre and len(collector.books_genre) == 0

    def test_get_book_genre_valid_book_genre_returned(self, collector):
        collector.add_new_book("Sherlock")
        collector.set_book_genre("Sherlock", 'Детективы')
        assert collector.get_book_genre("Sherlock") == 'Детективы'

    def test_get_book_genre_nonexistent_book_genre_none_returned(self, collector):
        assert "Sherlock" not in collector.books_genre and collector.get_book_genre("Sherlock") is None

    @pytest.mark.parametrize("books_data, search_genre, expected", [
        ([("Sherlock", 'Детективы')], "Детективы", ["Sherlock"]),
        ([], "Детективы", []),
        ([("Sherlock", 'Детективы')], "Комедии", []),
        ([("Sherlock", 'Детективы')], "Драма", [])
    ])
    def test_get_books_with_specific_genre(self, collector, books_data, search_genre, expected):
        for name, genre in books_data:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        assert collector.get_books_with_specific_genre(search_genre) == expected

    @pytest.mark.parametrize("books_data, expected", [
        ([("Beauty and Beast", 'Мультфильмы'), ("Sherlock", 'Детективы')], ["Beauty and Beast"]),
        ([("Sherlock", 'Детективы')], [])
    ])
    def test_get_books_for_children(self, collector, books_data, expected):
        for name, genre in books_data:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        assert collector.get_books_for_children() == expected

    @pytest.mark.parametrize("books_data, expected", [
        (["Sherlock", "Beauty and Beast"], {"Sherlock": "", "Beauty and Beast": ""}),
        ([], {})
    ])
    def test_get_books_genre(self, collector, books_data, expected):
        for name in books_data:
            collector.add_new_book(name)
        assert collector.get_books_genre() == expected

    def test_add_book_in_favorites_existing_book_added_to_favorites(self, collector):
        collector.add_new_book("Sherlock")
        collector.add_book_in_favorites("Sherlock")
        assert "Sherlock" in collector.favorites and len(collector.favorites) == 1

    def test_add_book_in_favorites_nonexistent_book_empty_list_returned(self, collector):
        collector.add_book_in_favorites("Sherlock")
        assert collector.favorites == []

    def test_add_book_in_favorites_duplicate_book_not_added(self, collector_with_favorite):
        collector_with_favorite.add_book_in_favorites("Sherlock")
        assert len(collector_with_favorite.favorites) == 1

    def test_delete_book_from_favorites_existing_book_deleted(self, collector_with_favorite):
        collector_with_favorite.add_new_book("Beauty and Beast")
        collector_with_favorite.add_book_in_favorites("Beauty and Beast")
        collector_with_favorite.delete_book_from_favorites("Beauty and Beast")
        assert "Beauty and Beast" not in collector_with_favorite.favorites and len(collector_with_favorite.favorites) == 1 

    def test_delete_book_from_favorites_nonexistent_book_not_deleted(self, collector_with_favorite):
        collector_with_favorite.delete_book_from_favorites("Beauty and Beast")
        assert "Sherlock" in collector_with_favorite.favorites and len(collector_with_favorite.favorites) == 1

    def test_get_list_of_favorites_books_favorites_list_returned(self, collector_with_favorite):
        favorites = collector_with_favorite.get_list_of_favorites_books()
        assert favorites == ["Sherlock"]