from django.shortcuts import render

# Create your views here.
from .models import Manufacturer, Product, Website, Website_Product

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_manufactures = Manufacturer.objects.all().count()
    num_products = Product.objects.all().count()
    num_websites = Website.objects.all().count()
    num_webProducts = Website_Product.objects.all().count()

    context = {
        'num_manufactures': num_manufactures,
        'num_products': num_products,
        'num_websites': num_websites,
        'num_webProducts': num_webProducts,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
