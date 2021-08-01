from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.test import APIClient
from question.models import Question
client = APIClient()
test_user = User.objects.get(username='root')
client.force_authenticate(user=test_user)


# 단위테스트
# 1. 질문을 데이터베이스에 저장, 수정, 삭제하는 API 개발
# 질문 저장
def create_question():
    new_id = Question.objects.all().order_by("-id")[0].id + 1
    new_question = {
        'title': f'question no.{new_id}',
        'content': f'contents for question no.{new_id}',
        'user': test_user.id
    }
    return client.post('http://localhost:8000/questions/', new_question, format='json')


# 질문 수정
def update_question(question_id):
    update_data = {
        'title': f'updated question no.{question_id}',
        'content': f'updated contents for question no.{question_id}',
        'user': test_user.id
    }
    return client.put(f'http://localhost:8000/questions/{question_id}/', update_data, format='json')


# 질문 삭제
def delete_question(question_id):
    return client.delete(f'http://localhost:8000/questions/{question_id}/', format='json')


# 2. 질문의 댓글을 데이터베이스에 저장하는 API 개발
def create_comment(question_id):
    question = get_object_or_404(Question, id=question_id)
    comment_num = question.comments.count() + 1
    new_comment = {
        'question': question_id,
        'content': f'comment no.{comment_num} for question no.{question_id}',
        'user': test_user.id
    }
    return client.post('http://localhost:8000/comments/', new_comment, format='json')


# 3. 질문에 달린 댓글 목록을 출력하는 API 개발
def comment_list_from_question(question_id):
    return client.get(f'http://localhost:8000/questions/{question_id}/comments/', format='json')


# 4. 키워드로 질문의 제목 또는 본문내용을 검색하는 API 개발
def search_question_by_keyword(keyword):
    pass


# 5. 질문 작성일 기준 각 월별 전체 질문 중에서 가장 좋아요가 많은 질문을 출력하는 API 개발
# 5-1. 질문 좋아요 / 좋아요 취소
def like_question(question_id):
    client.extra = {'request': client.request()}
    client.extra['request'].user = test_user
    print(client.extra['request'].user.is_authenticated)
    return client.post(f'http://localhost:8000/questions/{question_id}/like/', format='json')


# 5-2. 월별 베스트 질문 리스트
def monthly_best_questions():
    pass


# ## test script ##

# from question import unit_tests

# Question CRUD
# unit_tests.create_question()
# unit_tests.update_question(5)
# unit_tests.delete_question(5)

# Comment CR
# unit_tests.create_comment()
# unit_tests.comment_list_from_question(1)

# Question Search
# unit_tests.search_question_by_keyword()

# Question like/unlike
# unit_tests.like_question(1)

# Monthly Best Question
# unit_tests.monthly_best_question()
