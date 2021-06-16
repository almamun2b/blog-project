from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.signals import user_logged_in 
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import author, category, article, comment
from .forms import crateForm, RegisterForm, AuthorForm, CommentForm, CategoryForm
from django.contrib.auth.decorators import login_required


def index(request):
    posts = article.objects.all()
    posts = posts.filter().order_by('-posted_on')

    search = request.GET.get('search')
    
    if search:
        posts = posts.filter(
            Q(title__icontains=search)
            |
            Q(body__icontains=search)
        )
        
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    total_article = paginator.get_page(page)

    context = {
        'posts': total_article
    }
    return render(request, 'index.html', context)


@login_required(login_url="login")
def getauthor(request, name):
    post_author = get_object_or_404(User, username=name)
    auth = get_object_or_404(author, name=post_author.id)
    post = article.objects.filter(article_author=auth.id)
    post = post.order_by('-posted_on')

    paginator = Paginator(post, 4)
    page = request.GET.get('page')
    total_article = paginator.get_page(page)

    context = {
        'auth': auth,
        'post': total_article
    }
    return render(request, 'profile.html', context)


def getsingle(request, id):
    post = get_object_or_404(article, pk=id)
    
    first = article.objects.first()
    last = article.objects.last()
    
    # first = article.objects.order_by('posted_on').first()
    # last = article.objects.order_by('posted_on').last()

    getComment = comment.objects.filter(post=id)

    related = article.objects.filter(category=post.category).exclude(id=id)[:4]
    form = CommentForm(request.POST or None)
    
    if form.is_valid():
        instance= form.save(commit=False)
        instance.post = post
        instance.save()
    
    context = {
        'post': post,
        'first': first,
        'last': last,
        'related': related,
        'form': form,
        'comment': getComment
    }
    return render(request, 'single.html', context)


def gettopic(request, name):
    cat = get_object_or_404(category, name=name)
    posts = article.objects.filter(category=cat.id)
    posts = posts.filter().order_by('-posted_on')

    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    total_article = paginator.get_page(page)

    context = {
        'posts': total_article,
        'cat': cat
    }
    return render(request, 'category.html', context)


def getlogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)

            if auth is not None:
                login(request, auth)
                return redirect('index')
            else:
                messages.add_message(
                    request, messages.ERROR, 'Username or password mismatch')
                return render(request, 'login.html')

    return render(request, 'login.html')
    # return render(request, 'login.html', {'error': 'Username or Password Wrong'})


def getlogout(request):
    logout(request)
    return redirect('index')


def getcreate(request):
    if request.user.is_authenticated:
        user = get_object_or_404(author, name=request.user.id)
        form = crateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = user
            instance.save()
            return redirect('index')
        return render(request, 'create.html', {'form': form})
    else:
        return redirect('login')


def getupdate(request, id):
    if request.user.is_authenticated:
        user = get_object_or_404(author, name=request.user.id)
        post = get_object_or_404(article, id=id)
        form = crateForm(request.POST or None,
                         request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = user
            instance.save()
            messages.success(request, 'Article Updated successfully')
            return redirect('profile')

        return render(request, 'create.html', {'form': form})

    else:
        return redirect('login')


def getdelete(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(article, id=id)
        post.delete()
        messages.warning(request, 'Article Delated')

        return redirect('profile')

    else:
        return redirect('login')


# def getprofile(request):
#     if request.user.is_authenticated:
#         user = get_object_or_404(author, name=request.user.id)
#         post = article.objects.filter(article_author=user.id)
#         return render(request, 'logged_in_profile.html', {'post': post, 'user': user})

#     else:
#         return redirect('login')


def getprofile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        author_profile = author.objects.filter(name=user.id)

        if author_profile:
            authorUser = get_object_or_404(author, name=request.user.id)
            post = article.objects.filter(article_author=authorUser.id)
            post = post.filter().order_by('-posted_on')
            return render(request, 'logged_in_profile.html', {'post': post, 'user': authorUser})
        else:
            form = AuthorForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = user
                instance.save()
                return redirect('profile')

            return render(request, 'createauthor.html', {'form': form})

    else:
        return redirect('login')


def getregister(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Registration success')
        return redirect('login')
    return render(request, 'register.html', {'form': form})


def getCategory(request):
    query = category.objects.all()
    query = query.filter().order_by('name')
    return render(request, 'topics.html', {'topic': query})


def createTopic(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            form = CategoryForm(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, 'Topic Create')
                return redirect('category')            
            return render(request, 'create_topics.html', {'form': form})
        else:
            raise Http404("You are not authorized to access the page")
    else:
        return redirect('login')
