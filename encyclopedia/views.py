from django.shortcuts import render
from random import choice
from markdown2 import Markdown

from . import util

converter = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    file = util.get_entry(title)
    if file == None:
        return render(request, "encyclopedia/error.html", {
            "error": "The entry does not exist"
        })

    content = converter.convert(file)
    return render(request, "encyclopedia/entries.html", {
        "title": title,
        "content": content
    })


def search(request):
    if request.method == 'POST':
        formSearch = request.POST['q']
        if util.get_entry(formSearch) is not None:
            content = converter.convert(util.get_entry(formSearch))
            return render(request, "encyclopedia/entries.html", {
                "title": formSearch,
                "content": content
            })
        else:
            Newlist = []
            entries = util.list_entries()
            for name in entries:
                if formSearch.lower() in name.lower():
                    Newlist.append(name)
            return render(request, "encyclopedia/index.html", {
                "entries": Newlist
            })

def newPage(request):
    if request.method == 'POST':
        title = request.POST['title']
        entries = util.list_entries()
        for name in entries:
            if title.lower() == name.lower():
                return render(request, "encyclopedia/error.html", {
                    "error": "The entry already exists"
                })

        content = request.POST['content']
        fileName = "entries/" + title + ".md"
        with open(fileName, 'w') as f:
            f.write("#" + title + "\n\n" + content)
        mdc = util.get_entry(title)
        newContent = converter.convert(mdc)
        return render(request, "encyclopedia/entries.html", {
            "title": title,
            "content": newContent
        })

    else:
        return render(request, "encyclopedia/newPage.html")


def edit(request, title):
    if request.method == 'POST':
        content = request.POST['editcontent']
        fileName = "entries/" + title + ".md"
        with open(fileName, 'w') as f:
            f.write("#" + title + "\n\n" + content)
        newcontent = converter.convert(util.get_entry(title))
        return render(request, "encyclopedia/entries.html", {
            "title": title,
            "content": newcontent
        })

    MDcontent = util.get_entry(title)
    content = MDcontent.split("\n", 2)[2]
    return render(request, "encyclopedia/edit.html", {
        "content": content,
        "title": title
    })

def random(request):
    entries = util.list_entries()
    title = choice(entries)
    content = converter.convert(util.get_entry(title))
    return render(request, "encyclopedia/entries.html", {
        "title": title,
        "content": content
    })