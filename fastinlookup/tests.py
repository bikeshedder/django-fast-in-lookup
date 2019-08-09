from django.conf import settings
from django.db import connection
from django.db.models import F
from django.test import TestCase

from .models import Item
from . import lookups


ITEM_COUNT=10

class IneffTestCase(TestCase):

    def setUp(self):
        self.item_names = [f'Item #{i}' for i in range(1, ITEM_COUNT+1)]
        self.items = Item.objects.bulk_create([Item(name=name) for name in self.item_names])
        Item.objects.update(fk=F('id'))
        self.item_ids = [item.id for item in self.items]

    def test_in_pk(self):
        self.assertEqual(len(Item.objects.filter(pk__in=self.item_ids)), ITEM_COUNT)

    def test_in_id(self):
        self.assertEqual(len(Item.objects.filter(id__in=self.item_ids)), ITEM_COUNT)

    def test_in_name(self):
        self.assertEqual(len(Item.objects.filter(name__in=self.item_names)), ITEM_COUNT)

    def test_in_fk(self):
        self.assertEqual(len(Item.objects.filter(fk__in=self.item_ids)), ITEM_COUNT)

    def test_ineff_pk(self):
        with self.assertNumQueries(1):
            items = list(Item.objects.filter(pk__ineff=self.item_ids))
        self.assertEqual(len(items), ITEM_COUNT)
        self.assertIn('unnest(', connection.queries[-1]['sql'])

    def test_ineff_id(self):
        with self.assertNumQueries(1):
            items = list(Item.objects.filter(id__ineff=self.item_ids))
        self.assertEqual(len(items), ITEM_COUNT)
        self.assertIn('unnest(', connection.queries[-1]['sql'])

    def test_ineff_name(self):
        with self.assertNumQueries(1):
            items = list(Item.objects.filter(name__ineff=self.item_names))
        self.assertEqual(len(items), ITEM_COUNT)
        self.assertIn('unnest(', connection.queries[-1]['sql'])

    def test_ineff_fk(self):
        with self.assertNumQueries(1):
            items = list(Item.objects.filter(fk__ineff=self.item_ids))
        self.assertEqual(len(items), ITEM_COUNT)
        self.assertIn('unnest(', connection.queries[-1]['sql'])
