from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Logging levels with color coding
INFO = f"{Fore.CYAN}[INFO]{Style.RESET_ALL}"
WARNING = f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL}"
ERROR = f"{Fore.RED}[ERROR]{Style.RESET_ALL}"


def log_message(level, message):
    """
    Prints a log message with the specified level (INFO, WARNING, ERROR).
    """
    print(f"{level} {message}")
