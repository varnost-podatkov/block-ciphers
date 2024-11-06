import json
import os
import sys

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

file_path = "data/phonebook.bin"


def load_phone_book(file: str, key: bytes) -> dict[str, str]:
    try:
        # preberemo šifrirano datoteko
        with open(file, 'br') as h:
            data = h.read()

        # razčlenimo IV in čistopis
        iv, ct = data[:16], data[16:]

        # pripravimo AES-CTR
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv)).decryptor()

        # dešifriramo

        pt = cipher.update(ct) + cipher.finalize()

        # bajte čistopisa dekodiramo po UTF-8
        # in s JSON niz pretvorimo v pythonovski slovar
        return json.loads(pt.decode("utf8"))
    except FileNotFoundError:
        print(f"Could not load {file}, creating an empty phone book.")
        return {}
    except (UnicodeDecodeError, json.JSONDecodeError):
        # Smo dešifrirali, samo vsebina nima smisla
        print(f"Could not load decrypted data into a dictionary, maybe key is incorrect, aborting.")
        sys.exit(1)


def save_phone_book(phone_book: dict[str, str], file: str, key: bytes):
    # ustvarimo naključni IV
    iv = os.urandom(16)

    # slovar zapišemo v format JSON in ga postrojimo z UTF-8
    pt = json.dumps(phone_book).encode("utf8")

    # instanciramo AES-CTR
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv)).encryptor()

    # šifriramo čistopis
    ct = cipher.update(pt) + cipher.finalize()

    # shranimo IV in čistopis
    with open(file, 'wb') as h:
        h.write(iv)
        h.write(ct)


def add_contact(phone_book: dict[str, str], name: str, number: str):
    phone_book[name] = number
    print(f'Contact {name} added with number {number}.')


def search_contact(phone_book: dict[str, str], query: str):
    hits = [(name, number) for name, number in phone_book.items() if name.find(query) != -1]

    if hits:
        print(f"Found {len(hits)} hits: ")
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
        print()
        choice = input("Phone Book Menu (1 - Add / 2 - Search / 3 - Exit): ")

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
