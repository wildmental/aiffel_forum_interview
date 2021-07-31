from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Question(models.Model):
    # 참조 필드
    user = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)

    # 모델 필드
    created = models.DateTimeField(default=datetime.now())
    title = models.CharField(max_length=64, verbose_name='title')
    content = models.TextField(max_length=250, verbose_name='question_txt')
    likes = models.IntegerField(default=0)

    class Meta:
        db_table = 'question'
        verbose_name = 'forum question'
        verbose_name_plural = 'forum questions'


class Comment(models.Model):
    # 참조 필드
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='comments', on_delete=models.CASCADE)

    # 모델 필드
    created = models.DateTimeField(default=datetime.now())
    content = models.TextField(max_length=250, verbose_name='comment_txt')

    class Meta:
        db_table = 'comment'
        verbose_name = 'forum comment'
        verbose_name_plural = 'forum comments'
