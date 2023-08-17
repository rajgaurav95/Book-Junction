from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core import serializers


from .models import *



# Create your views here.
def Landing_page(request):
    if request.method=='POST':
        pass 
    else:
        books=Book.objects.all()
        return render(request,'Landing_page.html',{"books":books})


def product_filter_page(request):
    if request.method=='POST':
        pass 
    else:
        id=request.GET.get('id',None)
        price=request.GET.get('price',None)
        if id:
            books=Book.objects.filter(genre__id=id) 
        else: 
            books=Book.objects.all()
        paginator=Paginator(books,9,orphans=1)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)

        context={
            "books":page_obj,
            "genres":genres.objects.all()
        }
        return render(request,'filter_books_page.html',context)

def cart_page(request):
    if request.method=='POST':
        pass 
    else:
        return render(request,'cart.html')

def price_1(filter_results):
    filter_results['result'] = filter_results['result'].union(Book.objects.filter(price__gte=100,price__lte=500)) if filter_results['result'] else Book.objects.filter(price__gte=100,price__lte=500)
def price_2(filter_results):
    filter_results['result'] = filter_results['result'].union(Book.objects.filter(price__gte=500,price__lte=1000)) if filter_results['result'] else Book.objects.filter(price__gte=500,price__lte=1000)
def price_3(filter_results):
    filter_results['result'] = filter_results['result'].union(Book.objects.filter(price__gte=1000,price__lte=1500)) if filter_results['result'] else Book.objects.filter(price__gte=1000,price__lte=1500)
def price_4(filter_results):
    filter_results['result'] = filter_results['result'].union(Book.objects.filter(price__gte=1500,price__lte=2000)) if filter_results['result'] else Book.objects.filter(price__gte=1500,price__lte=2000)
def price_5(filter_results):
    filter_results['result'] = filter_results['result'].union(Book.objects.filter(price__gte=2500)) if filter_results['result'] else Book.objects.filter(price__gte=2000)

def group_1(filter_results):
    filter_results['result'] = filter_results['result'].order_by('author__id')
def group_2(filter_results):
    filter_results['result'] = filter_results['result'].order_by('price')
def group_3(filter_results):
    filter_results['result'] = filter_results['result'].order_by('genre__name')

def Bookfilters(request):
    filters=sorted(request.POST.get('filters').split(','))
    print(filters)
    filter_results = {
        "result":None,
        "x_1" : price_1,
        "x_2" : price_2,
        "x_3" : price_3,
        "x_4" : price_4,
        "x_5" : price_5,
        "y_1" : group_1,
        "y_2" : group_2,
        "y_3" : group_3
        }
    
    for filter in filters:
        if filter in ['y_1','y_2','y_3']:
            if filter_results['result'] is None:
                filter_results['result']=Book.objects.all()
        filter_results[filter](filter_results)

    serialized_object = serializers.serialize('python', filter_results['result'])
    # 
    return JsonResponse({'filter':serialized_object})

def book_details(request,id):
    book = Book.objects.get(id=int(id))
    review_queryset = Review.objects.filter(book_id = book)
    return render(request,'book_detail.html',{'book':book, 'review_queryset' : review_queryset})

def search_result(request):
    search=request.POST.get('search')
    books=Book.objects.all()
    books_set=set()
    books_set = books.filter(title__icontains=search)
    gen_set = books.filter(genre__name__icontains=search)
    books_set = books_set.union(gen_set)
    serialized_object = serializers.serialize('python',books_set)
    # 
    return JsonResponse({'filter':serialized_object})

def user_reviews(request):
    if request.method == 'POST':
        text = request.POST.get('review')
        book_id = request.POST.get('book_id')
        if text!="":
            review_obj = Review.objects.create(book_id = book_id, customer_id = request.user.id, text = text)
            review_obj.save()
    return redirect(f'/book/detail/{book_id}/')
