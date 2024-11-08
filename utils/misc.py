import numpy as np


def generate_pdf():
    # Aquí iría la funcionalidad para generar el PDF con el código fuente
    print("Generando PDF con el código fuente...")


def lists_to_columns(lists):
    """
    Converts a list of strings into a 2D NumPy array, where each string is treated as a row, 
    and each character in the string is a separate column.
    Then, it transposes the array, converting rows into columns.

    Parameters:
    lists (list of str): A list of words or strings where each word represents a row in the resulting array.

    Returns:
    np.ndarray: A 2D NumPy array where each original word's characters are now columns.
    """
    # Convert each word in the list to a list of characters, then create a 2D NumPy array
    array = np.array([list(word) for word in lists])

    # Transpose the array so rows become columns
    transposed_array = array.T
    return transposed_array


def word_to_alphabet_positions(word):
    """
    Converts each character in a given word to its corresponding position in the alphabet, 
    assuming 'A' is 0, 'B' is 1, ..., 'Z' is 25.
    This function is case-insensitive, so it will handle both uppercase and lowercase letters.

    Parameters:
    word (str): The word to be converted to alphabet positions.

    Returns:
    list of int: A list of integer positions representing each character's position in the alphabet.
    """
    # Convert word to uppercase, then calculate each character's position by subtracting 'A' (ASCII value 65) from the character's ASCII value
    return [ord(char) - ord('A') for char in word.upper()]


def create_spanish_alphabet():
    """
    Creates and returns a list containing the uppercase letters of the Spanish alphabet.ß

    Returns:
    list: A list of characters representing the uppercase Spanish alphabet.
    """
    # Create a list of the uppercase Spanish alphabet, including the letter 'Ñ'.
    alphabet = list("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")

    # Return the alphabet as a list of characters.
    return alphabet


def fill_text(text, length):
    """
    Fills the input text until it reaches the specified length by repeating the original text.

    If the text is shorter than the desired length, it will repeat the text until the length is met.
    If the desired length is smaller than or equal to the text's length, it will return the original text.

    Parameters:
    text (str): The text to be filled.
    length (int): The desired length of the output string.

    Returns:
    str: The text filled up to the specified length.
    """
    # If the length is less than or equal to the original text, return the original text.
    repeated_text = text[:length] if length <= len(
        text) else (text * (length // len(text) + 1))[:length]

    return repeated_text


def split_sentence_into_columns(sentence, columns):
    """
    Splits a sentence into columns, filling each column with consecutive letters from the sentence. 
    Spaces are removed, and letters are wrapped to fit into rows if needed.

    Parameters:
    sentence (str): The sentence to be split into columns.
    columns (int): The number of columns to create.

    Returns:
    np.ndarray: A 2D NumPy array where each row contains a segment of the sentence, 
    with letters wrapped as necessary.
    """
    # Remove spaces from the sentence and create a NumPy array of letters
    letters = np.array(list(sentence.replace(" ", "")))

    # Calculate the required number of rows based on the number of columns
    rows = int(np.ceil(len(letters) / columns))

    # Pad the letters array to ensure it fills the grid fully, wrapping extra letters if needed
    padded_letters = np.pad(letters, (0, rows * columns - len(letters)), mode='wrap')

    # Reshape the padded array into the specified number of rows and columns
    result = padded_letters.reshape(rows, columns)
    return result


def columns_to_words(array):
    """
    Concatenates characters in each column of a 2D array into words, treating each column as a separate word. 
    Empty cells are ignored.

    Parameters:
    array (np.ndarray): A 2D NumPy array where each column represents a separate word to be formed.

    Returns:
    list of str: A list of words created by concatenating characters in each column.
    """
    # Join each character in each column to form a word, ignoring any empty cells
    words = [''.join([char for char in array[:, i] if char]) for i in range(array.shape[1])]
    return words

