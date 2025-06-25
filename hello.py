import json
import os

class Book:
    def __init__(self, title, author, year, is_borrowed):
        self.title = title
        self.author = author
        self.year = year
        self.is_borrowed = is_borrowed

    def __str__(self):
        return (f"Книга: {self.title}\n"
                f"Автор: {self.author}\n"
                f"Рік: {self.year}\n"
                f"Книга взята? {self.is_borrowed}\n")


class Library:
    def __init__(self):
        self.books = []
        self.load_library()

    def add_book(self):
        title = input("Введіть назву книги: ").strip().lower()
        author = input("Введіть автора книги: ").strip().lower()
        year = input("Введіть рік видання: ").strip()
        for book in self.books:
            if title == book.title:
                print("Ця книга вже є в бібліотеці\n")
                return

        book = Book(title, author, year, "Ні")
        self.books.append(book)
        self.save_books()

    def save_books(self):
        data = []
        for book in self.books:
            data.append({
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "is_borrowed": book.is_borrowed
            })

        with open("books.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_library(self):
        if os.path.exists("books.json"):
            with open("books.json", "r") as f:
                data = json.load(f)
                for book in data:
                    loaded_book = Book(book["title"],book["author"],book["year"],book["is_borrowed"])
                    self.books.append(loaded_book)

    def find_book(self, title):
        book_found = False
        for book in self.books:
            if book.title == title:
                print(book)
                book_found = True
                break

        if not book_found:
            print("Такої книги на жаль у нас немає")

    def borrow_book(self, title):
        book_found = False
        for book in self.books:
            if book.title == title and book.is_borrowed == "Ні":
                print("Ось ваша книга, обовʼязково поверніть!")
                book.is_borrowed = "Так"
                self.save_books()
                book_found = True
                break
            elif book.title == title and book.is_borrowed == "Так":
                print("На жаль цю книгу вже взяли")
                book_found = True

        if not book_found:
            print("На жаль такої книги немає в нашому асортименті")

    def return_book(self, title):
        book_found = False
        for book in self.books:
            if book.title == title and book.is_borrowed == "Так":
                print("Дякуємо що вчасно повернули!")
                book.is_borrowed = "Ні"
                self.save_books()
                book_found = True
                break
            elif book.title == title and book.is_borrowed == "Ні":
                print("Ви вже повернули цю книгу раніше.")
                book_found = True
                break

        if not book_found:
            print("У нас ніколи не було такої книги, можливо ви брали її не у нас.")

    def book_list(self):
        for book in self.books:
            print(book)


lib = Library()
choose = -1
while choose != 0:
    print("1. Додати нову книгу\n"
          "2. Взяти книгу\n"
          "3. Віддати книгу\n"
          "4. Переглянути список книг\n"
          "5. Знайти книгу\n"
          "0. Вийти")
    try:
        choose = int(input(">> "))
        if choose < 0 or choose > 5:
            raise ValueError
    except ValueError:
        print("Вводьте лише числа від 0 до 4")
    else:
        match choose:
            case 1:
                lib.add_book()
            case 2:
                lib.borrow_book(input("Введіть назву книги, яку хочете взяти: ").strip().lower())
            case 3:
                lib.return_book(input("Введіть назву книги, яку хочете повернути: ").strip().lower())
            case 4:
                lib.book_list()
            case 5:
                lib.find_book(input("Введіть назву книги, яку бажаєте знайти: ").strip().lower())