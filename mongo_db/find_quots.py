from models import Quote, Author
import connect


def error_func(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except IndexError as error_int:
            return "Incorrect input"

    return wrapper


def find_quote_by_name(name):
    list_quotes = []
    authors = Author.objects(full_name=name)

    if len(authors) == 0:
        return "Author not find"

    quotes = Quote.objects(author=authors[0].id)

    for quot in quotes:
        list_quotes.append(quot.quote)

    return list_quotes


def find_quote_by_tag(tag):
    list_quotes = []
    quotes = Quote.objects(tags=tag)

    for quot in quotes:
        list_quotes.append(quot.quote)

    return list_quotes


def find_quote_by_tags(tags):
    list_quotes = []
    tags_list = tags.split(",")
    quotes = Quote.objects(tags__in=tags_list)

    for quot in quotes:
        list_quotes.append(quot.quote)

    return list_quotes


@error_func
def work_with_commands(user_input):

    commands = {"name": find_quote_by_name,
                "tag": find_quote_by_tag,
                "tags": find_quote_by_tags,
                }

    parse_user_input = user_input.split(":")
    command = parse_user_input[0]
    args = parse_user_input[1]
    result = commands[command](args)

    if len(result) == 0:
        return "Tag not find"

    return result


if __name__ == "__main__":
    while True:
        user_input = input("Enter your commands: ")

        if user_input == "exit":
            break

        result = work_with_commands(user_input)

        print(result)


