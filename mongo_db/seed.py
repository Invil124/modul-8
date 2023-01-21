from models import Author, Quote
import connect

import json
from datetime import datetime


def get_json_data(json_file):
    with open(json_file, "r", encoding="utf-8") as fh:
        result = json.load(fh)
        return result


def fill_author(json_data_authors: dict):
    for data in json_data_authors:
        author = Author()
        author.full_name = data["fullname"]
        author.born_date = datetime.strptime(data["born_date"], "%B %d, %Y")
        author.born_location = data["born_location"]
        author.description = data["description"]
        author.save()


def fill_quotes(json_data_quotes: dict):
    for data in json_data_quotes:
        quot = Quote()
        quot.tags = data["tags"]
        quot.quote = data["quote"]
        quot.author = Author.objects(full_name=data["author"])[0].id
        quot.save()


if __name__ == "__main__":
    json_data_authors = get_json_data("authors.json")
    fill_author(json_data_authors)
    json_data_quotes = get_json_data("qoutes.json")
    fill_quotes(json_data_quotes)




