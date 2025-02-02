import csv
import os
from django.core.management.base import BaseCommand
from numpy.version import release

from GT_Movies_Store.models import Movie
from django.db import transaction


class Command(BaseCommand):
    help = "Import a CSV file into the database"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Path to the CSV file")

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        if not os.path.exists(csv_file):
            self.stderr.write(self.style.ERROR(f"File '{csv_file}' does not exist"))
            return

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            records = []

            for row in reader:
                records.append(Movie(
                    title=row['name'],
                    director=row['director'],
                    poster=row['email'],
                    price=row['price'],
                    release_date = row['release_date'],
                ))

            # Use bulk_create for efficiency
            with transaction.atomic():
                Movie.objects.bulk_create(records, batch_size=1000)

            self.stdout.write(self.style.SUCCESS("CSV import complete!"))
