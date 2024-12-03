import logging

def setup_logging():
    """Initializes logging configuration for the application.

        Configures logging with an INFO log level and a custom format that includes a 
        timestamp and the log message.

        Returns: 
            None
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

