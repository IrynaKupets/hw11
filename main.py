from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        # self.value = name

    @Field.value.setter
    def value(self, value):
        if value.isalpha():
            Field.value.fset(self, value)
        else:
            raise ValueError


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if value.replace("+", "").replace("(", "").replace(")", "").isdigit():
            Field.value.fset(self, value)
        else:
            raise ValueError


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            Field.value.fset(self, value)
        except:
            Field.value.fset(self, "")


class Record:
    def __init__(self, name: Name, phone: list = None, birthday: Birthday = None):
        self.name = name
        self.phone = phone
        self.birthday = birthday

    def days_to_birthday(self):
        if self.birthday:
            current_date = datetime.now().date()
            bday_year = current_date.year
            days = datetime.strptime(self.birthday.value, "%Y-%m-%d").replace(year=bday_year).date() - current_date
            if days.days < 0:
                days = datetime.strptime(self.birthday.value, "%Y-%m-%d").replace(
                    year=bday_year + 1).date() - current_date
            return f"{days.days} to {self.name.value}'s birthday"
        else:
            return "No Birthday found"

    def add_phone(self, phone: Phone):
        self.phone.append(phone)

    def del_phone(self, phone: Phone):
        for p in self.phone:
            if phone.value == p.value:
                self.phone.remove(p)

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        self.del_phone(old_phone)
        self.add_phone(new_phone)

    def __repr__(self):
        return f"name: {self.name.value}, phone: {[i.value for i in self.phone]}, birthday: {self.birthday.value}"


class AddressBook(UserDict):
    N = 2

    def iterator(self):
        index, print_block = 1, '-' * 50 + '\n'
        for record in self.data.values():
            print_block += str(record) + '\n'
            if index < self.N:
                index += 1
            else:
                yield print_block
                index, print_block = 1, '-' * 50 + '\n'
        yield print_block

    def show_all_records(contacts, *args):
        if not contacts:
            return 'Address book is empty'
        result = 'List of all users:\n'
        print_list = contacts.iterator()
        for item in print_list:
            result += f'{item}'
        return result

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def show_phone_numbers(self, name: Name):
        return [i.value for i in self.data[name].phone]


phone_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return "Please, enter the name and number"
        except ValueError:
            return "Enter a valid number"
        except KeyError:
            return "No such name in phonebook"

    return wrapper


def add_user(*arg):
    try:
        name = Name(arg[0])
    except ValueError:
        return "Please enter a name"
    phone_list = []
    for i in arg:
        try:
            phone_list.append(Phone(i))
        except ValueError:
            continue
    try:
        bday = Birthday(arg[-1])
    except ValueError:
        bday = Birthday(None)

    rec = Record(name, phone_list, bday)
    if rec.name.value not in phone_book:
        phone_book.add_record(rec)
    else:
        return f"The name {name.value} already exists. To change number please use the 'change {name.value}' command"
    return f"Contact {name.value} added successfully"


@input_error
def add_number(*args):
    phone_book[args[0]].add_phone(Phone(args[1]))
    return f"Phone number {args[1]} is successfully added for user {args[0]}"


@input_error
def del_number(*args):
    phone_book[args[0]].del_phone(Phone(args[1]))
    return f"Phone number {args[1]} is successfully deleted"


@input_error
def change_number(*args):
    phone_book[args[0]].change_phone(Phone(args[1]), Phone(args[2]))
    return f"Phone number for {args[0]} is successfully changed from {args[1]} to {args[2]}"


@input_error
def phone(*args):
    return phone_book.show_phone_numbers(args[0])


@input_error
def days_to_b_day(*args):
    return phone_book[args[0]].days_to_birthday()


def show_all(*args):
    return phone_book.show_all_records(args[0])


def view(*args):
    lst = ["{:^10}: {:>10}".format(k, str(v)) for k, v in phone_book.items()]
    return "\n".join(lst)


def hello(*args):
    return "How can I help you?"


def exit(*args):
    return "Good bye!"


COMMANDS = {hello: ["hello", "hi"],
            change_number: ["change"],
            phone: ["phone"],
            exit: ["exit", "close", "good bye", ".", "bye"],
            add_user: ["add user"],
            add_number: ["add number", "add phone"],
            show_all: ["show all", "show"],
            del_number: ["delete", "del"],
            days_to_b_day: ["tell days to birthday", "tell bday"],
            view: ["view", "all users"]
            }


def parse_command(user_input: str):
    for k, v in COMMANDS.items():
        for i in v:
            if user_input.lower().startswith(i.lower()):
                return k, tuple(user_input[len(i):].strip().split(" "))


def main():
    while True:
        user_input = input("Enter your command ")
        try:
            result, data = parse_command(user_input)
            print(result(*data))
            if result is exit:
                break
        except TypeError:
            print(f"No such command. Consider using one from a list: {[v for v in COMMANDS.values()]}")


if __name__ == "__main__":
    main()
