from question.models import Question, Comment
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(method_name='count_likes')

    class Meta:
        model = Question
        fields = ["id", "created", "modified", "title",
                  "content", "user", "likes"]

    def count_likes(self, question):
        return question.like_users.count()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
