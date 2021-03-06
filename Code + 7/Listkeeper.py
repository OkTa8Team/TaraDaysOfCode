import os

"""Listkeeper_ans.py

    Manage lists from the files.

"""

__author__ = "maydee"

YES = frozenset({'YES', 'Y', 'yes', 'y', 'Yes'})

def menu():
    """Shows the menu and receives the users answer.
    """
    is_changed = False
    item_list = []

    filename, item_list = choose_file()
    if not filename:
        print("Canceled")
        return

    while True:
        print_list(item_list)
        user_choice = choice(item_list, is_changed)
        if user_choice in 'Aa':
            is_changed = add_element(item_list, is_changed)
        elif user_choice in 'Dd':
            is_changed = del_element(item_list, is_changed)
        elif user_choice in 'Ss':
            is_changed = save_item_list(filename, item_list)
        elif user_choice in 'Qq':
            if (is_changed and (get_string("Save unsaved changed (y/n)", "y") in YES)):
                save_item_list(filename, item_list, True)
            break


def choose_file():
    """Returns the filename and the list items."""
    item_list = []
    filename = None
    new_file = False

    files = [file for file in os.listdir(".") if file.endswith(".lst")]

    if not files:
        new_file = True
    else:
        print_list(files)
        while True:
            file_index = get_integer("Specify the number of the file you want or 0 to create new one", maximum=len(files))
            if file_index in range(len(files) + 1):
                break
            else:
                print("Enter the valid number, please.\n")
        if file_index == 0:
            new_file = True
        else:
            filename = files[file_index - 1]
            item_list = load_item_list(filename)
    if new_file:
        filename = get_string("Choose filename")
        if not filename.endswith(".lst"):
            filename += ".lst"
    return filename, item_list


def choice(item_list, is_changed):
    """Searches for the filename file or asks to create new one."""
    while True:
        if item_list:
            if is_changed:
                options = "[A]dd [D]elete [S]ave [Q]uit"
                valid_options = "AaDdSsQq"
            else:
                options = "[A]dd [D]elete [Q]uit"
                valid_options = "AaDdQq"
        else:
            options = "[A]dd [Q]uit"
            valid_options = "AaQq"
        user_choice = get_string(options, default='a')
        if user_choice not in options:
            print('ERROR: invalid choice--enter on of "{0}"'.format(valid_options))
            input("Press Enter to continue...")
        else:
            return user_choice


def add_element(item_list, is_changed):
    """Add an element to the list"""
    new_item = get_string("Add item")
    if new_item:
        item_list.append(new_item)
        item_list.sort(key=str.lower)
        return True
    return is_changed


def del_element(item_list, is_changed):
    """Delete an element from the list."""
    del_item = get_integer("Delete item number (or 0 to cancel)", maximum=len(item_list))
    if del_item != 0:
        del item_list[del_item-1]
        return True
    return is_changed


def load_item_list(filename):
    """Load the list from the file."""
    item_list = []
    file = None
    try:
        file = open(filename, encoding='utf-8')
        for line in file:
            item_list.append(line.rstrip())
    except EnvironmentError as err:
        print("Error! Failed to load {0}: {1}".format(filename, err))
        return []
    finally:
        if file is not None:
            file.close()
    return item_list


def print_list(item_list):
    """Print the list to the console."""
    if not item_list:
        print("-- no items are in the list --")
    else:
        for index, item in enumerate(item_list):
            print("{0}: {item}".format(index + 1, **locals()))
    print()


def save_item_list(filename, item_list, stop_after_save = False):
    """Save the list to the filename file."""
    file = None
    try:
        file = open(filename, 'w', encoding='utf-8')
        file.write("\n".join(item_list))
        file.write("\n")
    except EnvironmentError as err:
        print("ERROR! Failed to save {filename}: {err}")
        return True
    else:
        print("Saved {0} item{1} to {2}.lst".format(len(item_list),'s' if len(item_list) > 1 else '', filename))
        if not stop_after_save:
            input("Press Enter to continue...")
        return False
    finally:
        if file is not None:
            file.close()


def get_string(message, name="string", default=None,
               minimum_length=0, maximum_length=80):
    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line:
                if default is not None:
                    return default
                if minimum_length == 0:
                    return ""
                else:
                    raise ValueError("{0} may not be empty".format(
                                     name))
            if not (minimum_length <= len(line) <= maximum_length):
                raise ValueError("{name} must have at least "
                        "{minimum_length} and at most "
                        "{maximum_length} characters".format(
                        **locals()))
            return line
        except ValueError as err:
            print("ERROR", err)


def get_integer(message, name="integer", default=None, minimum=0,
                maximum=100, allow_zero=True):

    class RangeError(Exception): pass

    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line and default is not None:
                return default
            i = int(line)
            if i == 0:
                if allow_zero:
                    return i
                else:
                    raise RangeError("{0} may not be 0".format(name))
            if not (minimum <= i <= maximum):
                raise RangeError("{name} must be between {minimum} "
                        "and {maximum} inclusive{0}".format(
                        " (or 0)" if allow_zero else "", **locals()))
            return i
        except RangeError as err:
            print("ERROR", err)
        except ValueError as err:
            print("ERROR {0} must be an integer".format(name))


def main():
    pass

main()