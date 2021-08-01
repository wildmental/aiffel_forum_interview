import json
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from aiffel_forum.permissions import IsOwner, IsOwnerOrReadOnly
from question.models import Question, Comment
from question.serializers import QuestionSerializer, CommentSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    permission_action_mapping = {
        'like': IsAuthenticated
    }
    pagination_class = PageNumberPagination

    @action(methods=["POST"], detail=True)
    def like(self, request, *args, **kwargs):
        question = get_object_or_404(Question, id=kwargs['pk'])
        like_users = question.like_users
        user = request.user

        if like_users.exists():
            if like_users.get(id=user.id):
                question.like_users.remove(user)
                message = f'unliked question no.{question.id}'
            else:
                question.like_users.add(user)
                message = f'liked question no.{question.id}'
        else:
            question.like_users.add(user)
            message = f'liked the question no.{question.id}'

        context = {'like_count': question.like_users.count(), 'message': message}
        return Response(json.dumps(context), content_type="application/json")


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related("question")
    serializer_class = CommentSerializer
    permission_classes = [IsOwner, IsOwnerOrReadOnly]
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        question_comments = get_object_or_404(Question, id=kwargs['question_pk']).comments.all()

        page = self.paginate_queryset(question_comments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        comments_data = CommentSerializer(instance=question_comments, many=True).data
        return Response(comments_data)
