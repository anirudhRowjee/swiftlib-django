import isbnlib
import isbnlib._exceptions as exceptions
import isbnlib.dev._exceptions as goob_exceptions


def getBookData(isbn13):
    try:
        data = isbnlib.meta(str(isbn13), service='goob')
    except goob_exceptions.NoDataForSelectorError:
        # google books not working
        try:
            data_open = isbnlib.meta(str(isbn13))
            data = data_open
        except exceptions.NotValidISBNError:
            return False
        return False

    name = data['Title']
    author = data['Authors'][0]
    isbn13 = data['ISBN-13']

    print([name, author, isbn13])
    return [name, author, isbn13]

