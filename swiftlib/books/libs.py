import isbnlib
import isbnlib._exceptions as exceptions


def getBookData(isbn13):
    try:
        data = isbnlib.meta(str(isbn13), service='goob')
    except exceptions.NotValidISBNError:
        return False

    name = data['Title']
    author = data['Authors'][0]
    isbn13 = data['ISBN-13']

    return [name, author, isbn]
