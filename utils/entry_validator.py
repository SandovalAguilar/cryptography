from utils import misc as m

# Custom exceptions to handle various input validation errors


class NotIntegerError(Exception):
    """Exception raised when the input is not an integer."""

    def __init__(self, message="La entrada no es un número entero."):
        super().__init__(message)


class NotStringError(Exception):
    """Exception raised when the input is not a string."""

    def __init__(self, message="La entrada no es de tipo texto."):
        super().__init__(message)


class NotInAlphabetError(Exception):
    """Exception raised when the input contains characters outside the Spanish alphabet."""

    def __init__(self, message="La entrada contiene caracteres fuera del alfabeto español."):
        super().__init__(message)


class BlankInputError(Exception):
    """Exception raised when the input is blank or contains only whitespace."""

    def __init__(self, message="La entrada está vacía o contiene solo espacios en blanco."):
        super().__init__(message)


class NumericStringError(Exception):
    """Exception raised when the input is a numeric string instead of alphabetic text."""

    def __init__(self, message="La entrada es de tipo numérico."):
        super().__init__(message)


class InvalidKeyError(Exception):
    """Exception raised when a key is out of the acceptable range."""

    def __init__(self, message="La clave está fuera de rango; elija una distinta."):
        super().__init__(message)


# Validation functions for input

def validate_type(raw_input, expected_type):
    """
    Validates the type of the input based on the expected type (int or str).

    Parameters:
        raw_input: The input to be validated.
        expected_type (type): The expected data type for the input (either int or str).

    Returns:
        raw_input if the validation is successful.
        Raises an appropriate Exception if validation fails.
    """
    if expected_type is int:
        try:
            int(raw_input)
            return raw_input
        except ValueError:
            return NotIntegerError()  # Returns exception if input is not an integer

    elif expected_type is str:
        if isinstance(raw_input, str) and raw_input.isnumeric():
            return NumericStringError()  # Returns exception if input is a numeric string
        else:
            return raw_input  # Returns the input if it is a valid string

    else:
        return ValueError("Expected type must be int or str.")


def all_characters_in_alphabet(raw_input):
    """
    Checks if all characters in the input text are within the Spanish alphabet.

    Parameters:
        raw_input (str): The input string to validate.

    Returns:
        raw_input if all characters are within the Spanish alphabet.
        Raises NotInAlphabetError if validation fails.
    """
    alphabet = m.create_spanish_alphabet()  # Gets the Spanish alphabet
    # Convert to uppercase and remove spaces
    text_upper = raw_input.upper().replace(' ', '')
    if not all(char in alphabet for char in text_upper):
        # Returns exception if any character is outside the alphabet
        return NotInAlphabetError()
    return raw_input


def is_blank(raw_input):
    """
    Checks if the input text is blank (i.e., empty or whitespace only).

    Parameters:
        raw_input (str): The input string to check.

    Returns:
        raw_input if the input is not blank.
        Raises BlankInputError if the input is blank.
    """
    if raw_input.strip() == "":
        return BlankInputError()  # Returns exception if input is blank
    return raw_input
