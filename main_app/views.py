from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Cat, Toy
from .forms import FeedingForm
# Create your views here.


def home(request):
  return render(request, 'home.html')
def about(request):
  return render(request, 'about.html')
def cats_index(request):
  cats = Cat.objects.all()
  return render(request, 'cats/index.html', {'cats': cats})
def cats_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  # Get the toys the cat doesn't have
  toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', {
    'cat': cat, 'feeding_form': feeding_form,
    # Add the toys to be displayed
    'toys': toys_cat_doesnt_have
  })
def add_feeding(request, cat_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.cat_id = cat_id
    new_feeding.save()
  return redirect('detail', cat_id=cat_id)

def assoc_toy(request, cat_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Cat.objects.get(id=cat_id).toys.add(toy_id)
  return redirect('detail', cat_id=cat_id)


class CatCreate(CreateView):
  model = Cat
  fields = '__all__'
class CatUpdate(UpdateView):
  model = Cat
  fields = ['breed', 'description', 'age']
class CatDelete(DeleteView):
  model = Cat
  success_url = '/cats/'
class ToyList(ListView):
  model = Toy
class ToyDetail(DetailView):
  model = Toy
class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'
class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']
class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'