from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django import forms
import random

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title not in util.list_entries():
        return render(request, "encyclopedia/filenotfound.html")
    else:
        return render(request, "encyclopedia/entry.html",{
        'title': title,
        'entry': markdown2.markdown(util.get_entry(title))
        })

def search(request):
    if request.method == "POST":
        result = str(request.POST['q'])
        entries = util.list_entries()
        searchlist = list()
        x = 0
        y = 0
        if result in entries:
            return render(request, "encyclopedia/entry.html",{
            'title': result,
            'entry': markdown2.markdown(util.get_entry(result))
            })
        else:
            for entry in entries:
                if result in entry.lower():
                    searchlist.append(entry)
            return render(request, "encyclopedia/searchresults.html", {
                "entries": searchlist
            })

def edit(request, title):
    if request.method == "GET":
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "content": util.get_entry(title)
        })
    else:
        new_content = request.POST.get("edit-content")
        util.save_entry(title, new_content)
        return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))

#Create a new form
class NewEntry(forms.Form):
    title = forms.CharField(label = "Enter Title")
    text = forms.CharField(label = "Enter Description")


def create(request):
    context = {}
    context['form'] = NewEntry()
    return render(request, "encyclopedia/newpage.html", context)


def new(request):
    entries = util.list_entries()
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            title = form.cleaned_data["title"]
            if title.capitalize() in entries:
                return render(request, "encyclopedia/existingpage.html")
            else:
                util.save_entry(title.capitalize(), text)
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title.capitalize()]))

def randompage(request):
    entries = util.list_entries()
    rand_number = random.randint(0, len(entries)-1)
    rand_entry = entries[rand_number]
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[rand_entry]))
