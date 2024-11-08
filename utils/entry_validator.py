from utils import misc as m


class NotIntegerError(Exception):
    def __init__(self, message="La entrada no es un número entero."):
        super().__init__(message)


class NotStringError(Exception):
    def __init__(self, message="La entrada no es de tipo texto."):
        super().__init__(message)


class NotInAlphabetError(Exception):
    def __init__(self, message="La entrada contiene caracteres fuera del alfabeto español."):
        super().__init__(message)


class BlankInputError(Exception):
    def __init__(self, message="La entrada está vacía o contiene solo espacios en blanco."):
        super().__init__(message)


class NumericStringError(Exception):
    def __init__(self, message="La entrada es de tipo numérico."):
        super().__init__(message)


class InvalidKeyError(Exception):
    def __init__(self, message="La clave esta fuera de rango, elija una distinta."):
        super().__init__(message)


def validate_type(raw_input, expected_type):
    """
    Validates the type of the input based on the expected type (int or str).

    Parameters:
    raw_input: The input to be validated.
    expected_type: The expected type of the input (int or str).

    Returns:
    raw_input if validation is successful.
    Exception if validation fails.
    """
    if expected_type is int:
        try:
            int(raw_input)
            return raw_input
        except ValueError:
            return NotIntegerError()

    elif expected_type is str:
        if isinstance(raw_input, str) and raw_input.isnumeric():
            return NumericStringError()
        else:
            return raw_input

    else:
        return ValueError("Expected type must be int or str.")


def all_characters_in_alphabet(raw_input):
    """
    Checks if all characters in the input text are within the Spanish alphabet.

    Returns:
    raw_input if all characters are within the alphabet.
    Exception if validation fails.
    """
    alphabet = m.create_spanish_alphabet()
    text_upper = raw_input.upper().replace(' ', '')
    if not all(char in alphabet for char in text_upper):
        return NotInAlphabetError()
    return raw_input


def is_blank(raw_input):
    """
    Checks if the input text is blank.

    Returns:
    raw_input if the input is not blank.
    Exception if the input is blank.
    """
    if raw_input.strip() == "":
        return BlankInputError()
    return raw_input
