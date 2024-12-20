import numpy as np
from utils import misc as m
from utils import entry_validator as e
from textwrap import wrap


def transposition_cipher(text: str, key: str) -> str:
    """
    Applies a columnar transposition cipher to the input text based on a given key.

    Parameters:
    text (str): The text to be encrypted using the transposition cipher.
    key (str): The key used to define the column order. The key is sorted alphabetically to determine
    the reordering of columns.

    Returns:
    ciphered_array (str): The encrypted text, where each "column" of the original text is rearranged
    according to the order defined by the sorted key.
    """
    # Step 1: Divide text into columns based on the length of the key
    text = m.split_sentence_into_columns(text, columns=len(key))

    # Step 2: Sort the key to determine the column rearrangement order
    indexes = [key.index(char) for char in sorted(list(key))]

    # Step 3: Reorder columns in the text according to the sorted key's indexes
    ciphered_array = m.columns_to_words(text[:, indexes])

    # Step 4: Combine columns to form the final ciphered text
    return ' '.join(ciphered_array)


def transposition_decipher(text: str, key: str) -> str:
    """
    Deciphers a text encoded using a columnar transposition cipher, where columns are reordered according to the specified key.

    Parameters:
    text (str): The encrypted text to be deciphered. Spaces are removed for processing.
    key (str): The key string used to determine the column order.

    Returns:
    str: The deciphered text, with characters reordered back into their original form.
    """
    # Remove spaces from the text for consistent processing
    text = text.replace(' ', '')

    # Calculate the number of rows needed to accommodate the text in columns based on the key length
    rows = int(np.ceil(len(text) / len(key)))

    # Split the text into chunks representing rows in the transposition table
    chunked_text = wrap(text, rows)

    # Determine the column order based on alphabetical ordering of the key
    indexes = [sorted(list(key)).index(char) for char in key]

    # Reorder the chunks according to the derived column order
    chunked_text = [chunked_text[i] for i in indexes]

    # Use the utility function to transpose columns back into rows
    deciphered_array = m.lists_to_columns(chunked_text)

    # Concatenate the transposed rows to form the final deciphered text
    deciphered_text = [' '.join(row) for row in deciphered_array]

    return ' '.join(deciphered_text)


def caesar_cipher(text: str, key: int) -> str:
    """
    Encrypts the given text using a Caesar cipher with the provided key.

    Parameters:
    text (str): The text to be encrypted.
    key (int): The number of positions to shift each character.

    Returns:
    str: The encrypted (ciphered) message.
    """
    # Retrieve the Spanish alphabet, assuming this function provides the uppercase alphabet including 'Ñ'.
    spanish_alphabet = m.create_spanish_alphabet()

    try:
        # Shift each character in the text by the key.
        ciphered_text = [(spanish_alphabet.index((char)) + key) % len(spanish_alphabet)
                         for char in text]

        # Convert the shifted indices back to characters.
        ciphered_text = [spanish_alphabet[index] for index in ciphered_text]
    except Exception as exp:
        print(exp)
        return e.InvalidKeyError()

    # Join and return the encrypted message as a string.
    return ''.join(ciphered_text)


def caesar_decipher(text: str, key: int) -> str:
    """
    Decrypts the given text that was encrypted using a Caesar cipher with the provided key.

    Parameters:
    text (str): The text to be decrypted.
    key (int): The number of positions used during encryption.

    Returns:
    str: The decrypted (deciphered) message.
    """
    # Retrieve the Spanish alphabet, assuming this function provides the uppercase alphabet including 'Ñ'.
    spanish_alphabet = m.create_spanish_alphabet()

    try:
        # Shift each character in the text by the key in the reverse direction.
        deciphered_text = [(spanish_alphabet.index((char)) - key) % len(spanish_alphabet)
                           for char in text]

    # Convert the shifted indices back to characters.
        deciphered_text = [spanish_alphabet[index]
                           for index in deciphered_text]
    except Exception as exp:
        print(exp)
        return e.InvalidKeyError()

    # Join and return the decrypted message as a string.
    return ''.join(deciphered_text)


def vigenere_cipher(text: str, key: str) -> str:
    """
    Encrypts the given text using the Vigenère cipher with the provided key. 
    It works with the Spanish alphabet, including 'Ñ'.

    Parameters:
    text (str): The plain text to be encrypted.
    key (str): The key used for encryption, repeated as necessary to match the length of the text.

    Returns:
    str: The encrypted (ciphered) message.
    """
    # Retrieve the Spanish alphabet, assuming this function provides the uppercase alphabet including 'Ñ'.
    spanish_alphabet = m.create_spanish_alphabet()

    # Adjust the key to match the length of the text by repeating it.
    key = m.fill_text(key, len(text))

    # Encrypt the text:
    # For each character in the text, shift it by the position of the corresponding key character in the alphabet.
    ciphered_text = [(spanish_alphabet.index((text[index])) + (spanish_alphabet.index((key[index]))))
                     % len(spanish_alphabet) for index in range(len(text))]

    # Convert the shifted indices back to characters.
    ciphered_text = [spanish_alphabet[index] for index in ciphered_text]

    # Join the list of characters to form the final encrypted message.
    return ''.join(ciphered_text)


def vigenere_decipher(text: str, key: str) -> str:
    """
    Decrypts the given text that was encrypted using the Vigenère cipher with the provided key.
    It works with the Spanish alphabet, including 'Ñ'.

    Parameters:
    text (str): The encrypted (ciphered) text to be decrypted.
    key (str): The key used during encryption, repeated as necessary to match the length of the text.

    Returns:
    str: The decrypted (deciphered) message.
    """
    # Retrieve the Spanish alphabet, assuming this function provides the uppercase alphabet including 'Ñ'.
    spanish_alphabet = m.create_spanish_alphabet()

    # Adjust the key to match the length of the text by repeating it.
    key = m.fill_text(key, len(text))

    # Decrypt the text:
    # For each character in the text, shift it by the position of the corresponding key character in reverse.
    deciphered_text = [(spanish_alphabet.index((text[index])) - (spanish_alphabet.index((key[index]))))
                       % len(spanish_alphabet) for index in range(len(text))]

    # Convert the shifted indices back to characters.
    deciphered_text = [spanish_alphabet[index] for index in deciphered_text]

    # Join the list of characters to form the final decrypted message.
    return ''.join(deciphered_text)
