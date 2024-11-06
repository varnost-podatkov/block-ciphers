import json

file_path = "data/phonebook.json"


def load_phone_book(file: str) -> dict[str, str]:
    try:
        with open(file, 'br') as h:
            return json.loads(h.read())
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Could not load {file}, creating an empty phone book.")
        return {}


def save_phone_book(phone_book: dict[str, str], file: str):
    with open(file, 'wb') as h:
        h.write(json.dumps(phone_book).encode("utf8"))


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
    phone_book = load_phone_book(file_path)

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
                save_phone_book(phone_book, file_path)
                print("Phone book saved. Goodbye!")
                break
            case _:
                print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
