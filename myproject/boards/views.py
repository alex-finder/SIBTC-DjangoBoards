from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404
from django.contrib.auth.decorators import login_required

from .forms import NewTopicForm
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
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})


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
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
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
    return render(request, 'topic_posts.html', {'topic': topic})
