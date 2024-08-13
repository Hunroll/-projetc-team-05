from Bot import *

global test_count, successfull_count, test_name
def assert_eq(a, b, comment: str):
    global test_count, successfull_count
    test_count += 1
    is_eq = a == b
    if (is_eq):
        successfull_count += 1
    print("<{}> is expected to be <{}> ({}) - {}".format(a, b, comment, is_eq))

def unit_test(func):
    test_name = func.__name__
    def inner()->bool:
        init_test(test_name)
        try:
            func()
        except Exception as ex:
            test_error(ex)
        finally:
            return end_test()
    return inner   

def init_test(name: str):
    global test_count, successfull_count, test_name
    test_count = 0
    successfull_count = 0
    test_name = name
    print(f"Starting test {name}")

def end_test() -> bool:
    global test_count, successfull_count, test_name
    print(f"Ending test {test_name}, passed {successfull_count}/{test_count} tests.")
    return successfull_count == test_count

def test_error(ex: Exception):
    global test_name, test_count
    test_count += 1
    print(f"Exception in test {test_name}", ex)


@unit_test
def test4():
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    # Додавання запису John до адресної книги
    book.add_record(john_record)
    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)
    # Виведення всіх записів у книзі
    # for name, record in book.data.items():
    #     print(record)
    assert_eq(str(book.find("John")), "Contact name: John, birthday: Not set, phones: 1234567890; 5555555555", "John is here")
    assert_eq(str(book.find("Jane")), "Contact name: Jane, birthday: Not set, phones: 9876543210", "Jane is here")
    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    assert_eq(str(book.find("John")), "Contact name: John, birthday: Not set, phones: 1112223333; 5555555555", "John has new number")

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    assert_eq(str(found_phone), "5555555555", "Phone is found")

    #set birthday for John
    john.add_birthday("03.08.1995")
    assert_eq(str(book.find("John")), "Contact name: John, birthday: 03.08.1995, phones: 1112223333; 5555555555", "John\'s birthday is added")

    book.save_data("testbook.dat")
    book = AddressBook.load_data("testbook.dat")
    assert_eq(str(book.find("John")), "Contact name: John, birthday: 03.08.1995, phones: 1112223333; 5555555555", "Book is loaded from file")


    jane = book.find("Jane")
    jane.add_birthday("02.01.1995")
    assert_eq(str(book.find("Jane")), "Contact name: Jane, birthday: 02.01.1995, phones: 9876543210", "Jane\'s birthday is added")

    #get upcoming birthday for my "today"
    bd_dict = book.get_upcoming_birthdays("29.07.2024")
    assert_eq(len(bd_dict) == 1 and bd_dict[0]["congratulation_date"] == "05.08.2024", True, "Upcoming birthday is john\'s, 2 days later, on Monday")

    book.delete("Jane")
    assert_eq(book.find("Jane"), None, "Jane is deleted")

    john.remove_phone("5555555555")
    assert_eq(str(book.find("John")), "Contact name: John, birthday: 03.08.1995, phones: 1112223333", "John has 1 number left")

    john.add_birthday("04.08.1995")
    assert_eq(str(book.find("John")), "Contact name: John, birthday: 04.08.1995, phones: 1112223333", "John has new birthday")

if test4():
    print("Tests passed successfully")
else:
    print("Some tests failed")
