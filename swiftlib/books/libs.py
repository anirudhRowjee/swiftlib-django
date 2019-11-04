import isbnlib
import isbnlib._exceptions as exceptions
import isbnlib.dev._exceptions as goob_exceptions


def getBookData(isbn13):
    try:
        data = isbnlib.meta(str(isbn13), service='goob')
    except goob_exceptions.NoDataForSelectorError:
        # Google books not working
        try:
            data_open = isbnlib.meta(str(isbn13))
            data = data_open
        except exceptions.NotValidISBNError:
            return False
        return False
    
    length=len(data['Authors'])
    
    if length==1:
        # Only one author
        authorstring = data['Authors'][0]
        
    else:
        # To get multiple author names in one element in one string
        authorstring= ""
        for i in range(0,length):
            authorstring+=data['Authors'][i]
            if i==(length-1):
                # To avoid extra last comma
                pass
            else:
                authorstring+=","

               
    name = data['Title']
    author = authorstring 
    isbn13 = data['ISBN-13']

    print([name, author, isbn13])
    return [name, author, isbn13]
