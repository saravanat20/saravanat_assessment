from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.generic import ListView
from .forms import SignUpForm, AddRecordForm
from .models import Record
from rest_framework import generics
from .serializers import RecordModelSerializer
from django.forms import ModelForm
import requests

class RecordModelListCreate(generics.ListCreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordModelSerializer

class RecordModelRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordModelSerializer

class RecordModelForm(ModelForm):
    class Meta:
        model = Record
        fields = ['first_name', 'last_name']


def home(request):
    records = Record.objects.all()
    # Check to see if logging in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            messages.success(request, "You Have Been Logged In")
            return redirect('home')
        else:
            messages.success(request,"Invalid login creditanils..")
            return redirect('home')
    else:
        return render(request, 'home.html',{'records': records})

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request,"You Have Been Logged Out...")
    return redirect('home')

def register(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered!!!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})

def customer_record(request,pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id = pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You Must Be Logged In To View Page!!!")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        deleting = Record.objects.get(id = pk)
        deleting.delete()
        messages.success(request, f"Customer {pk} Record Has Been Deleted")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In To Delete")
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Has Been Added Successfully !!")
                redirect('home')
        return render(request,'add_record.html',{'form': form})
    else:
        messages.success(request, "Login Please")
        return redirect('home')

def update_record(request,pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id = pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record Has Been Updated !!")
            return redirect('home')
        return render(request,'update_record.html',{'form':form})
    else:
        messages.success(request, "Login Please")
        redirect('home')

def ag_grid_view(request):
    data = Record.objects.all()  # Fetch your data here
    data_json = serialize('json', data)
    return JsonResponse(data_json, safe=False)

def search_name(request):
    if request.method == "POST":
        searched = request.POST['searched']
        names = Record.objects.filter(first_name__contains = searched)
        return render (request,'search_name.html',{'searched': searched,'names':names})
    else:
        return render (request,'search_name.html',{})

'''API'''
def create_object(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Send POST request to API endpoint
            response = requests.post('http://127.0.0.1:8000/api/recordmodels/', json=form.cleaned_data)
            if response.status_code == 201:  # Created
                return redirect('add_record.html')  # Redirect to object list view
    else:
        form = SignUpForm()
    return render(request, 'home', {'form': form})

def retrieve_object(request, id):
    # Send GET request to API endpoint
    response = requests.get(f'http://127.0.0.1:8000/api/recordmodels/{id}/')
    if response.status_code == 200:  # OK
        data = response.json()
        return render(request, 'object_detail.html', {'object': data})
    else:
        return render(request, 'error.html', {'status_code': response.status_code})


def update_object(request, id):
    
    response = requests.get(f'http://localhost:8000/api/yourmodels/{id}/')
    if response.status_code == 200:  # OK
        data = response.json()
        form = AddRecordForm(data)
        if request.method == 'POST':
            form = AddRecordForm(request.POST)
            if form.is_valid():
                response = requests.put(f'http://localhost:8000/api/yourmodels/{id}/', json=form.cleaned_data)
                if response.status_code == 200:  # OK
                    return redirect('object_detail', id=id)  # Redirect to object detail view
        return render(request, 'update_object.html', {'form': form})
    else:
        return render(request, 'error.html', {'status_code': response.status_code})
    
def delete_object(request, id):
    # Send DELETE request to API endpoint
    response = requests.delete(f'http://localhost:8000/api/yourmodels/{id}/')
    if response.status_code == 204:  # No Content
        return redirect('object_list')  # Redirect to object list view
    else:
        return render(request, 'error.html', {'status_code': response.status_code})





    
     

     
     
         
         
         
         
     



