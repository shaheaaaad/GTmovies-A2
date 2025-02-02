import csv
from django.core.management.base import BaseCommand
from MovieStore.models import Movie
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open('/Users/shahdbargouthi/Desktop/GTmovieStore-A2/mysite/movies_metadata.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                original_title = row['original_title']

                release_date_str = row['release_date']  # Remove spaces
                release_date = None
                if release_date_str:
                    if "-" in release_date_str:  # YYYY-MM-DD format
                        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                    elif "/" in release_date_str:  # MM/DD/YY format
                        release_date = datetime.strptime(release_date_str, '%m/%d/%y').strftime('%Y-%m-%d')

                overview = row['overview']

                # Create Movie instance and save to the database
                movie = Movie( title =original_title, release_date =release_date, description =overview)
                movie.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported movies into the database'))
