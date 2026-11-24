import hashlib
import json
import tempfile
from decimal import Decimal
from io import StringIO
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, override_settings

from products.models import Category, Product
from products.serializers import ProductSerializer


class ApprovedImageBatchTests(TestCase):
    def setUp(self):
        self.media = tempfile.TemporaryDirectory()
        self.addCleanup(self.media.cleanup)
        self.override = override_settings(MEDIA_ROOT=self.media.name)
        self.override.enable()
        self.addCleanup(self.override.disable)
        category = Category.objects.create(name='Consumables')
        self.container = Product.objects.create(
            name='Existing containers', sku='CW-017', slug='existing-container', category=category,
            price=Decimal('123.45'), stock=7, is_active=False, is_featured=True,
            image='products/previous-container.png',
        )
        Product.objects.create(name='Slides', sku='CW-001-SLIDES', category=category)
        self.unrelated = Product.objects.create(name='Unrelated', sku='OTHER', category=category, image='products/other.png')

    def test_apply_is_idempotent_and_preserves_existing_commercial_fields(self):
        for _ in range(2):
            call_command('apply_product_image_batch', 1, stdout=StringIO())
        self.assertEqual(Product.objects.count(), 18)  # 17 mapped listings + unrelated
        self.container.refresh_from_db()
        self.assertEqual(self.container.price, Decimal('123.45'))
        self.assertEqual(self.container.stock, 7)
        self.assertEqual(self.container.slug, 'existing-container')
        self.assertFalse(self.container.is_active)
        self.assertTrue(self.container.is_featured)
        self.assertIn('30 ml', self.container.name)
        self.unrelated.refresh_from_db()
        self.assertEqual(self.unrelated.image.name, 'products/other.png')
        self.assertEqual(ProductSerializer(self.container).data['image'], '/media/' + self.container.image.name)
        items = json.loads((Path(settings.BASE_DIR) / 'docs/product-images/batch-01.json').read_text())['items']
        self.assertEqual(len(items), 20)
        self.assertEqual(len(list(Path(self.media.name).rglob('*.png'))), 20)
        for item in items:
            path = Path(self.media.name) / item['asset'].removeprefix('static/assets/')
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item['sha256'])
        new = Product.objects.get(sku='CAT-P03-I02')
        self.assertIsNone(new.price)
        self.assertEqual(new.stock, 0)  # model default, never fabricate inventory

    def test_dry_run_does_not_write_media_or_database(self):
        for batch in (1, 2):
            call_command('apply_product_image_batch', batch, dry_run=True, stdout=StringIO())
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(list(Path(self.media.name).rglob('*')), [])

    def test_conflicting_media_is_not_overwritten(self):
        from django.core.management.base import CommandError
        for batch in (1, 2):
            with self.subTest(batch=batch):
                records = Path(settings.BASE_DIR) / f'static/content/product-images-batch-{batch:02d}.json'
                record = json.loads(records.read_text())['products'][0]
                path = Path(self.media.name) / record['image'].removeprefix('assets/')
                path.parent.mkdir(parents=True)
                path.write_bytes(b'Existing user image')
                with self.assertRaises(CommandError):
                    call_command('apply_product_image_batch', batch, stdout=StringIO())
                self.assertEqual(path.read_bytes(), b'Existing user image')
                self.assertEqual(Product.objects.count(), 3)

    def test_batch_two_preserves_batch_one_and_existing_commercial_fields(self):
        call_command('apply_product_image_batch', 1, stdout=StringIO())
        first_batch = list(Product.objects.order_by('pk').values())
        existing = Product.objects.create(
            name='Existing pipettes', sku='CAT-P07-I01', slug='existing-pipettes',
            category=self.container.category, price=Decimal('456.78'), stock=9,
            is_active=False, is_featured=True, image='products/previous-pipettes.png',
        )
        for _ in range(2):
            call_command('apply_product_image_batch', 2, stdout=StringIO())
        self.assertEqual(Product.objects.count(), 38)  # 17 + 20 batch listings + unrelated
        self.assertEqual(
            list(Product.objects.filter(pk__in=[p['id'] for p in first_batch]).order_by('pk').values()),
            first_batch,
        )
        existing.refresh_from_db()
        self.assertEqual(existing.name, 'Automatic micropipettes')
        self.assertEqual(existing.price, Decimal('456.78'))
        self.assertEqual(existing.stock, 9)
        self.assertEqual(existing.slug, 'existing-pipettes')
        self.assertEqual(existing.category_id, self.container.category_id)
        self.assertFalse(existing.is_active)
        self.assertTrue(existing.is_featured)
        self.assertEqual(ProductSerializer(existing).data['image'], '/media/' + existing.image.name)
        new = Product.objects.get(sku='CAT-P12-I04')
        self.assertIsNone(new.price)
        self.assertEqual(new.stock, 0)
        self.assertIn('100 tests', new.description)
        self.assertEqual(len(list(Path(self.media.name).rglob('*.png'))), 40)
        for batch in (1, 2):
            audit = Path(settings.BASE_DIR) / f'docs/product-images/batch-{batch:02d}.json'
            for item in json.loads(audit.read_text())['items']:
                path = Path(self.media.name) / item['asset'].removeprefix('static/assets/')
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item['sha256'])
