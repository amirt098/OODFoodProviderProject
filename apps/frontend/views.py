from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render


class FrontendViewSet(viewsets.ViewSet):

    def list(self, request):
        return render(request, 'home.html')

    @action(detail=False, methods=['get'], url_path='')
    def home(self, request):
        return render(request, 'home.html')

    @action(detail=False, methods=['get'])
    def about(self, request):
        return render(request, 'about.html')

    @action(detail=False, methods=['get'])
    def contact(self, request):
        return render(request, 'contact.html')

    # @action(detail=False, methods=['get'])
    # def services(self, request):
    #     return render(request, 'frontend/services.html')
