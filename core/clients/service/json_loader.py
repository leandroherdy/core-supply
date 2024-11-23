import io

import pandas as pd
import requests


class JSONLoader:
    """
    Data loader in JSON format.
    """

    def load_data(self, url):
        """
        Loads data from a URL and returns it as a list of dictionaries.

        :param url: The URL of the JSON data.
        :return: List of dictionaries or None if an error occurs.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = pd.read_json(io.BytesIO(response.content))
            return data.to_dict(orient='records')
        except Exception as e:
            print(f'Error loading JSON: {e}')
            return None
