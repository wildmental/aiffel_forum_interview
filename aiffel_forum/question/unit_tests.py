import datetime
import random
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.test import APIClient
from question.models import Question, Comment
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
    res = client.post('http://localhost:8000/questions/', new_question, format='json')
    print(res, res.data)


# 질문 수정
def update_question(question_id):
    update_data = {
        'title': f'updated question no.{question_id}',
        'content': f'updated contents for question no.{question_id}',
        'user': test_user.id
    }
    res = client.put(f'http://localhost:8000/questions/{question_id}/', update_data, format='json')
    print(res, res.data)


# 질문 삭제
def delete_question(question_id):
    res = client.delete(f'http://localhost:8000/questions/{question_id}/', format='json')
    print(res, res.data)


# 2. 질문의 댓글을 데이터베이스에 저장하는 API 개발
def create_comment(question_id):
    question = get_object_or_404(Question, id=question_id)
    comment_num = question.comments.count() + 1
    new_comment = {
        'question': question_id,
        'content': f'comment no.{comment_num} for question no.{question_id}',
        'user': test_user.id
    }
    res = client.post(f'http://localhost:8000/questions/{question_id}/comments/', new_comment, format='json')
    print(res, res.data)


# 3. 질문에 달린 댓글 목록을 출력하는 API 개발
def comment_list_from_question(question_id):
    res = client.get(f'http://localhost:8000/questions/{question_id}/comments/', format='json')
    print(res, res.data)

# 4. 키워드로 질문의 제목 또는 본문내용을 검색하는 API 개발
def create_dummy_question_for_search():
    dummy_questions = [{'title': f'모두의연구소', 'content': f'모두의연구소', 'user': test_user.id},
                       {'title': f'AIFFEL', 'content': f'aiffel', 'user': test_user.id},
                       {'title': f'백엔드 엔지니어', 'content': f'백엔드엔지니어', 'user': test_user.id}]
    for new_question in dummy_questions:
        res = client.post('http://localhost:8000/questions/', new_question, format='json')
        print(res, res.data)


def search_question_by_keyword(t_key, c_key):
    res = client.get(f'http://localhost:8000/questions/?title_key={t_key}&content_key={c_key}', format='json')
    print(res, res.data)


# 5. 질문 작성일 기준 각 월별 전체 질문 중에서 가장 좋아요가 많은 질문을 출력하는 API 개발
# 5-1. 질문 좋아요 / 좋아요 취소
def like_question(question_id):
    client.extra = {'request': client.request()}
    client.extra['request'].user = test_user
    res = client.post(f'http://localhost:8000/questions/{question_id}/like/', format='json')
    print(res, res.data)


# 5-2. 더미 데이터 생성
def create_dummy_users():
    # 유저 수 100명까지 생성
    new_user_id = User.objects.all().order_by("-id")[0].id + 1
    bulk_test_user = []
    for i in range(new_user_id, new_user_id + 100):
        user = User(username=f'dummy_user_{i}', password=make_password("aiffel123!"))
        bulk_test_user.append(user)
    User.objects.bulk_create(bulk_test_user)


def create_dummy_questions():
    new_question_id = Question.objects.all().order_by("-id")[0].id + 1
    bulk_question = []
    # 과거 300일 (10 개월) 간의 질문 게시글 1,000개 생성
    for i in range(0, 1000):
        now = datetime.now().astimezone()
        delta = timedelta(days=(i % 300)+1)
        question = Question(created=(now-delta).astimezone(), modified=(now-delta).astimezone(),
                            title=f'question no.{new_question_id+i}',
                            content=f'contents for question no.{new_question_id+i}',
                            # 유저 100명에 더미 질문 균등분배
                            user=User.objects.get(id=(i % 100)+1))
        bulk_question.append(question)
    Question.objects.bulk_create(bulk_question)


def create_dummy_comments():
    # 질문마다 0 ~ 100개 랜덤 개수의 코멘트 생성
    questions = Question.objects.all()
    for question in questions:
        bulk_comment = []
        comment_num = question.comments.count() + 1
        random_comment_cnt = random.randint(1, 101)
        for user in User.objects.filter(id__lt=random_comment_cnt):
            comment = Comment(question=question,
                              content=f'comment no.{comment_num} for question no.{question.id}',
                              user=user)
            bulk_comment.append(comment)
        Comment.objects.bulk_create(bulk_comment)


def create_dummy_likes():
    questions = Question.objects.all()
    for question in questions:
        # 질문마다 0 ~ 100개 랜덤 개수의 좋아요 생성
        random_like_cnt = random.randint(1, 101)
        for like_user in User.objects.filter(id__lt=random_like_cnt):
            client.force_authenticate(user=like_user)
            client.post(f'http://localhost:8000/questions/{question.id}/like/', format='json')


# 5-3. 월별 베스트 질문 리스트
def monthly_best_questions():
    res = client.get(f'http://localhost:8000/questions/monthly_best/', format='json')
    print(res, res.data)

# ------------------------------------------ #
# ## test script ##

# python manage.py shell
# from question import unit_tests

# Question CRUD
# unit_tests.create_question()
# unit_tests.update_question(5)
# unit_tests.delete_question(5)

# Comment CR
# unit_tests.create_comment()
# unit_tests.comment_list_from_question(1)

# Question Search
# unit_tests.create_dummy_question_for_search()
# unit_tests.search_question_by_keyword()

# Question like/unlike
# unit_tests.like_question(1)

# Monthly Best Question
# unit_tests.create_dummy_users()
# unit_tests.create_dummy_questions()
# unit_tests.create_dummy_comments()
# unit_tests.create_dummy_likes()
# unit_tests.monthly_best_questions()
