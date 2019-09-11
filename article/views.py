from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .forms import ArticleForm
from .models import Article,Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json
from django.urls import reverse
# Create your views here.

def articles(request):
    keyword = request.GET.get("keyword")
    keyword2 = request.GET.get("keyword2")

    if keyword and keyword2:
            print("sa")
            articles =Article.objects.filter(id__contains = keyword2,title__contains = keyword)
            messages.success(request,"Id ve Cihaz ismine ait cihazlar görüntüleniyor.")
            return render(request,"articles.html",{"articles":articles})

    messages.warning(request,"Bulunamadı.Lütfen Cihaz id'sini ve ismini doğru girdiğinizden emin olun.")

    return render(request,"articles.html")

def index(request):
    context = {
        "numbers":[1,2,3,4,5]
    }
    return render(request,"index.html",context)

def dashboard():
    context = {
        "numbers":[1,2,3,4,5]
    }
    return render(request,"dashboard.html",context)

def about(request):
    return render(request,"about.html")
@login_required(login_url = "user:login")
def dashboard(request):
    articles =Article.objects.all()
    context = {
        "articles":articles
    }

    return render(request,"dashboard.html",context)
@login_required(login_url = "user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    
    if form.is_valid():
        article = form.save(commit = False)
        article.author = request.user
        article.save()
        """
        article objesini oluşturuyor.
        bizim articleyi oluştur ama save yapma onu ben yapıcam demek lazım
        article.save() yapıyor
        """
        messages.success(request,"Makale başarıyla oluşturuldu.")
        return redirect("dashboard")

    return render(request,"addarticle.html",{"form":form})

def detail(request,id):
    #article = Article.objects.filter(id = id).first()
    article =  get_object_or_404(Article,id = id)

    comments = article.comments.all()
    return render(request,"detail.html",{"article":article,"comments":comments})
@login_required(login_url = "user:login")
def update(request,id):

    article = get_object_or_404(Article,id=id)
    form = ArticleForm(request.POST or None,request.FILES or None,instance = article)
    if form.is_valid():
        article = form.save(commit = False)
        article.author = request.user
        article.save()
        """
        article objesini oluşturuyor.
        bizim articleyi oluştur ama save yapma onu ben yapıcam demek lazım
        article.save() yapıyor
        """
        messages.success(request,"Makale başarıyla güncellendi.")
        return redirect("dashboard")
    
    return render(request,"update.html",{"form":form})
@login_required(login_url = "user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id = id)

    article.delete()

    messages.success(request,"Makale Başarıyla Silindi")

    return redirect("dashboard")
def addComment(request,id):
    article = get_object_or_404(Article,id = id)
    
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        newComment = Comment(comment_author = comment_author,comment_content = comment_content)

        newComment.article = article

        newComment.save()

    return redirect(reverse("article:detail",kwargs={"id":id}))#Dinamik url yapısı reverse fonksiyonuyla daha iyi olur

