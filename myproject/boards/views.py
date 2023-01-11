from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .forms import NewTopicForm, PostForm
from .models import Board, Topic, Post


def home(request: HttpRequest) -> HttpResponse:
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_topics(request: HttpRequest, pk: int) -> HttpResponse:
    # without get_object_or_404 approach
    # try:
    # board = Board.objects.get(pk=pk)
    # except Board.DoesNotExist:
    #     raise Http404

    # board = get_object_or_404(Board, pk=pk)
    # return render(request, 'topics.html', {'board': board})
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})

# def new_topic_invalid(request: HttpRequest, pk: int) -> HttpResponse:
#     """
#     This view is only considering the happy path, which is receiving the data and saving it into the database.
#     But there are some missing parts. We are not validating the data.
#     The user could submit an empty form or a subject that's bigger than 255 characters
#     """
#     board = get_object_or_404(Board, pk=pk)
#
#     if request.method == 'POST':
#         subject = request.POST['subject']
#         message = request.POST['message']
#
#         # Hard-coded the USER retrieval logic, since auth is not yet implemented
#         user = User.objects.first()  # TODO: get the currently logged in user
#
#         topic = Topic.objects.create(
#             subject=subject,
#             board=board,
#             starter=user
#         )
#
#         return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
#
#     return render(request, 'new_topic.html', {'board': board})


@login_required
def new_topic(request: HttpRequest, pk: int) -> HttpResponse:
    board = get_object_or_404(Board, pk=pk)
    # user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            # topic.starter = user
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )

            # TODO: potential_defect: redirect to board_topics instead of topic_posts
            # return redirect('board_topics', pk=board.pk)
            """  
            Very important: in the view reply_topic we are using topic_pk because we are referring to 
            the keyword argument of the function, in the view new_topic we are using topic.pk because a topic 
            is an object (Topic model instance) and .pk we are accessing the pk property of the Topic model instance. 
            Small detail, big difference.
            """
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

    # if request.method == 'POST':
    #     form = NewTopicForm(request.POST)
    #     if form.is_valid():
    #         topic = form.save()
    #         return redirect('board_topics', pk=board.pk)
    # else:
    #     form = NewTopicForm()
    # return render(request, 'new_topic.html', {'form': form})


def topic_posts(request: HttpRequest, pk: int, topic_pk: int):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


def reply_topic(request: HttpRequest, pk: int, topic_pk: int):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # TODO: Potential defect: remove commit=False from line below
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)

    # TODO: Potential defect: indent the 'else' from below
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})
