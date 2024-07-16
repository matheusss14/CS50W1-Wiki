from django.shortcuts import render, redirect
from django.http import HttpResponse

from markdown2 import Markdown
from random import choice
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title": "All Pages"
    })

def page(request, page):
    content = MDtoHTML(page)
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "page": f"{page} is not a valid entry."
        })
    else:
        return render(request, "encyclopedia/page.html", {
            "page": page,
            "content": content
        })
    
def search(request):
    if request.method == "POST":
        entry = request.POST['q']
        exists = MDtoHTML(entry)
        if exists:
            return render(request, "encyclopedia/page.html", {
            "page": entry,
            "content": exists
        })
        else:
            entries = util.list_entries()
            related = []
            for i in entries:
                if entry.lower() in i.lower():
                    related.append(i)
            return render(request, "encyclopedia/index.html", {
                "entries": related,
                "title": "Results:"
            })


def new(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST["content"]
        exists = util.get_entry(title)
        if exists is not None:
            return render(request, 'encyclopedia/error.html', {
                "page": 'entry already exists'
            })
        else:
            util.save_entry(title, content)
            return redirect(f'wiki/{title}')
    else:
        return render(request, "encyclopedia/new.html")
    
def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "page": title,
            "content": content,
        })

def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect(f'wiki/{title}')
    
def random(request):
    entries = util.list_entries()
    random = choice(entries)
    return redirect(f'wiki/{random}')

def MDtoHTML(file):
    content = util.get_entry(file)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


