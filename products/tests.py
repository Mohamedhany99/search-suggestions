from django.test import TestCase, Client
from django.urls import reverse
from .models import Product
from .views import import_products, search
from rest_framework import status
import csv
import io
import os


class ProductTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.import_url = reverse(import_products)
        self.search_url = reverse(search)

    def test_import_products(self):
        with open("test_file.csv", "w") as file:
            file.write("id,name,category,price\n")
            file.write("98297800-1486-40c1-9b44-7ee5f5cec34a,Mouse,Books,57257.82\n")
        # data = "id,name\n98297800-1486-40c1-9b44-7ee5f5cec34a,Mouse,Books,57257.82\n"
        # data_file = io.StringIO(data)
        # os.remove("test_file.csv")
        data_file = {"file": open("test_file.csv", "rb")}
        response = self.client.post(
            self.import_url, data_file, format="multipart/form-data"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(
            Product.objects.get(id="98297800-1486-40c1-9b44-7ee5f5cec34a").name, "Mouse"
        )
        # self.assertEqual(Product.objects.get(id=2).name, "Banana")
        os.remove("test_file.csv")

    def test_search(self):
        Product.objects.create(id=1, name="Apple")
        Product.objects.create(id=2, name="Banana")
        response = self.client.get(self.search_url, {"q": "a"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "Apple")
        self.assertEqual(response.data[1]["name"], "Banana")
