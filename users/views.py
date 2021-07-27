from django.views import View
from django.shortcuts import render

# Create your views here.
# CBV
class LoginView(View):

    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        pass

#FBV
def login_view(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass