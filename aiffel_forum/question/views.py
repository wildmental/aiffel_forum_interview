import os
import sqlite3
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from aiffel_forum.permissions import IsOwnerOrReadOnly
from question.models import Question, Comment
from question.serializers import QuestionSerializer, CommentSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsOwnerOrReadOnly, ]
    pagination_class = PageNumberPagination

    @action(methods=["POST"], detail=True)
    def like(self, request, *args, **kwargs):
        question = get_object_or_404(Question, id=kwargs['pk'])
        like_users = question.like_users
        user = request.user

        if user.is_anonymous:
            res_msg = {'message': 'Authentication is needed to like questions'}
            return Response(res_msg, status=status.HTTP_400_BAD_REQUEST)

        try:
            like_users.get(id=user.id)
            question.like_users.remove(user)
            message = f'unliked question no.{question.id}'
        except ObjectDoesNotExist as e:
            question.like_users.add(user)
            message = f'liked question no.{question.id}'
        res_msg = {'like_count': question.like_users.count(), 'message': message}
        return Response(res_msg)

    @action(methods=["GET"], detail=False)
    def monthly_best(self, request, *args, **kwargs):
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        with open(os.getcwd()+'/question/monthly_best.sql') as stmt:
            cur.execute(stmt.read())
        monthly_bests = self.queryset.filter(id__in=[row[1] for row in cur.fetchall()]).order_by('-created')
        res_data = self.serializer_class(monthly_bests, many=True).data
        return Response(res_data)

    @action(methods=["GET"], detail=False)
    def find(self, request, *args, **kwargs):
        title_key = request.query_params.get('title_key', None)
        content_key = request.query_params.get('content_key', None)

        title_search, content_search, search_res = None, None, None
        if title_key:
            title_search = self.queryset.filter(title__icontains=title_key)
        if content_key:
            content_search = self.queryset.filter(content__icontains=content_key)

        search_res = title_search | content_search if title_key and content_key \
            else title_search if title_key else content_search if content_key else None

        if search_res is None:
            return Response({'message': "search keyword is required"})

        res_data = self.serializer_class(search_res, many=True).data
        return Response(res_data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related("question")
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, ]
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        question_comments = get_object_or_404(Question, id=kwargs['question_pk']).comments.all()

        page = self.paginate_queryset(question_comments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        comments_data = CommentSerializer(instance=question_comments, many=True).data
        return Response(comments_data)
