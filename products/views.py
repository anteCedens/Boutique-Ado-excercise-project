from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None

    # Checking whether request.get exists
    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            # this double underscore ("__") syntax is common when making queries in django
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # Since we named the text input in the form 'q', we can just check if 'q' is in request.get
        if 'q' in request.GET:
            # If it is, set it equal to a variable called query
            query = request.GET['q']
            # If the query is blank it's not going to return any results
            # So if that's the case let's use the Django messages framework
            # to attach an error message to the request.
            # And then redirect back to the products url.
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            # If the query isn't blank, use a special object from django.db.models called Q
            # to generate a search query
            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/product_detail.html', context)
