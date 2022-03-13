from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import *
from .forms import *
from .helper import *
import os, random


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
abcdpath = BASE_DIR+os.path.sep+"appSocial"+os.path.sep+"abcd"

img_exts = ['jpg','jpeg','bmp','gif','png']

def home(request):
    title = "Home"
    return render(request, "appSocial/home.html", {'title':title,})

def user_signup(request):
    title = 'Sign up here'
    if request.method == 'POST':
        form = CreateNewUser(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # the next two lines will save the user profile data (model) into the table
            naya_user = UserProfile(user=user)
            naya_user.save()
            user = authenticate(username=username, password=raw_password)
            # login(request, user)
            dname = str(user)+"_"+str(request.user.id)
            os.chdir(abcdpath)
            os.mkdir(dname)
            # return redirect('success')
            return render(request, 'appSocial/success.html',{'naya_user':naya_user})
    else:
        form = CreateNewUser()
    return render(request, 'appSocial/signup.html', {'form': form, 'title':title,})


def success(request):
    return render(request, "appSocial/success.html")

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
            password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    dname = str(user)+"_"+str(request.user.id)
                    if not os.path.exists(abcdpath+os.path.sep+dname):
                        os.mkdir(abcdpath+os.path.sep+dname)
                    os.chdir(abcdpath+os.path.sep+dname)
                    print("success changing directory")
                    messages.success(request, "success logging in..")
                    return redirect('display')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        return render(request, 'appSocial/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def upload_image(request):
    if request.method == 'POST':
        print(request.POST)
        form = ImageForm(request.POST, request.FILES)
        # print(dir(request.FILES))
        print(request.FILES['your_image'])
        print(request.user)
        if form.is_valid():
            upld = form.save(commit=False)
            upld.uploaded_by = request.user
            # print("Uploaded by:-->", upld.uploaded_by)
            form.save()
            upload_to_disk(request)
            return redirect('display')
            # return HttpResponse("Image Uploaded.")
    else:
        form = ImageForm()
    return render(request,'appSocial/uploadimage.html', {'form':form,})

@login_required
def display_images(request):

    x,l,s,c = [],[],[],[]
    likes_dict = {}
    shares_dict = {}
    images = Tasveer.objects.all().order_by("?") # .order_by("?") randomizes the queryset
    all_likes = Like.objects.all()
    all_shares = Share.objects.all()
    all_comments = Comment.objects.all()

    for i in range(len(all_likes)):
        l.append(all_likes[i].post.id)

    likes_dict = convert_list_to_ditc(l)

    for j in range(len(all_shares)):
        s.append(all_shares[j].post.id)
    # print(likes_dict)

    for k in range(len(all_comments)):
        c.append(all_comments[k].post_id)

    shares_dict = convert_list_to_ditc(s)
    comments_dict = convert_list_to_ditc(c)
    # print(comments_dict)

    liked_post = Like.objects.filter(user=request.user)
    liked_post_list = liked_post.values_list('post', flat=True)
    alllike_post_list = all_likes.values_list('post', flat=True)
    allpost_list = images.values_list('id',flat=True)
    comment_post_list = all_comments.values_list('post',flat=True)
    # print(dir(liked_post_list))
    # print(all_likes.values())

    # print(liked_post)
    # print("***")

    # print(liked_post)

    for a in images:
        # if "q" in str(a.name):
            # print("yes", a.name)
        aa = str(a.your_image)
        x.append(os.path.basename(aa))
            # print(x)
    if request.method == 'POST' and 'img_upload' in request.POST:
        # print(request.POST)
        form = ImageForm(request.POST, request.FILES)

        # for k,v in request.FILES.items():
        #     print(k,'\t',v)
        # print("******")
        # print(request.FILES['your_image'])
        # print(request.user)
        if form.is_valid():
            upld = form.save(commit=False)
            upld.uploaded_by = request.user
            fn = str(request.FILES['your_image'])
            ext = get_extension(fn)
            # print(ext)
            if ext == "mp4":
                upld.isVideo = 1
                upload_video_to_disk(request)
            else:
                upld.isVideo = False
                upload_to_disk(request)
            # print("Uploaded by:-->", upld.uploaded_by)
            form.save()

            return redirect('display')
            # return HttpResponse("Image Uploaded.")
    # elif request.method == "POST" and 'comment_btn' in request.POST:
    #     print(request.POST)
    #     return redirect('add_comment')

    else:
        form = ImageForm()
        form_comment = CommentForm()


    context = {'images':images, 'naam':x, 'form':form,'form_comment':form_comment,
    'liked_post_list':liked_post_list,'liked_post':liked_post,'all_likes':all_likes,
    'comment_post_list':comment_post_list,'likes_dict':likes_dict,'shares_dict':shares_dict,
    'comments_dict':comments_dict,'all_comments':all_comments,
    'alllike_post_list':alllike_post_list,'allpost_list':allpost_list,}

    return render(request, 'appSocial/display_images.html', context = context )

@login_required
def display_images_by_user(request):
    x = []
    images = Tasveer.objects.filter(uploaded_by=request.user)
    shared_imgs = Share.objects.filter(user=request.user)
    # print(images.count())

    username = request.user
    for a in images:
        # if "q" in str(a.name):
            # print("yes", a.name)
        aa = str(a.your_image)
        x.append(os.path.basename(aa))
            # print(x)

    return render(request, 'appSocial/display-user.html',
     {'images':images,'username':username,'shared_imgs':shared_imgs,})

@login_required
def liked(request, pk):
    post = Tasveer.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    if not already_liked:
        liked_post = Like(post=post, user=request.user)
        liked_post.save()
    return redirect('display')

@login_required

def unliked(request, pk):
    post = Tasveer.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post,user=request.user)
    already_liked.delete()
    return redirect('display')


@login_required
def shared(request, pk):
    post = Tasveer.objects.get(pk=pk)
    shared_post = Share(post=post, user=request.user)
    shared_post.save()
    return redirect('display')


@login_required
def comment_to_post(request, pk):
    allLikedComments_dict = {}
    post = get_object_or_404(Tasveer, pk=pk)
    allCommentsOnPost = Comment.objects.all()
    allLikedComments = LikeComment.objects.all()
    allLikedComments_list = allLikedComments.values_list('post',flat=True)
    allLikedComments_dict = convert_list_to_ditc(allLikedComments_list)
    print(allLikedComments_dict)

    # paginator = Paginator(allCommentsOnPost,3)
    # page = request.GET.get('page',1)
    #
    # try:
    # 	allCommentsOnPost = paginator.page(page)
    # except PageNotAnInteger:
    # 	allCommentsOnPost = paginator.page(1)
    # except EmptyPage:
    # 	allCommentsOnPost = paginator.page(paginator.num_pages)

    if request.method == "POST":
        form_comment = CommentForm(request.POST)
        if form_comment.is_valid():
            comment = form_comment.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            form = CommentForm()
            return render(request, 'appSocial/add-comment.html', {'form':form,'post':post,
            'allCommentsOnPost':allCommentsOnPost,'postid':post.id,'allLikedComments_dict':allLikedComments_dict,})
    else:
        form = CommentForm()
    return render(request, 'appSocial/add-comment.html', {'form': form, 'post':post,
    'allCommentsOnPost':allCommentsOnPost,'postid':post.id,'allLikedComments_dict':allLikedComments_dict,
    'allLikedComments_list':allLikedComments_list,})


@login_required
def like_comment(request, ck):
    # post = Tasveer.objects.get(pk=pk)
    postc = Comment.objects.get(id=ck)
    print(postc)
    already_liked = LikeComment.objects.filter(post=postc, user=request.user)
    if not already_liked:
        liked_comment = LikeComment(post=postc, user=request.user)
        liked_comment.comment_liked = postc
        liked_comment.save()
    return redirect('display')

@login_required
def unlike_comment(request, ck):
    postc = Comment.objects.get(id=ck)
    already_liked = LikeComment.objects.filter(post=postc,user=request.user)
    already_liked.delete()
    return redirect('display')


def profile(request, username):
    d = {}
    post_id_list, likes_count_list = [],[]
    videos_count, images_count = 0,0
    posts_by_user = Tasveer.objects.filter(uploaded_by=request.user)

    for post_by_user in posts_by_user:
        d[post_by_user.id] = post_by_user.liked_image.count()
        if post_by_user.isVideo == 1:
            videos_count += 1
        else:
            images_count += 1

    post_id_list = list(d.keys())
    likes_count_list = list(d.values())
    if len(likes_count_list) > 0:

        id_of_most_liked = post_id_list[likes_count_list.index(max(likes_count_list))]
        most_liked_post = Tasveer.objects.get(id=id_of_most_liked,uploaded_by=request.user)

        context = {'posts_by_user':posts_by_user,
        'id_of_most_liked':id_of_most_liked,'most_liked_post':most_liked_post,
        'videos_count':videos_count, 'images_count':images_count,}
    else:
        context = {'posts_by_user':posts_by_user,
        # 'id_of_most_liked':id_of_most_liked,'most_liked_post':most_liked_post,
        'videos_count':videos_count, 'images_count':images_count,}

    # print(videos_count, images_count)

    # print(most_liked_post)
    # print(id_of_most_liked)
    return render(request, 'appSocial/profile.html', context = context,)

@require_POST
def test(request):
    # id = request.POST.get('id')
    td = request.POST.get('td')
    print(request.POST)
    print(td)


@require_POST
def test_ajax(request):
    id = request.POST.get('id')
    print("test test")
    print(id)
    print(request.POST.get('td'))
