import json
import os
import sys

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

file_path = "data/phonebook.bin"


def load_phone_book(file, key):
    try:
        # preberemo vsebino datoteke
        with open(file, 'br') as h:
            data = h.read()

        # vsebino ločimo v IV (prvih 16 bajtov) in tajnopis (preostali del)
        iv, ct = data[:16], data[16:]

        # pripravimo dešifrirani algoritem
        dec = Cipher(algorithms.AES(key), modes.CTR(iv)).decryptor()
        # dešifriramo
        pt = dec.update(ct) + dec.finalize()

        # čistopis (objekt JSON) pretvorimo v slovar
        return json.loads(pt)

    except FileNotFoundError:
        print(f"Could not load {file}, creating an empty phone book")
        return {}
    except (UnicodeDecodeError, json.JSONDecodeError):
        # Smo dešifrirali, samo vsebina nima smisla
        print(f"Could not load decrypted data into a dictionary, maybe key is incorrect, aborting.")
        sys.exit(1)


def save_phone_book(phone_book, file, key):
    # vsebino slovarja serializiramo kot objekt JSON
    pt = json.dumps(phone_book).encode("utf8")
    # izberemo naključni IV in ta mora biti pri vsakem shranjevanju drugačen 
    iv = os.urandom(16)

    # pripravimo šifrirni algoritem
    enc = Cipher(algorithms.AES(key), modes.CTR(iv)).encryptor()

    # šifriramo
    ct = enc.update(pt) + enc.finalize()

    # v datoteko shranimo IV || CT
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
    # Pozor: Podana rešitev ni varna. V njej zgolj demonstriramo pravilno uporabo
    # šifre AES-CTR z naključnim IV.
    # 1. V praksi bi morala takšna aplikacija poleg tajnosti zagotoviti še celovitost,
    # saj lahko napadalec spremeni tajnopis in tega ne bomo zaznali: AES-CTR zagotavlja
    # zgolj tajnost, celovitosti ne.
    # 2. Ključ smo za lažje poganjanje/testiranje kar statično zapisali v programsko
    # kodo. Veliko boljše bi bilo ključ npr. izpeljati iz gesla, ki ga vpiše uporabnik,
    # a je pri tem treba biti pazljiv: to je tema, ki jo bomo še obravnavali.
    # Alternativa bi bila tudi npr. spodnja koda, a to zahteva od uporabnika da pri vsakem
    # zagonu vpiše 32 znakov dolg ključ, kar je nepraktično.
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
