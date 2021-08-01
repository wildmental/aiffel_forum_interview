from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User
from datetime import datetime


class Question(TimeStampedModel):
    # 참조 필드
    user = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    like_users = models.ManyToManyField(User, blank=True, related_name='like_questions')

    # 모델 필드
    title = models.CharField(max_length=64, verbose_name='title')
    content = models.TextField(max_length=250, verbose_name='question_txt')

    def like_users_cnt(self):
        return self.like_users.count()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'question'
        verbose_name = 'forum question'
        verbose_name_plural = 'forum questions'


class Comment(TimeStampedModel):
    # 참조 필드
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='comments', on_delete=models.CASCADE)

    # 모델 필드
    content = models.TextField(max_length=250, verbose_name='comment_txt')

    class Meta:
        db_table = 'comment'
        verbose_name = 'forum comment'
        verbose_name_plural = 'forum comments'
