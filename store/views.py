from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    try:
        book = Book.objects.get(pk=bid)
    except:
        return HttpResponse('No such book found') #### TO BE CHANGED ####
    count = len(BookCopy.objects.filter(book__exact=book, status__exact=True))
    context = {
        'book': book, # set this to an instance of the required book
        'num_available': count, # set this to the number of copies of the book available, or 0 if the book isn't available
        'user_rating':0
    }
    if request.user.is_authenticated:
        user_rating = book.user_ratings.get(str(request.user))
        print(user_rating)
        print(type(user_rating))
        if user_rating :
            context['user_rating'] = user_rating
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    get_data = request.GET
    print(get_data)
    books = Book.objects.filter(
        title__icontains=get_data.get('title',''), 
        author__icontains=get_data.get('author',''),
        genre__icontains=get_data.get('genre', '')
    )
    context = {
        'books': books, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    } 
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    books = BookCopy.objects.filter(borrower__exact=request.user)
    context = {
        'books': books,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    return render(request, template_name, context=context)

@csrf_exempt
def loanBookView(request):
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    if not request.user.is_authenticated:
        return JsonResponse({ "message": "You must be logged in to loan book" })
    book_id = request.POST['bid'] # get the book id from post data
    books = BookCopy.objects.filter(book_id__exact=book_id, status__exact=True)
    if books:
        book = books[0]
        book.borrow_date = datetime.date.today()
        book.borrower = request.user
        book.status = False
        book.save()
        message = "success"
    else:
        message = "No books available to loan"
    response_data = {
        'message': message,
    }
    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    if request.method == "POST":
        try:
            bid = request.POST['bid']
            book = BookCopy.objects.get(pk=bid)
            book.status = True
            book.borrower = None
            book.borrow_date = None
            book.save()
            return JsonResponse( {"message":"Book successfully returned."} )
        except:
            return JsonResponse( {"message":"No 'bid' found"} )
    else:
        return JsonResponse( {"message":"Bad Request"} )

@login_required
def rateBookview(request, bid):
    if request.method == "POST":
        book = Book.objects.get(pk=bid)
        rating = request.POST['rating']
        book.user_ratings[str(request.user)] = rating
        book.save()
        rating_sum = 0
        for key in book.user_ratings:
            print(key,book.user_ratings[key])
            rating_sum += int(book.user_ratings[key])
        book.rating = rating_sum/len(book.user_ratings)
        book.save()
        return redirect('/book/'+str(bid))
    else:
        return HttpResponse("Bad Request")


