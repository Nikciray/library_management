from django.shortcuts import render
from django.template import loader
from .models import Book,Genre,Record

# Create your views here.
from django.shortcuts import render
from .models import Book
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Max,Count
from django.db.models import Max, F
from django.db.models.functions import Cast,TruncDate



def book_detail(request, pk):
    book = Book.objects.get(id=pk)
    unreturned_count = Record.objects.filter(book=pk,returned=False).count()
    book.stock = book.count-unreturned_count
    return render(request, 'book_detail.html', {'book': book,
})

def search(request,pg_no):
    template = loader.get_template('search.html')
    query = request.GET.get('query','')
    genre_id = request.GET.get('genre_id',0)
    genres = Genre.objects.all();
    books = Book.objects.all()

    if(genre_id):
        books = books.filter(genre=int(genre_id))
    if(query):
        books = books.filter(Q(title__icontains=query)|Q(description__icontains=query)|Q(author__name__icontains=query))

    pageObj = Paginator(books,15)
    if(pg_no):
        books = pageObj.page(pg_no)
    else:
        books = pageObj.page(1)

    return HttpResponse(template.render({'title':'Search results for : '+query,'books':books,'genres':genres,"query":query,"genre_id":int(genre_id)},request))


    

def index(request):
    template = loader.get_template('books.html')#load template
    query = request.GET.get('query','')
    genre_id = request.GET.get('genre_id',0)
    genres = Genre.objects.all();
    action_drama = Book.objects.filter(Q(genre__name__icontains='Action') | Q(genre__name__icontains='Drama')).distinct()
    mystery_thriller = Book.objects.filter(Q(genre__name__icontains='Mystery') | Q(genre__name__icontains='Thriller')).distinct()
    fantasy_adventure = Book.objects.filter(Q(genre__name__icontains='Fantasy') | Q(genre__name__icontains='Adventure')).distinct()

    # fantasy_adventure = Book.objects.filter(Q(genre__name__icontains='Fantasy') | Q(genre__name__icontains='Adventure')).distinct()
    popular_books = Book.objects.annotate(num_borrowed=Count('record')).order_by('-num_borrowed')[:10]
    latest_books = Book.objects.order_by('-publication_date')[:10]
    return HttpResponse(template.render({'latest_books':latest_books,
                                         'popular_books':popular_books,
                                         'action_drama':action_drama,
                                         'mystery_thriller':mystery_thriller,
                                        #  'fantasy_adventure':fantasy_adventure,
                                         'genres':genres,"query":query,"genre_id":int(genre_id)},request))


    

    
    # return HttpResponse(template.render({"books":books,"query":query,'genres':genres,'genre_id':int(genre_id)},request))