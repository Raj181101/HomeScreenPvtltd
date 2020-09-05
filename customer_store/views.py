from django.shortcuts import render
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse, JsonResponse
from .models import *

# Create your views here.

class CustomerSerializer(ModelSerializer):
    bookmarks = SerializerMethodField()

    class Meta:
        model = Customer
        depth = 1
        fields = ('id','name','email','mobile','langitude','latitude','bookmarks')
    
    def get_bookmarks(self, customer):       
        context = []
        bookmarks = customer.customerbookmark_set.last().bookmarks.all()
        for bookmark in bookmarks:
            data = {}
            data['title'] = bookmark.title
            data['url'] = bookmark.url
            data['source_name'] = bookmark.source_name
            context.append(data)
        
        return context

class BookmarkSerializer(ModelSerializer):
    customer = SerializerMethodField()

    class Meta:
        model = Bookmark
        depth = 1
        fields = ('id','title','url','source_name','customer')
    
    def get_customer(self, bookmark):       
        context = {}

        customer = bookmark.customerbookmark_set.last().customer
        context['id'] = customer.id
        context['name'] = customer.name
        context['email'] = customer.email
        context['mobile'] = customer.mobile
        
        
        return context


@require_GET
@csrf_exempt
def customer(request,id):
    '''
        url = 'http://localhost:8000/api/customer/2/'
    '''

    
    try:
        providers = Customer.objects.filter(id=id)
        status = True
        response = CustomerSerializer(providers, many=True).data
    except ValidationError:
        status = False
        data = ["Invalid UID/id"]

    return JsonResponse({
            'status' : status,
            'data' : response
        })

@require_GET
@csrf_exempt
def all_customer(request):
    try:
        providers = Customer.objects.filter(status=True)
        status = True
        response = CustomerSerializer(providers, many=True).data
    except ValidationError:
        status = False
        data = ["Invalid UID/id"]

    return JsonResponse({
            'status' : status,
            'data' : response
        })


@require_GET
@csrf_exempt
def api_browse(request):
    '''
        url = 'http://localhost:8000/api/browse/?id=2',
        url = 'http://localhost:8000/api/browse/?source_name=Python',
        url = 'http://localhost:8000/api/browse/?title=Python',
        url = 'http://localhost:8000/api/browse/?startdate=2020-09-01&enddate=2020-09-05',
        url = 'http://localhost:8000/api/browse/?latitude=77.5946&longitude=12.9716',
        url = 'http://localhost:8000/api/browse/?sort_by=false/true',
    '''

    status = False
    response = ["No Data Found On Your Search!."]
    message  = 'Success'

    id = request.GET.get('id')

    source_name = request.GET.get('source_name')

    title = request.GET.get('title')

    ##Search on Date Range
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')

    ##Search on Location of Latitude and Langitude
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    ##Search on Sorting from low to high or high to low
    sort_by = request.GET.get('sort_by')

    if id or source_name or title or startdate or enddate or latitude or longitude or sort_by:
        if id:
            try:
                customers = Customer.objects.filter(id=id)
                if customers:
                    response = CustomerSerializer(customers, many=True).data
                    status = True
                else:
                    status = False
                    message = 'No Data Matched With Your Search ID !. Please Provide Valid ID'
                    
            except Exception as e:
                status = False
                message = str(e)

        if source_name:
            try:
                bookmarks = Bookmark.objects.filter(source_name__icontains = source_name)
                if bookmarks:
                    response = BookmarkSerializer(bookmarks, many=True).data
                    status = True
                else:
                    status = False
                    message = 'No Data Matched With Your Search !. Please Provide Valid SourceName'

            except Exception as e:
                status = False
                message = str(e)
        
        if title:
            try:
                bookmarks = Bookmark.objects.filter(title__icontains = title)
                if bookmarks:
                    response = BookmarkSerializer(bookmarks, many=True).data
                    status = True
                else:
                    status = False
                    message = 'No Data Matched With Your Search !. Please Provide Valid Title'

            except Exception as e:
                status = False
                message = str(e)

        if startdate and enddate:
            try:
                bookmarks = Bookmark.objects.filter(created_date__range = [startdate,enddate])
                if bookmarks:
                    response = BookmarkSerializer(bookmarks, many=True).data
                    status = True
                else:
                    status = False
                    message = 'No Data Matched With Your Search !. Please Provide Valid Dates'

            except Exception as e:
                status = False
                message = str(e)

        if latitude and longitude:
            try:
                customers = Customer.objects.filter(latitude=latitude,langitude=longitude)
                if customers:
                    ids = [bookmark.id for customer in customers for bookmark in customer.customerbookmark_set.all()]
                    bookmarks = Bookmark.objects.filter(id__in=ids)
                    response = BookmarkSerializer(bookmarks, many=True).data
                    status = True
                else:
                    status = False
                    message = 'No Data Matched With Your Search ID !. Please Provide Valid Latitude and Longitude'
                    
            except Exception as e:
                status = False
                message = str(e) 

        if sort_by and sort_by.lower() == 'true':
            try:
                bookmarks = Bookmark.objects.all().order_by('-created_date')
                if bookmarks:
                    response = BookmarkSerializer(bookmarks, many=True).data
                    status = True
                else:
                    status = False
                    message = 'No Data Matched With Your Search !. '

            except Exception as e:
                status = False
                message = str(e)

        elif sort_by and sort_by.lower() == 'false':
            try:
                bookmarks = Bookmark.objects.all().order_by('created_date')
                if bookmarks:
                    response = BookmarkSerializer(bookmarks, many=True).data
                    status = True
                else:
                    status = False
                    message = 'No Data Matched With Your Search !.'

            except Exception as e:
                status = False
                message = str(e)
    
    else:
        message = 'Fails'
    
    

    

    return JsonResponse({
            'status' : status,
            'message' : message,
            'data' : response
        })


@require_POST
@csrf_exempt
def bookmark_create(request):
    """
	url = http://127.0.0.1:8000/api/create/
	data = {
		'title':'Python',
        'url':'https://www.djangoproject.com/'
        'source_name':'djangoteam',
        'customer_id':1,
	}
	""" 
    
    success = False
    response = {}	
    title = request.POST.get('title')
    url = request.POST.get('url')
    source_name = request.POST.get('source_name')
    customer_id = request.POST.get('customer_id')

    if title and url and source_name and customer_id:
        try:
            if Customer.objects.filter(id=customer_id):
                try:
                    bookmark = Bookmark.objects.create(title=title,url=url,source_name=source_name)
                    customer = Customer.objects.filter(id=customer_id).last()
                    customerbkmk = customer.customerbookmark_set.last()
                    customerbkmk.bookmarks.add(bookmark)
                    customerbkmk.save()
                    response['message'] = 'Bookmark Created Succesfully'
                    success = True
                except Exception as e:
                    response['message'] = str(e)
            else:
                response['message'] = 'Customer Does Not Exists With Provided ID,Please Provide Valid ID'
        except Exception as e:
            response['message'] = str(e)

    else:
        response['message'] = 'Please Provide Valid Data'


    return JsonResponse({
            'success' : success,
            'data' : response
        })
