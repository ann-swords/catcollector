from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cat, Toy
from .forms import FeedingForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Import the decorators for Function based Views only
from django.contrib.auth.decorators import login_required
# Import the decorators for Class based Views only
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


# class Cat:
#     def __init__(self, name, breed, description, age):
#         self.name = name
#         self.breed = breed
#         self.description = description
#         self.age = age


# cats = [
#     Cat('Lolo', 'Tabby', 'Long Curly Hair', 3),
#     Cat('Sachi', 'Tortise Shell', 'Cute face', 0),
#     Cat('Jojo', 'Tortise Shell', 'Cool meow', 2),
# ]


def home(request):
    # same as res.send in Express
    return render(request, 'home.html')


def about(request):
    # return HttpResponse('<h1>About the cat collector</h1>')
    return render(request, 'about.html')

@login_required
def cats_index(request):
    # cats = Cat.objects.all()  # Django's ORM Function (Object Relational Mapper)
    # instead of writing sql code, we just write Django code orm (cuz it's already built in)
    # only return the user's cats from the DB
    cats = Cat.objects.filter(user=request.user)
    return render(request, 'cats/index.html', {'cats': cats})

@login_required
def cats_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  # instantiate FeedingForm to be rendered in the template
  feeding_form = FeedingForm()
  toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
  return render(request, 'cats/detail.html', {
    # include the cat and feeding_form in the context
    'cat': cat,
    'feeding_form': feeding_form,
    'toys': toys_cat_doesnt_have
  })

# To create new data
class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    # fields = '__all__'
    fields = ['name', 'breed', 'description', 'age', 'image']

# attach the user to the data comes in from the form
    def form_valid(self, form):
        # self.request.user is the logged user
        form.instance.user = self.request.user
        # Allows the createView form_valid methd to do it's normal work
        return super().form_valid(form)



class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = ['breed', 'description', 'age' ]

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = '/cats/'

@login_required
def add_feeding(request, cat_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('detail', cat_id=cat_id)


# TOYS:
class ToyList(LoginRequiredMixin, ListView):
    model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy


class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'

@login_required
def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)

def unassoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('detail', cat_id=cat_id)

# Sign Up View Function:
def signup(request):
    error_message = ''
    if request.method == 'POST':
        # Make a 'user' form object with the data from the browser
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # save user to db
            user = form.save()
            # Log in the user automatically once they sign up
            login(request, user)
            return redirect('index')
        
        else:
            error_message = 'Invalid: Please Try Again!'

    # If there's a bad post or get request:
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
