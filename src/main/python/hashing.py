import hashlib
from configparser import ConfigParser

def select_hash_algorithm(day):
    """
    Selects the hash algorithm based on the day of the month.
    """
    return 'sha256' if day % 2 == 0 else 'md5'

def calculate_file_hash(file_path, day):
    """
    Calculates the hash of a file using the selected algorithm.
    """
    calculated_hash = hashlib.new(select_hash_algorithm(day))

    with open(file_path, 'rb') as file:
        for block in iter(lambda: file.read(4096), b""):
            calculated_hash.update(block)

    return calculated_hash.hexdigest()

def calculate_mac(hash_value, token, day):
    """
    Calculates the Message Authentication Code (MAC) using the hash and token.
    """
    calculated_mac = hashlib.new(select_hash_algorithm(day + 1))

    if day == 0:
        calculated_mac.update((hash_value + token).encode())
    else:
        calculated_mac.update((token + hash_value).encode())

    return calculated_mac.hexdigest()

def get_hash(name, date_today):
    """
    Calculates the hash of a file using different algorithms and applies a Message Authentication Code (MAC).
    """
    day = int(date_today.strftime('%d'))

    # Calculate the file hash
    hash_value = calculate_file_hash(name, day)

    # Read the token from the configuration file
    config = ConfigParser()
    config.read("config.ini")
    token = config.get("HASHING", "token")

    # Calculate the MAC using the hash and token
    mac_value = calculate_mac(hash_value, token, day)

    return mac_value
