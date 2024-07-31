from django.shortcuts import render, redirect

from django.http import Http404

from django.urls import reverse

from django import forms

from . import util

from random import choice

import markdown2


class NewTaskForm(forms.Form):
    title = forms.CharField(label="Entry Title:", max_length=100)
    content = forms.CharField(widget=forms.Textarea ,label="Content:")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, name):
    get = util.get_entry(name)
    if get is not None:
        html = markdown2.markdown(get)
        return render(request, "encyclopedia/entry.html", {
            "title": html,
            "name": name.capitalize(),
        })
    else:
        list = [list for list in util.list_entries() if name.lower() in list.lower()]
        if not list:
            raise Http404("The requested page does not exist")
        return render(request, "encyclopedia/list.html", {
            "list": list,
            "name": name,
        })

def newpage(request):
    # return render(request, "encyclopedia/newpage.html")
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                form.add_error("title",f"An entry with title:{title} already exists")
                return render(request, "encyclopedia/newpage.html", {
                    "form": form
                })
            util.save_entry(title, content)
            return redirect("encyclopedia:entry", name=title)
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })

    return render(request, "encyclopedia/newpage.html", {
        "form": NewTaskForm()
    })

def edit(request, name):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]   
            util.save_entry(title, content)
            return redirect("encyclopedia:entry", name=title)
    entry_content = util.get_entry(name)
    form = NewTaskForm(initial={'title': name, 'content': entry_content})
    return render(request, "encyclopedia/edits.html", {
        "form": form,
        "name": name,
    })

def random(request):
    new = choice(util.list_entries())
    return redirect("encyclopedia:entry", name=new)


def search(request):
    query = request.GET.get('q')
    if query:
        return redirect('encyclopedia:entry', name=query)
    return redirect('encyclopedia:index')

