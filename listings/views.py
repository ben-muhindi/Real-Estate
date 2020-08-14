from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator 
from listings.choices import price_choices, bedroom_choices, state_choices

from .models import Listing

def index(request): 
    listings =Listing.objects.order_by('-list_date').filter(is_published =True) 

    paginator = Paginator(listings,6)
    page = request.GET.get ('page')
    paged_listings = paginator.get_page(page)

    context ={
        'listings':paged_listings
    }
  
    return render(request,'listings/listings.html', context)

def listing(request, listing_id): 
    listing =get_object_or_404 (Listing, pk = listing_id)
   
    context ={
        'listing':listing
    }

    return render(request,'listings/listing.html', context)

def search(request): 
    queryset_list =Listing.objects.order_by ('-list_date')  # we start a query set list to get all of the listings. Then add filters for the search. 

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords: 
            queryset_list = queryset_list.filter(description__icontains=keywords) # icontains helps us to search the description for any words contained in this keywords. Notice, it is a double underscore. 
    # City 
    if 'city' in request.GET:
        city = request.GET['city']
        if city: 
            queryset_list = queryset_list.filter(city__iexact=city) #Note, iexact is case insensitive meaning Bedford and bedford will return the same values. if you want it to be case sensitive, then you will just use exact. 
    # State 
    if 'state' in request.GET:
        state = request.GET['state']
        if state: 
            queryset_list = queryset_list.filter(state__iexact=state) 

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms: 
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms) #lte means less than or equal to 
    
     # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price: 
            queryset_list = queryset_list.filter(price__lte=price) #lte means less than or equal to 


    context ={
        'state_choices':state_choices, 
        'bedroom_choices':bedroom_choices,
        'price_choices':price_choices,  
        'listings':queryset_list,  
        'values': request.GET
    }
    return render(request,'listings/search.html', context)


