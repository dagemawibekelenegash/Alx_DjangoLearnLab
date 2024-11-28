from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from .models import Book
from django.contrib.auth.models import User


class BookTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/books/"
        self.book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "publication_year": 2020,
        }
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_create_book(self):
        response = self.client.post(self.url, self.book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.book_data["title"])
        self.assertEqual(response.data["author"], self.book_data["author"])
        self.assertEqual(
            response.data["publication_year"], self.book_data["publication_year"]
        )

    def test_get_books_list(self):
        self.client.post(self.url, self.book_data, format="json")
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_book_by_id(self):
        book = self.client.post(self.url, self.book_data, format="json").data
        book_id = book["id"]
        response = self.client.get(f"/api/books/{book_id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], book_id)

    def test_update_book(self):
        book = self.client.post(self.url, self.book_data, format="json").data
        book_id = book["id"]
        updated_data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "publication_year": 2022,
        }
        response = self.client.put(
            f"/api/books/{book_id}/", updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Book")
        self.assertEqual(response.data["author"], "Updated Author")
        self.assertEqual(response.data["publication_year"], 2022)

    def test_delete_book(self):
        book = self.client.post(self.url, self.book_data, format="json").data
        book_id = book["id"]
        response = self.client.delete(f"/api/books/{book_id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"/api/books/{book_id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_books(self):
        book1 = self.client.post(
            self.url,
            {"title": "Python Book", "author": "Author One", "publication_year": 2021},
            format="json",
        ).data
        book2 = self.client.post(
            self.url,
            {"title": "Java Book", "author": "Author Two", "publication_year": 2020},
            format="json",
        ).data
        response = self.client.get(f"/api/books/?search=python", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books(self):
        self.client.post(
            self.url,
            {"title": "Python Book", "author": "Author One", "publication_year": 2021},
            format="json",
        )
        self.client.post(
            self.url,
            {"title": "Java Book", "author": "Author Two", "publication_year": 2020},
            format="json",
        )
        response = self.client.get(f"/api/books/?ordering=title", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Java Book")

    def test_permissions(self):
        self.client.logout()
        response = self.client.post(self.url, self.book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url, self.book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
