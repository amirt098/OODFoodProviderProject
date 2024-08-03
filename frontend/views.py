from django.views import View
from django.shortcuts import render
from django.urls import path


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html', {"request": request})


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html', {'request': request})


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html', {'request': request})

# If you have a services page, you can uncomment and create a ServicesView similarly
# class ServicesView(View):
#     def get(self, request):
#         return render(request, 'frontend/services.html')
