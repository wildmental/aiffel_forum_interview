from django.contrib.auth.models import User
from question.models import Question, Comment
from rest_framework.test import APIClient


# 단위테스트
# 1. 질문을 데이터베이스에 저장, 수정, 삭제하는 API 개발
# 질문 저장
def create_question():
    client = APIClient()
    test_user = User.objects.get(username='root')
    client.force_authenticate(user=test_user)

    # question contents
    new_id = Question.objects.all().order_by("-id")[0].id + 1
    question = {
        'title': 'question no.' + str(new_id),
        'content': 'contents for question no.' + str(new_id),
        'user': test_user.id
    }
    return client.post('http://localhost:8000/questions/', question, format='json')


# 질문 수정
def update_question():
    pass


# 질문 삭제
def delete_question():
    pass


# 2. 질문의 댓글을 데이터베이스에 저장하는 API 개발
def create_comment():
    pass


# 3. 질문에 달린 댓글 목록을 출력하는 API 개발
def comment_list_from_question():
    pass


# 4. 키워드로 질문의 제목 또는 본문내용을 검색하는 API 개발
def search_question_by_keyword():
    pass


# 5. 질문 작성일 기준 각 월별 전체 질문 중에서 가장 좋아요가 많은 질문을 출력하는 API 개발
def monthly_best_question():
    pass


# ## django shell - test script ##
# from question import unit_tests
# unit_tests.create_question()
# unit_tests.update_question()
# unit_tests.delete_question()
# unit_tests.comment_list_from_question()
# unit_tests.search_question_by_keyword()
# unit_tests.monthly_best_question()
