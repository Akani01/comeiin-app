"""Apply an approved catalogue batch without resetting commercial fields."""
import hashlib
import json
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from products.models import Category, Product


class Command(BaseCommand):
    help = 'Apply an approved product-image batch; preserves existing price, stock and visibility.'

    def add_arguments(self, parser):
        parser.add_argument('batch', type=int, choices=[1, 2])
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **options):
        root = Path(settings.BASE_DIR)
        number = options['batch']
        records = json.loads((root / f'static/content/product-images-batch-{number:02d}.json').read_text())['products']
        audit = json.loads((root / f'docs/product-images/batch-{number:02d}.json').read_text())
        assets = {item['asset']: item for item in audit['items']}
        copies = {}
        for record in records:
            for view in record['gallery']:
                asset = 'static/' + view['image']
                approved = assets.get(asset)
                if not approved or approved['image_approval'] != 'approved':
                    raise CommandError(f'Unapproved asset: {asset}')
                source = root / asset
                data = source.read_bytes()
                digest = hashlib.sha256(data).hexdigest()
                if digest != approved['sha256']:
                    raise CommandError(f'Approved image changed: {asset}')
                destination = view['image'].removeprefix('assets/')
                if default_storage.exists(destination):
                    with default_storage.open(destination, 'rb') as stream:
                        if hashlib.sha256(stream.read()).hexdigest() != digest:
                            raise CommandError(f'Existing media differs; refusing overwrite: {destination}')
                else:
                    copies[destination] = data

        if options['dry_run']:
            self.stdout.write(f'Validated {len(assets)} approved images for {len(records)} listings. No changes made.')
            return

        # Files are immutable and retained on retries; all database edits are atomic.
        for destination, data in copies.items():
            saved = default_storage.save(destination, ContentFile(data))
            if saved != destination:
                raise CommandError(f'Media name collision: {destination}; no database changes made.')

        created = updated = 0
        with transaction.atomic():
            for record in records:
                category, _ = Category.objects.get_or_create(
                    name=record['category'], defaults={'slug': slugify(record['category'])}
                )
                product, is_new = Product.objects.get_or_create(
                    sku=record['id'],
                    defaults={'name': record['name'], 'slug': record['id'].lower(), 'category': category, 'badge': record['category']},
                )
                product.name = record['name']
                product.short_description = record['description']
                details = [record['description']] + [f'{key}: {value}' for key, value in record['specs'].items()]
                if record['variants']:
                    details.append(record['variantLabel'] + ': ' + '; '.join(record['variants']))
                if record['pack']:
                    details.append('Packaging: ' + record['pack'])
                product.description = '\n'.join(details)
                product.image.name = record['image'].removeprefix('assets/')
                # Existing price, stock, slug, category, visibility and featured state stay intact.
                product.save(update_fields=['name', 'short_description', 'description', 'image', 'updated_at'])
                created += int(is_new)
                updated += int(not is_new)
        self.stdout.write(self.style.SUCCESS(f'Batch {number:02d}: {created} created, {updated} updated; {len(assets)} approved images.'))
