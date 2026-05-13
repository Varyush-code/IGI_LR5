from django.shortcuts import render, redirect
from apps.animals.models import Animal
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotFound

def index(request):
    animals = Animal.objects.all()
    return render(request, "animals/index.html", {"animals": animals})

def create(request):
    if request.method == "POST":
        animal = Animal()
        animal.name = request.POST.get("name")
        animal.species = request.POST.get("species")
        animal.family = request.POST.get("family")
        animal.age = request.POST.get("age")
        animal.gender = request.POST.get("gender")
        animal.country = request.POST.get("country")
        animal.description = request.POST.get("description")

        animal.save()
        return redirect("animals:list")

    return render(request, "animals/create.html")

def update(request, pk):
    try:
        animal = Animal.objects.get(pk=pk)

        if request.method == "POST":
            animal.name = request.POST.get("name")
            animal.species = request.POST.get("species")
            animal.family = request.POST.get("family")
            animal.age = request.POST.get("age")
            animal.gender = request.POST.get("gender")
            animal.country = request.POST.get("country")
            animal.description = request.POST.get("description")

            animal.save()
            return redirect("animals:list")
        return render(request, "animals/update.html", {"animal": animal})
    except Animal.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

def delete(request, pk):
    try:
        animal = Animal.objects.get(pk=pk)
        animal.delete()
        return HttpResponseRedirect("/")
    except Animal.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")