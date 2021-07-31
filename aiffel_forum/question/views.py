from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from question.models import Question, Comment
from question.serializers import QuestionSerializer, CommentSerializer
from question.permissions import IsOwnerOrReadOnly


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = PageNumberPagination


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related("question")
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = PageNumberPagination

