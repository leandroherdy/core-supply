from core.clients.data_transformers.phone_formatter import PhoneFormatter
from core.clients.data_transformers.region_mapper import RegionMapper
from core.clients.data_transformers.type_classifier import TypeClassifier
from core.clients.loaders.csv_loader import CSVLoader
from core.clients.loaders.json_loader import JSONLoader


class DataProcessor:
    """ Data processor for normalising and applying business rules. """

    def __init__(self):
        self.data_in_memory = []

    def process_data(self, *urls):
        """
        Loads and processes data based on the provided URLs.
        Combines formatted data from JSON and CSV files into a single list.

        :param urls: URLs of the files (CSV or JSON).
        :return: List of processed data.
        """
        all_processed_data = []

        for url in urls:
            try:
                if url.endswith('.json'):
                    loader = JSONLoader()
                    formato = 'json'
                elif url.endswith('.csv'):
                    loader = CSVLoader()
                    formato = 'csv'
                else:
                    raise ValueError(f'File format not supported for URL: {url}')

                data = loader.load_data(url)
                if data is None:
                    raise ValueError(f'Failed to load data from URL: {url}')

                processors = {'json': self.process_json_data, 'csv': self.process_csv_data}
                processed_data = processors[formato](data)

                all_processed_data.extend(processed_data)

                print(f"Successfully processed {len(processed_data)} records from {url}")

            except Exception as e:
                print(f"Error processing URL {url}: {e}")

        self.data_in_memory.extend(all_processed_data)
        return all_processed_data

    def get_data(self):
        """
        Returns the data currently stored in memory.
        :return: List of processed data.
        """
        return self.data_in_memory

    def process_json_data(self, data):
        """
        Processes and applies business rules to JSON data, returning a list of treated user records.
        :param data: Raw JSON data to be processed.
        :return: List of processed user dictionaries.
        """
        data_processed = []
        for item in data:
            if "results" in item:
                item = item["results"]

            try:
                location = item.get("location", {})
                coordinates = location.get("coordinates", {})
                timezone = location.get("timezone", {})
                picture = item.get("picture", {})
                name = item.get("name", {})

                client = {
                    'type':
                        TypeClassifier.classify_type(
                            float(coordinates.get('longitude', 0) or 0), float(coordinates.get('latitude', 0) or 0)
                        ),
                    'gender':
                        'm' if item.get("gender", "N/A").lower() == "male" else 'f',
                    'name': {
                        'title': name.get("title", "N/A"),
                        'first': name.get("first", "N/A"),
                        'last': name.get("last", "N/A")
                    },
                    'location': {
                        'region': RegionMapper.map_state_to_region(location.get("state", "N/A")),
                        'street': location.get("street", "N/A"),
                        'city': location.get("city", "N/A"),
                        'state': location.get("state", "N/A"),
                        'postcode': location.get("postcode", "N/A"),
                        'coordinates': {
                            'latitude': coordinates.get('latitude', 'N/A'),
                            'longitude': coordinates.get('longitude', 'N/A')
                        },
                        'timezone': {
                            'offset': timezone.get("offset", "N/A"),
                            'description': timezone.get("description", "N/A")
                        }
                    },
                    'email':
                        item.get("email", "N/A"),
                    'birthday':
                        item.get("dob", {}).get("date", "N/A"),
                    'registered':
                        item.get("registered", {}).get("date", "N/A"),
                    'telephoneNumbers': [PhoneFormatter.format_phone_number(item.get("phone"))]
                                        if item.get("phone") else [],
                    'mobileNumbers': [PhoneFormatter.format_phone_number(item.get("cell"))]
                                     if item.get("cell") else [],
                    'picture': {
                        'large': picture.get("large", "N/A"),
                        'medium': picture.get("medium", "N/A"),
                        'thumbnail': picture.get("thumbnail", "N/A")
                    },
                    'nationality':
                        'BR',
                }
                data_processed.append(client)
            except Exception as e:
                print(f'Error processing item: {e}')

        return data_processed

    def process_csv_data(self, data):
        """
        Processes raw CSV data and applies business rules.

        :param data: List of dictionaries representing rows from a CSV file.
        :return: List of processed user dictionaries.
        """
        data_processed = []
        for item in data:
            try:
                client = {
                    'type':
                        TypeClassifier.classify_type(
                            float(item.get('location.coordinates.longitude', 0)),
                            float(item.get('location.coordinates.latitude', 0))
                        ),
                    'gender':
                        'm' if item.get("gender", "N/A") == "male" else 'f',
                    'name': {
                        'title': item.get("name.title", "N/A"),
                        'first': item.get("name.first", "N/A"),
                        'last': item.get("name.last", "N/A"),
                    },
                    'location': {
                        'region': RegionMapper.map_state_to_region(item.get("location.state", "N/A")),
                        'street': item.get("location.street", "N/A"),
                        'city': item.get("location.city", "N/A"),
                        'state': item.get("location.state", "N/A"),
                        'postcode': item.get("location.postcode", "N/A"),
                        'coordinates': {
                            'latitude': item.get('location.coordinates.latitude'),
                            'longitude': item.get('location.coordinates.longitude')
                        },
                        'timezone': {
                            'offset': item.get("location.timezone.offset", "N/A"),
                            'description': item.get("location.timezone.description", "N/A"),
                        }
                    },
                    'email':
                        item.get("email", "N/A"),
                    'birthday':
                        item.get("dob.date", "N/A"),
                    'registered':
                        item.get("registered.date", "N/A"),
                    'telephoneNumbers': [PhoneFormatter.format_phone_number(item.get("phone"))]
                                        if item.get("phone") else [],
                    'mobileNumbers': [PhoneFormatter.format_phone_number(item.get("cell"))]
                                     if item.get("cell") else [],
                    'picture': {
                        'large': item.get("picture.large", "N/A"),
                        'medium': item.get("picture.medium", "N/A"),
                        'thumbnail': item.get("picture.thumbnail", "N/A"),
                    },
                    'nationality':
                        'BR',
                }
                data_processed.append(client)
            except Exception as e:
                print(f'Error processing item: {e}')
        return data_processed
