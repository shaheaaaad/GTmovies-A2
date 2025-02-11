import csv

from django.contrib.sites import requests
from django.core.management.base import BaseCommand
from GT_Movies_Store.models import Movie
from datetime import datetime
import requests

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        base_image_url = "https://image.tmdb.org/t/p/w500"
        with open('mysite/data.csv', 'r') as file:
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

                tmdb_id = row["id"]
                API_KEY = "28b90a468d3ba4828915a141b58ca58e"
                TMDB_BASE_URL = "https://api.themoviedb.org/3/movie/"
                IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
                url = f"{TMDB_BASE_URL}{tmdb_id}?api_key={API_KEY}"
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()

                    poster_path = data.get("poster_path")
                    image = f"{IMAGE_BASE_URL}{poster_path}" if poster_path else None

                else:
                    image = None
                overview = row['overview']
                price = 8


                # Create Movie instance and save to the database
                movie = Movie( title =original_title, release_date =release_date, description =overview, image = image, price = price, tmdb_id = tmdb_id)
                movie.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported movies into the database'))





