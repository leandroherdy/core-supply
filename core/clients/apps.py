from django.apps import AppConfig

from core.clients.service.client_data_processor import DataProcessor


class ClientsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.clients'

    def ready(self):
        """
        Overrides the ready method to initialize the data processor.
        """
        self.initialize_data_processor()

    def initialize_data_processor(self):
        """
        Initializes the DataProcessor and preloads data into memory.

        Processes data from predefined JSON and CSV URLs and stores the
        results in memory for API use. Logs any errors during data loading.
        """
        self.data_processor = DataProcessor()

        try:
            json_file_path = 'https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json'
            csv_file_path = 'https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv'

            self.data_processor.process_data(json_file_path, csv_file_path)
            print(f"Data successfully preloaded. Total records: {len(self.data_processor.get_data())}")
        except Exception as e:
            print(f"Error preloading data: {e}")
