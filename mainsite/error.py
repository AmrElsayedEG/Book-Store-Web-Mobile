from django.shortcuts import render

# HTTP Error 400
def handler400(request, exception):
    return render(request, "404.html")

# HTTP Error 403
def handler403(request, exception):
    return render(request, "404.html")


# HTTP Error 404
def handler404(request , exception):
    return render(request, "404.html")

# HTTP Error 500
def handler500(request):
    return render(request, "404.html")
