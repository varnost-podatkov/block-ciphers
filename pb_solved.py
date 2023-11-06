import json
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

file_path = "data/phonebook.bin"


def load_phone_book(file, key):
    try:
        with open(file, 'br') as h:
            data = h.read()
        iv, ct = data[:16], data[16:]

        decryptor = Cipher(algorithms.AES(key), modes.CTR(iv)).decryptor()
        pt = decryptor.update(ct) + decryptor.finalize()

        return json.loads(pt)

    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Could not load {file}, creating an empty phone book")
        phone_book = {}
    return phone_book


def save_phone_book(phone_book, file, key):
    pt = json.dumps(phone_book).encode("utf8")
    iv = os.urandom(16)

    encryptor = Cipher(algorithms.AES(key), modes.CTR(iv)).encryptor()
    ct = encryptor.update(pt) + encryptor.finalize()

    with open(file, 'wb') as file:
        file.write(iv + ct)


def add_contact(phone_book, name, number):
    phone_book[name] = number
    print(f'Contact {name} added with number {number}.')


def search_contact(phone_book, query):
    hits = [(name, number) for name, number in phone_book.items() if name.find(query) != -1]

    if hits:
        print(f"Found {len(hits)} hits:")
        for name, number in hits:
            print(f"- {name}: {number}")
    else:
        print(f"No entries for query '{query}'")


def main():
    """try:
        key = bytes.fromhex(input("Enter key as HEX: "))
        assert len(key) == 16
    except (ValueError, AssertionError):
        print("Invalid key, aborting.")
        return"""
    
    key = bytes.fromhex("4552a7202d04fb997f31c649d5533255")

    phone_book = load_phone_book(file_path, key)
    print(f"Found {len(phone_book)} contacts.")

    while True:
        print("\nPhone Book Menu:")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        match choice:
            case '1':
                name = input("Enter contact name: ")
                number = input("Enter contact number: ")
                add_contact(phone_book, name, number)
            case '2':
                name = input("Enter contact name to search: ")
                search_contact(phone_book, name)
            case '3':
                save_phone_book(phone_book, file_path, key)
                print("Phone book saved. Goodbye!")
                break
            case _:
                print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
