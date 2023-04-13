from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown
from . import util
import random

from django import forms

# Making a form
class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(), label="Content")

# Markdown to html
def MdToHtml(title):
    markdowner = Markdown()
    entry = util.get_entry(title)
    if entry == None:
        return None
    else:
        return markdowner.convert(entry)


# Home page of wiki
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Get the wikipage of interest
def entry(request, title):
    html_content = MdToHtml(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry is invalid"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
    })

# Search form
def search(request):
    if request.method == "POST":
        title = request.POST['q']
        html_content = MdToHtml(title)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })
        else:
            allEntries = util.list_entries()
            recommendations = []
            for entry in allEntries:
                if title.lower() in entry.lower():
                    recommendations.append(entry)
            return render(request, "encyclopedia/search.html", {
            "recommendations": recommendations
            })

# Add a new wikipage
def new_page(request):

    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            for entry in util.list_entries():
                if title == entry:
                    return render(request, "encyclopedia/error.html", {
                        "message": "Wikipage with that title already exists."
                    })
                else:
                    util.save_entry(title, content)
                    return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "encyclopedia/new.html", {
            "form": form
            })

    else:
        return render(request, "encyclopedia/new.html", {
                "form": NewTaskForm()
        })
    
# Edit wikipage
def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
# Save the edit
def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = MdToHtml(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
# Random function
def rand(request):
    allEntries = util.list_entries()
    rand_entry = random.choice(allEntries)
    html_content = MdToHtml(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry,
        "content": html_content
    })


