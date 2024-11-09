import tkinter as tk
from tkinter import font
from methods import crypto_methods as cm
from utils import misc as m
from utils import entry_validator as e
from files import file_loader as f
from tkinter import ttk
from tkinter import scrolledtext


class CipherWindow:
    def __init__(self, root, title, key_type, text_type, encrypt_func, decrypt_func, default_size):
        """
        Initializes the CipherWindow class with attributes necessary for encryption/decryption.

        Parameters:
            root (tk.Tk): The main Tkinter root window.
            title (str): Title of the window.
            key_type (type): Expected type of key input.
            text_type (type): Expected type of text input.
            encrypt_func (callable): Encryption function.
            decrypt_func (callable): Decryption function.
            default_size (str): Default size of the window.
        """
        self.root = root
        self.title = title
        self.key_type = key_type
        self.text_type = text_type
        self.encrypt_func = encrypt_func
        self.decrypt_func = decrypt_func
        self.default_size = default_size
        self.alphabet = m.create_spanish_alphabet()  # Custom Spanish alphabet

    def open_window(self):
        """
        Opens a new window with fields for text input, key input, and buttons for encryption/decryption.
        Sets up a custom scrollbar style, and configures validation and display of encrypted/decrypted results.
        """
        window = tk.Toplevel(self.root)
        window.title(self.title)
        window.geometry(self.default_size)
        window.pack_propagate(True)

        # Custom scrollbar style for a darker theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Vertical.TScrollbar",
                        gripcount=0,
                        background="#333333",
                        darkcolor="#333333",
                        lightcolor="#666666",
                        troughcolor="#222222",
                        bordercolor="#444444",
                        arrowcolor="white")

        # Main label displaying the window title
        label = tk.Label(window, text=self.title, font=("Arial", 12, "bold"))
        label.pack(pady=10)

        # Text input field label and entry
        input_label = tk.Label(
            window, text="Introduce el texto:", font=("Arial", 10))
        input_label.pack(pady=5)
        input_entry = tk.Entry(window, width=30)
        input_entry.pack(pady=5)

        # Key input field label and entry
        input_label_key = tk.Label(
            window, text="Introduce la clave:", font=("Arial", 10))
        input_label_key.pack(pady=5)
        input_key = tk.Entry(window, width=30)
        input_key.pack(pady=5)

        # Output area with a label, scrollable text, and custom scrollbar
        output_label = tk.Label(window, text="Resultado:", font=("Arial", 10))
        output_label.pack(pady=5)
        output_frame = tk.Frame(window)
        output_frame.pack()
        output_text = tk.Text(output_frame, width=30,
                              height=5, wrap="word", state="disabled")
        output_text.grid(row=0, column=0)
        scrollbar = ttk.Scrollbar(
            output_frame, command=output_text.yview, style="Custom.Vertical.TScrollbar")
        output_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        def validate_input(raw_input, expected_type):
            """
            Validates the input based on type and alphabet constraints, allowing only valid Spanish characters.

            Parameters:
                raw_input (str): Input to validate.
                expected_type (type): Expected data type for the input.

            Returns:
                str or Exception: Validated input or an Exception if validation fails.
            """
            try:
                result = e.is_blank(raw_input)
                if isinstance(result, Exception):
                    return result

                result = e.validate_type(raw_input, expected_type)
                if isinstance(result, Exception):
                    return result

                if expected_type == str:
                    result = e.all_characters_in_alphabet(raw_input)
                    if isinstance(result, Exception):
                        return result

                return raw_input
            except Exception as exp:
                print(f"Error de validación: {exp}")
                return exp

        def display_message(message):
            """
            Displays a message in the output_text widget, clearing previous content.

            Parameters:
                message (str): Message to display.
            """
            output_text.config(state="normal")
            output_text.delete("1.0", tk.END)
            output_text.insert("1.0", message)
            output_text.config(state="disabled")

        def perform_action(action_func):
            """
            Validates inputs, handles errors, and performs encryption or decryption using the given function.

            Parameters:
                action_func (callable): Function to execute (either encryption or decryption).
            """
            text = input_entry.get()
            key = input_key.get()

            text_result = validate_input(text, self.text_type)
            key_result = validate_input(key, self.key_type)

            error_messages = []

            if isinstance(text_result, Exception):
                error_messages.append(f"Texto inválido: {text_result}")

            if isinstance(key_result, Exception):
                error_messages.append(f"Clave inválida: {key_result}")

            if error_messages:
                display_message("\n".join(error_messages))
            else:
                result = action_func(text_result.upper(), key_result.upper(
                ) if self.key_type == str else int(key_result))
                display_message(result)

        # Buttons for encryption and decryption
        encrypt_button = tk.Button(
            window, text="Cifrar", command=lambda: perform_action(self.encrypt_func))
        encrypt_button.pack(pady=10)
        decrypt_button = tk.Button(
            window, text="Descifrar", command=lambda: perform_action(self.decrypt_func))
        decrypt_button.pack(pady=5)


def open_about_window():
    """
    Opens a window displaying author details and version information, reading further details from a text file.
    """
    about_window = tk.Toplevel(root)
    about_window.title("Acerca de")
    about_window.geometry("500x400")

    title_font = font.Font(family="Arial", size=16, weight="bold")
    author_text = """
    Ismael Sandoval Aguilar (2024)\n
    Versión 1.0.1
    """
    title_label = tk.Label(about_window, text=author_text,
                           font=title_font, anchor="center")
    title_label.pack(pady=10)

    info_text = open(f.load_file('info_text', 'txt'), "r").read()

    text_widget = scrolledtext.ScrolledText(
    about_window, font=("Arial", 12), wrap="word")
    text_widget.insert("1.0", info_text)
    text_widget.config(state="disabled")
    text_widget.pack(fill="both", expand=True, padx=10, pady=10)



def open_source_code_window():
    """
    Opens a new window with the source code information, loading content from a text file, 
    and displaying it in a ScrolledText widget.
    """
    source_code_window = tk.Toplevel(root)
    source_code_window.title("Código fuente")
    source_code_window.geometry("500x400")

    info_text = open(f.load_file('source_code', 'txt'), "r").read()

    text_widget = scrolledtext.ScrolledText(
        source_code_window, font=("Arial", 10), wrap="word")
    text_widget.insert("1.0", info_text)
    text_widget.config(state="disabled")
    text_widget.pack(fill="both", expand=True, padx=10, pady=10)


# Función principal que abre la ventana principal
def open_main_window():
    """
    Opens the main application window, which provides options for selecting different encryption methods.
    Each encryption method opens a separate CipherWindow for encryption and decryption, and additional
    options allow viewing source code, 'About' information, and exiting the application.

    Returns:
    None
    """
    # Define the main application window
    global root
    root = tk.Tk()  # Initializes the root Tkinter window
    root.title("Opciones de Cifrado")  # Sets the window title
    root.geometry("300x310")  # Defines the main window size

    default_size = "500x370"  # Default size for encryption method windows

    # Main label in the main window
    label = tk.Label(
        root, text="Selecciona un Método de Cifrado", font=("Arial", 14))
    label.pack(pady=10)  # Adds padding for spacing

    # Create instances of CipherWindow for each encryption method

    # Transposition Cipher
    transposition_window = CipherWindow(
        root,
        title="Cifrado de Transposición",
        key_type=str,               # Specifies that the key is a string
        text_type=str,              # Specifies that the text is a string
        # Encryption function for Transposition Cipher
        encrypt_func=cm.transposition_cipher,
        # Decryption function for Transposition Cipher
        decrypt_func=cm.transposition_decipher,
        default_size=default_size
    )

    # Caesar Cipher
    caesar_window = CipherWindow(
        root,
        title="Cifrado de César",
        key_type=int,               # Specifies that the key is an integer
        text_type=str,              # Specifies that the text is a string
        encrypt_func=cm.caesar_cipher,  # Encryption function for Caesar Cipher
        decrypt_func=cm.caesar_decipher,  # Decryption function for Caesar Cipher
        default_size=default_size
    )

    # Vigenère Cipher
    vigenere_window = CipherWindow(
        root,
        title="Cifrado de Vigenére",
        key_type=str,               # Specifies that the key is a string
        text_type=str,              # Specifies that the text is a string
        encrypt_func=cm.vigenere_cipher,  # Encryption function for Vigenère Cipher
        decrypt_func=cm.vigenere_decipher,  # Decryption function for Vigenère Cipher
        default_size=default_size
    )

    # Buttons for each encryption method, linking to each CipherWindow instance's open_window method
    btn_transposition = tk.Button(
        root, text="Cifrado de Transposición", command=transposition_window.open_window
    )
    btn_transposition.pack(pady=5)  # Adds padding for spacing

    btn_caesar = tk.Button(
        root, text="Cifrado de César", command=caesar_window.open_window
    )
    btn_caesar.pack(pady=5)  # Adds padding for spacing

    btn_vigenere = tk.Button(
        root, text="Cifrado de Vigenére", command=vigenere_window.open_window
    )
    btn_vigenere.pack(pady=5)  # Adds padding for spacing

    # Additional buttons (not requiring a CipherWindow)

    # Button to open the source code window
    btn_source_code = tk.Button(
        root, text="Código Fuente", command=open_source_code_window
    )
    btn_source_code.pack(pady=5)  # Adds padding for spacing

    # Button to open the "About" window
    btn_about = tk.Button(
        root, text="Acerca de", command=open_about_window
    )
    btn_about.pack(pady=5)  # Adds padding for spacing

    # Button to exit the application
    btn_exit = tk.Button(
        root, text="Salir", command=root.destroy
    )
    btn_exit.pack(pady=5)  # Adds padding for spacing

    # Start the main event loop to run the application
    root.mainloop()
