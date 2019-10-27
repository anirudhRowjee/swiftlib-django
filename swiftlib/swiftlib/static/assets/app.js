// WORKING FILE FOR JAVASCRIPT

// function to see if book can be added by ISBN or not

// variable declaration
var isbn = document.getElementById('isbn')
var bookname = document.getElementById('bookname');
var author = document.getElementById('author');

// COPIED FROM DJANGO DOCS
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var csrftoken = getCookie('csrftoken');

function checkISBN(isbn){
    var endpoint = 'http://localhost:8000/books/isvalidISBN?isbn=';
    endpoint += isbn;

    // AJAX section
    $.ajax({
        
        url: endpoint,
        contentType: "application/json",
        dataType: "json",

        success: function(result){

            if (result['status'] == 'found'){
                console.log(result);
                bookname.value = result['name'];
                author.value= result['author'];
                $('#isbn').addClass('validBox');
            }
            else{
                console.log("INVALID ISBN");
            }
        }
    })
    
}


$('#isbn').on('change keyup paste', function(){
    // wrapper function - call eval function on change of value
    console.log("changing");
    var isbn = document.getElementById('isbn').value;
    if(isbn.length == 13 | isbn.length > 13){
        checkISBN(isbn);
    }
    else{
        bookname.value = '';
        author.value =  '';
    }
})
