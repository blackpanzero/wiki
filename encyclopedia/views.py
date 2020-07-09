from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseNotFound
from django.urls import reverse
from django.db.models import Q
import re

import random


from . import util

# For document conversion
import markdown2



def index(request):
    entry=util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),"random":random.choice(entry)
    })
def new(request):
    entry=util.list_entries()
    if request.method=="POST":
        title=request.POST["title"]
        titlecap=title.capitalize()
        titleupp=title.upper()
        titlelow=title.lower()
        if titlecap in entry or titleupp in entry or titlelow in entry:
            return render(request,"encyclopedia/new_entry.html",{"random":random.choice(entry),"message":"entry already exists","title":title})
        content=request.POST["content"]
        util.save_entry(title,content)  
        return HttpResponseRedirect(reverse("page", args = (title,)))


    return render(request,"encyclopedia/new_entry.html",{"random":random.choice(entry) })


def page(request,name):
    entry=util.list_entries()
    content=util.get_entry(name)
    markdowner = markdown2.Markdown()
    try:
        out_text = markdowner.convert(content)
    except TypeError:
        return HttpResponseNotFound('<h1>Sorry Page not found</h1>')
    print(out_text)
    return render(request, "encyclopedia/page.html", {"content":out_text,"random":random.choice(entry),"name":name})
   
    
def edit_page(request, editPage):
    entry=util.list_entries()
    content = util.get_entry(editPage)
    if request.method=="POST":
        content=request.POST["edit-content"]
        util.save_entry(editPage,content)
        return HttpResponseRedirect(reverse("page", args = (editPage,)))  
        
    return render(request, "encyclopedia/edit.html", {
        "page_title": editPage,
        "content": content,
        "random":random.choice(entry)
    })
def search(request):
    query = request.POST["q"] 
    querycap=query.capitalize()
    queryupp=query.upper()
    querylow=query.lower()  
    
    matches=[]
    #Check if the string contains "ai" followed by 1 or more "x" characters:
    entry=util.list_entries()
    
    if querycap in entry:
        return HttpResponseRedirect(reverse("page", args = (querycap,)))
    elif queryupp in entry:
        return HttpResponseRedirect(reverse("page", args = (queryupp,)))
    elif querylow in entry:
        return HttpResponseRedirect(reverse("page", args = (querylow,)))
  

    for t in entry:
        if re.findall(query.capitalize(), t) or re.findall(query.upper(), t) or re.findall(query.lower(), t):
            matches.append(t)
    
        
    return render(request,"encyclopedia/search.html",{"contents":matches,
    "random":random.choice(entry),"query":query})







