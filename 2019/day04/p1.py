def is_double(password):
    """
    Check if the given password contains at least one pair of adjacent digits that are the same.
    
    Args:
        password (list): A list of digits representing a password.

    Returns:
        bool: True if there is a pair of adjacent digits that are the same, otherwise False.
    """
    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            return True
    return False

def is_increasing(password):
    """
    Check if the given password has digits in non-decreasing order.
    
    Args:
        password (list): A list of digits representing a password.

    Returns:
        bool: True if the password has digits in non-decreasing order, otherwise False.
    """

    return password == sorted(password)

def int_to_digits_array(n: int) -> list:
    """
    Convert an integer to a list of its digits.
    
    Args:
        n (int): The integer to be converted.

    Returns:
        list: A list of digits representing the integer.
    """
    digits = []
    while n > 0:
        digit = n % 10  # Get the last digit of the number
        digits.append(digit)  # Add the digit to the list
        n = n // 10  # Remove the last digit from the number

    return digits[::-1]  # Reverse the list to get the original order of digits

def get_valid_passwords(min, max):
    """
    Find valid passwords within a given range (inclusive) based on specific rules.
    
    A password is valid if:
    1. It contains at least one pair of adjacent digits that are the same.
    2. Its digits are in non-decreasing order.
    
    Args:
        min (int): The lower bound of the range.
        max (int): The upper bound of the range.

    Returns:
        list: A list of valid password integers within the given range.
    """
    passwords = []
    for numb in range(min, max):
        digits = int_to_digits_array(numb)
        if not is_double(digits): continue
        if not is_increasing(digits): continue
        passwords.append(numb)
    return passwords

if __name__ == "__main__":
    raw = "265275-781584"
    # Calculate the number of valid passwords within the given range and print the result
    print("Part 1: ", len(get_valid_passwords(*map(int, raw.split("-")))))
