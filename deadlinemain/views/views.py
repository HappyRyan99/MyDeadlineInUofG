from django.http import JsonResponse
from django.shortcuts import render

def custom_page_not_found(request, exception=None):
    # Differentiate missing paths by HTTP method
    if request.method == 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Not Found',
            'message': 'The requested endpoint does not exist.',
        }, status=404)

    # For GET requests, serve the custom 404 HTML page
    return render(request, '404.html', status=404)
