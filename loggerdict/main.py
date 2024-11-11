import json
import logging
import logging.config
from pathlib import Path

from loggerdict import logging_configs


def setup_logging(log_config_path:Path):
    with open(log_config_path, 'r') as file:
        config = json.loads(file.read())
    logging.config.dictConfig(config)

def main():
    log_config_dir: Path = Path(Path(__file__).parent, 'logging_configs')
    setup_logging(Path(log_config_dir, 'log_to_stdout.json'))
    # Create loggers
    logger = logging.getLogger('my_module')

    # Example usage
    logger.debug('This is a debug message.')
    logger.info('This is an info message.')
    logger.error('This is an error message.')



if __name__ == '__main__':
    main()