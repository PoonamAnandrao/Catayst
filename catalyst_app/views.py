from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.views import View
from .forms import LoginForm, UserForm
from .forms import UploadForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import UploadedCSVFile
from rest_framework.decorators import api_view
import csv
from django.contrib import messages

# Perform the loging operation
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request,'base.html')
            else:
                return render(request, self.template_name, {'form': form, 'error_message': 'Invalid login credentials'})
        return render(request, self.template_name, {'form': form})
    
# Uploade the CSV file    
class FileUploadView(View):
    template_name = 'base.html'
    template = 'file_upload.html'

    def get(self, request):
        form = UploadForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'File Uploaded Successfully')
            return redirect('dashboard')

        return render(request, self.template, {'form': form})


def index(request):
    return render(request,'base.html') 

def dashboard(request):
    return render(request, 'dashboard.html')  

#fetach the User details
def user_detail(request):
    template_name = 'user_details.html'
    users = User.objects.all()
    return render(request, 'user.html', {'users': users})

# Inactive the SuperUser
def delete_user(request, user_id):
    user = User.objects.get(id = user_id)
    user.is_active = False
    user.save()
    users = User.objects.all()
    return render(request, 'user.html', {'users': users})

# Create SuperUser 
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('user_details') 
        else:
            messages.error(request, 'Failed to create user. Please correct the errors.')
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})

#Perferme filter operation 
@api_view(['GET'])
def filter_csv(request):
    name = request.GET.get('name', '')
    domain = request.GET.get('domain', '')
    year_founded = request.GET.get('year_founded', '')
    industry = request.GET.get('industry', '')
    size_range = request.GET.get('size_range', '')
    locality = request.GET.get('locality', '')
    country = request.GET.get('country', '')
    
    last_uploaded_file = UploadedCSVFile.objects.last()
    if not last_uploaded_file:
        return JsonResponse({'error': 'No CSV file uploaded yet'})
    with open(last_uploaded_file.file.path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        matching_count = 0
        for row in csv_reader:
            if (
                (not name or name.lower() in row.get('name', '').lower()) and
                (not domain or domain.lower() in row.get('domain', '').lower()) and
                (not year_founded or year_founded.lower() in row.get('year founded', '').lower()) and
                (not industry or industry.lower() in row.get('industry', '').lower()) and
                (not size_range or size_range.lower() in row.get('size range', '').lower()) and
                (not locality or locality.lower() in row.get('locality', '').lower()) and
                (not country or country.lower() in row.get('country', '').lower())
            ):
                matching_count += 1
        if matching_count is not None:
            return redirect('filter_page', matching_count=matching_count)
        else:    
            return redirect('filter_page')    
