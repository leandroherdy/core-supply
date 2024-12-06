import io

import pandas as pd
import requests


class CSVLoader:
    """
    Data uploader in CSV format.
    """

    @staticmethod
    def load_data(url):
        """
         Loads the data from a CSV URL and returns it as a list of dictionaries.
        :param url: URL of the CSV file.
        :return: List of dictionaries or None in case of error.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
            df.columns = [
                'gender', 'name.title', 'name.first', 'name.last', 'location.street', 'location.city',
                'location.state', 'location.postcode', 'location.coordinates.latitude',
                'location.coordinates.longitude', 'location.timezone.offset', 'location.timezone.description', 'email',
                'dob.date', 'dob.age', 'registered.date', 'registered.age', 'phone', 'cell', 'picture.large',
                'picture.medium', 'picture.thumbnail'
            ]
            data = df.to_dict(orient='records')
            return data
        except Exception as e:
            print(f'Error loading CSV: {e}')
            return None
