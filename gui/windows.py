import tkinter as tk
from tkinter import font
from methods import crypto_methods as cm
from utils import misc as m
from utils import entry_validator as e
from files import file_loader as f
from tkinter import ttk


class CipherWindow:
    def __init__(self, root, title, key_type, text_type, encrypt_func, decrypt_func, default_size):
        self.root = root
        self.title = title
        self.key_type = key_type
        self.text_type = text_type
        self.encrypt_func = encrypt_func
        self.decrypt_func = decrypt_func
        self.default_size = default_size
        # Assuming m.create_spanish_alphabet() is defined elsewhere
        self.alphabet = m.create_spanish_alphabet()

    def open_window(self):
        window = tk.Toplevel(self.root)
        window.title(self.title)
        window.geometry(self.default_size)
        window.pack_propagate(True)

        # Set up a custom style for the scrollbar
        style = ttk.Style()
        style.theme_use('clam')  # Use a theme that allows custom styling
        style.configure("Custom.Vertical.TScrollbar",
                        gripcount=0,
                        background="#333333",  # Dark background for the scrollbar
                        darkcolor="#333333",   # Darker shade for trough
                        lightcolor="#666666",  # Lighter shade for active area
                        # Color of the trough (scrollbar track)
                        troughcolor="#222222",
                        bordercolor="#444444",  # Border color around the scrollbar
                        arrowcolor="white")    # Color of arrows, if any

        # Main label
        label = tk.Label(window, text=self.title, font=("Arial", 12, "bold"))
        label.pack(pady=10)

        # Text input field
        input_label = tk.Label(
            window, text="Introduce el texto:", font=("Arial", 10))
        input_label.pack(pady=5)
        input_entry = tk.Entry(window, width=30)
        input_entry.pack(pady=5)

        # Key input field
        input_label_key = tk.Label(
            window, text="Introduce la clave:", font=("Arial", 10))
        input_label_key.pack(pady=5)
        input_key = tk.Entry(window, width=30)
        input_key.pack(pady=5)

        # Output field with scrollable Text widget
        output_label = tk.Label(window, text="Resultado:", font=("Arial", 10))
        output_label.pack(pady=5)

        # Frame for the Text widget and Scrollbar
        output_frame = tk.Frame(window)
        output_frame.pack()

        # Use a Text widget for multiline output
        output_text = tk.Text(output_frame, width=30,
                              height=5, wrap="word", state="disabled")
        output_text.grid(row=0, column=0)

        # Add a vertical scrollbar with the custom style
        scrollbar = ttk.Scrollbar(
            output_frame, command=output_text.yview, style="Custom.Vertical.TScrollbar")
        output_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        def validate_input(raw_input, expected_type):
            """Validates the input against expected type and Spanish alphabet if needed."""
            try:
                # Blank check
                result = e.is_blank(raw_input)
                if isinstance(result, Exception):
                    return result  # Return exception if validation fails

                # Type validation
                result = e.validate_type(raw_input, expected_type)
                if isinstance(result, Exception):
                    return result  # Return exception if validation fails

                # Additional alphabet validation if type is string
                if expected_type == str:
                    result = e.all_characters_in_alphabet(raw_input)
                    if isinstance(result, Exception):
                        return result  # Return exception if validation fails

                return raw_input
            except Exception as exp:
                print(f"Validation Error: {exp}")
                return exp

        def display_message(message):
            """Displays a message in the output_text widget."""
            output_text.config(state="normal")   # Enable editing
            output_text.delete("1.0", tk.END)    # Clear previous text
            output_text.insert("1.0", message)   # Insert new message
            # Disable editing to make it read-only
            output_text.config(state="disabled")

        def perform_action(action_func):
            """Executes the encryption or decryption function after validation."""
            text = input_entry.get()
            key = input_key.get()

            # Validate text and key with the expected types
            text_result = validate_input(text, self.text_type)
            key_result = validate_input(key, self.key_type)

            # Prepare error messages
            error_messages = []

            # Check if validation for text failed
            if isinstance(text_result, Exception):
                error_messages.append(f"Texto inválido: {text_result}")

            # Check if validation for key failed
            if isinstance(key_result, Exception):
                error_messages.append(f"Clave inválida: {key_result}")

            # Display error messages if any validation failed
            if error_messages:
                combined_error_message = "\n".join(error_messages)
                display_message(combined_error_message)
            else:
                # If both text and key are valid, proceed with the action function
                result = action_func(text_result.upper(), key_result.upper(
                ) if self.key_type == str else int(key_result))
                display_message(result)

        # Encrypt button
        encrypt_button = tk.Button(
            window, text="Cifrar", command=lambda: perform_action(self.encrypt_func))
        encrypt_button.pack(pady=10)

        # Decrypt button
        decrypt_button = tk.Button(
            window, text="Descifrar", command=lambda: perform_action(self.decrypt_func))
        decrypt_button.pack(pady=5)


def open_about_window():
    """
    Opens a new window to display information about the ciphers, including author details and
    specific descriptions from a text file. This function configures the window, title, and content.

    Returns:
    None
    """
    # Create a new top-level window for "About" information
    about_window = tk.Toplevel(root)
    # Set the title of the window to "Acerca de"
    about_window.title("Acerca de")
    about_window.geometry("500x400")  # Define window size to 500x400 pixels

    # Define a custom font for the title text
    title_font = font.Font(family="Arial", size=16, weight="bold")

    # Define the author information text
    author_text = """
    Ismael Sandoval Aguilar (2024)\n
    Versión 1.0.1
    """

    # Display the author information in a bold, centered label
    title_label = tk.Label(about_window, text=author_text,
                           font=title_font, anchor="center")
    title_label.pack(pady=10)  # Add padding around the title label for spacing

    # Read the cipher information from an external file
    info_text = open(f.load_file('info_text', 'txt'), "r").read()

    # Label to display the information text, justified to the left
    label = tk.Label(about_window, text=info_text,
                     font=("Arial", 10), justify="left")
    label.pack(pady=10, padx=10)  # Add padding around the label for spacing


def open_source_code_window():
    # Crea una nueva ventana para mostrar información sobre el código fuente
    source_code_window = tk.Toplevel(root)
    source_code_window.title("Código Fuente")
    source_code_window.geometry("500x350")

    # Etiqueta principal
    label = tk.Label(source_code_window, text="Generar PDF con el Código Fuente", font=(
        "Arial", 14, "bold"))
    label.pack(pady=10)

    # Botón para generar el PDF
    btn_generate_pdf = tk.Button(
        source_code_window, text="Generar PDF", command=m.generate_pdf, font=("Arial", 12))
    btn_generate_pdf.pack(pady=20)


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
