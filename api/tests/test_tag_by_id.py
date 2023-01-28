from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from api.models import Tag
from model_mommy import mommy
from model_mommy.mommy import make

class TestTagById(APITestCase):

    tag1: Tag
    url = reverse_lazy('tag', kwargs={'id': 1})

    def __prepare(self):

        self.tag1 = mommy.make(
            Tag,
            id=1,
            label='Fiction',
            count=5
        )

    def test_route_status(self):
        "It should return 200"

        self.__prepare()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_creation(self):
        "it should return a tag by id"

        self.__prepare()
        response = self.client.get(self.url)

        expected =  {
            'id': 1,
            'label': self.tag1.label,
            'count': self.tag1.count,
        }

        self.assertEqual(expected, response.json())
