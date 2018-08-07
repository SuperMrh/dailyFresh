from django.shortcuts import render

# Create your views here.


def index(request):  # , user_id
    if request.method == 'GET':
        # user_id = user_id
        return render(request, 'demo/index.html')
