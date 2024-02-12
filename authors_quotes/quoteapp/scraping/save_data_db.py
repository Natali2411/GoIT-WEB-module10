import pathlib
import shutil
from datetime import datetime

import django

from ..models import Author, Quote, Tag


import json


class FileInteraction:
    @staticmethod
    def read_info(path: str) -> dict:
        """
        Method reads info from json file.
        :param path: Path to file.
        :return: Data from file as a dictionary.
        """
        with open(path, "r") as fh:
            try:
                file_data = json.load(fh)
            except ValueError:
                return {}
            return file_data

    @staticmethod
    def save_info(path: str, data: dict) -> None:
        """
        Method saves dictionary to json file.
        :param data: Dictionary that should be saved.
        :param path: Path to file in which the data should be saved.
        """
        with open(path, mode="w") as fh:
            json.dump(data, fh)

    @staticmethod
    def delete_folder(folder_path: str) -> None:
        """

        :param folder_path:
        """
        path = pathlib.Path(folder_path)
        if path.exists():
            shutil.rmtree(path)


def write_to_db(authors_file_path: str, quotes_file_path: str) -> None:
    # Add authors
    authors_file_objects = FileInteraction.read_info(authors_file_path)
    quotes_file_objects = FileInteraction.read_info(quotes_file_path)
    for instance in authors_file_objects:
        author_data = instance
        born_date: datetime = datetime.strptime(author_data["born_date"], "%B %d, %Y")
        born_date_fmt: str = datetime.strftime(born_date, "%Y-%m-%d")
        author_data["born_date"] = born_date_fmt
        try:
            Author.objects.create(**author_data)
        except django.db.utils.IntegrityError as err:
            print(
                f"The author with the name '{author_data['fullname']}' already "
                f"exist in the collection, stacktrace err: '{err}'"
            )

    # Add quotes
    for instance in quotes_file_objects:
        quote_data = instance
        print("Quote data from file")
        print(quote_data)
        author = Author.objects.get(fullname=quote_data["author"])
        if author:
            tags = []
            for tag_name in quote_data["tags"]:
                try:
                    tag = Tag.objects.create(name=tag_name)
                    tags.append(tag)
                except django.db.utils.IntegrityError as err:
                    print(f"The tag with the name '{tag_name}' already exists, "
                          f"stacktrace err: '{err}'")
                    tags.append(
                        Tag.objects.get(name=tag_name)
                    )
            try:
                quote_data.pop("fullname")
                quote_data.pop("tags")
                quote = Quote.objects.create(**quote_data)
                quote.tags.add(*tags)
                quote.author = author
                quote.save()
            except django.db.utils.IntegrityError as err:
                print(f"The quote with the text '{quote_data['quote']}' already exists, "
                      f"stacktrace err: '{err}'")
