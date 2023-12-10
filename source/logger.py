from source.date import dateFormatted
import sys
import os
import yaml

# Obtém o diretório do script em execução
script_dir = getattr(sys, '_MEIPASS', os.path.dirname(
    os.path.abspath(sys.argv[0])))

# Constrói o caminho para o arquivo config.yaml
config_path = os.path.join(script_dir, "config.yaml")

# Abre o arquivo config.yaml
with open(config_path, 'r') as stream:
    c = yaml.safe_load(stream)

last_log_is_progress = False

COLOR = {
    'blue': '\033[94m',
    'default': '\033[99m',
    'grey': '\033[90m',
    'yellow': '\033[93m',
    'black': '\033[90m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'magenta': '\033[95m',
    'white': '\033[97m',
    'red': '\033[91m'
}

# Constrói o caminho para o arquivo de log
log_dir = os.path.join(script_dir, "logs")
os.makedirs(log_dir, exist_ok=True)  # Cria o diretório se não existir


def logger(message, progress_indicator=False, color='default'):
    global last_log_is_progress
    color_formatted = COLOR.get(color.lower(), COLOR['default'])

    formatted_datetime = dateFormatted()
    formatted_message = "[{}] => {}".format(formatted_datetime, message)
    formatted_message_colored = color_formatted + formatted_message + '\033[0m'

    # Start progress indicator and append dots to in subsequent progress calls
    if progress_indicator:
        if not last_log_is_progress:
            last_log_is_progress = True
            formatted_message = color_formatted + \
                "[{}] => {}".format(formatted_datetime,
                                    '⬆️ Processing last action..')
            sys.stdout.write(formatted_message)
            sys.stdout.flush()
        else:
            sys.stdout.write(color_formatted + '.')
            sys.stdout.flush()
        return

    if last_log_is_progress:
        sys.stdout.write('\n')
        sys.stdout.flush()
        last_log_is_progress = False

    print(formatted_message_colored)

    if c['save_log_to_file']:
        log_file_path = os.path.join(log_dir, "logger.log")
        logger_file = open(log_file_path, "a", encoding='utf-8')
        logger_file.write(formatted_message + '\n')
        logger_file.close()

    return True


def loggerMapClicked():
    logger('🗺️ New Map button clicked!')
    log_file_path = os.path.join(log_dir, "new-map.log")
    logger_file = open(log_file_path, "a", encoding='utf-8')
    logger_file.write(dateFormatted() + '\n')
    logger_file.close()
