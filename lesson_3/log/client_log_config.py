import logging

logger = logging.getLogger('app.client')

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")
file_handler = logging.FileHandler(filename='client_log.txt', encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.info('Тестовый запуск логирования')