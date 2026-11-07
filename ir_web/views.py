from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .registry import ir_instance

def search(request):
    search_query = request.GET.get('search_query', '')
    selected_filter = request.GET.get('query_type', '')

    res = []
    if selected_filter == "boolean":
        res = ir_instance.boolean(search_query)
    elif selected_filter == "phrase":
        res = ir_instance.phrase(search_query)
    elif selected_filter == "proximity":
        res = ir_instance.proximity(search_query)
    elif selected_filter == "wildcard":
        res = ir_instance.wildcard(search_query)
    elif selected_filter == "ranking":
        res = ir_instance.rank(search_query)

    return render(request, 'search.html', {
        'search_query': search_query,
        'selected_filter': selected_filter,
        "results": res
    })