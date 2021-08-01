# AIFFEL_forum_interview
### AIFFEL 학생 포럼 질문게시판 백엔드 서버 구현 명세

---
### < 목차 > 
1. API 호출 패턴 목록
2. 프로젝트 세팅 및 테스트 준비
3. 기존 더미데이터 및 단위테스트 스크립트 활용 빠른 테스트 방법
4. 상세 테스트를 위한 API Document (제시된 양식에 맞춤)
---

## 1. API 호출 패턴 목록
  
- **질문 관련 API**
  - 질문 목록 : Question List
  - 질문 상세 : Question Retrieve
  - 질문 등록 : Question Create
  - 질문 수정 : Question Update
  - 질문 삭제 : Question Delete


- **댓글 관련 API**
  - 질문별 댓글 목록 : Question Comments
  - 댓글 등록 : Comment Create
  - 댓글 상세 : Comment Retrieve


- **추가 기능 API**
  - 키워드 질문 검색 : Question Find
  - 질문 좋아요 / 좋아요 취소 : Question Like
  - 월간 베스트 질문 조회 : Question Monthly Best

## 2. 프로젝트 세팅 및 테스트 준비
- windows cmd 기준 프로젝트 세팅 방법 (python 3.7 설치된 상태로 가정)
  ```commandline
  > git clone https://github.com/wildmental/aiffel_forum_interview.git
  > cd aiffel_forum_interview
  > pycharm64 .  # 또는 기타 IDE 에서 프로젝트 오픈
  ```
  ```commandline
  > py -3.7 -m pip install virtualenv
  > py -3.7 -m virtualenv venv
  > venv\Scripts\activate
  > cd aiffel_forum
  > pip install -r requirements
  > py manage.py runserver
  ```

## 3. 기존 더미데이터 및 단위테스트 스크립트 활용 빠른 테스트 방법
  
  - 웹 브라우저로(DRF Browsable API 활용) 아래 url 목록 조회 (아래 모두 GET 요청 패턴)
    - 질문 목록
      - http://127.0.0.1:8000/questions/
    - 질문 상세 
      - http://127.0.0.1:8000/questions/1/ (~ 1000)
    - 질문별 댓글 
      - http://127.0.0.1:8000/questions/1/comments/ (~ 1000)
    - 댓글 상세 
      - http://127.0.0.1:8000/questions/any/comments/1/ (~ 49500)
    - 키워드 질문 검색 
      - http://127.0.0.1:8000/questions/find/
      - http://127.0.0.1:8000/questions/find/?title_key=모두&content_key=백엔드
      - http://127.0.0.1:8000/questions/find/?title_key=aiffel
      - http://127.0.0.1:8000/questions/find/?content_key=연구소
    - 월간 베스트 질문 조회
      - http://127.0.0.1:8000/questions/monthly_best/
      

- Django Shell 에서 단위테스트 스크립트로 [ POST, PUT, DELETE ] 패턴 테스트
  - runserver 스크립트 유지한 채로 새 cmd 열고 venv 활성화
  ```commandline
  > cd aiffel_forum
  > py manage.py shell
  ```
  ```python
  # 테스트 스크립트 import
  >>> from question import unit_tests
  
  # 질문 등록 수정 삭제 [ POST, PUT, DELETE ]
  >>> unit_tests.create_question() 
  >>> unit_tests.update_question(1) (~1000) question_id
  >>> unit_tests.delete_question(123) (~1000) question_id
  
  # 댓글 등록 [ POST ]
  >>> unit_tests.create_comment(1) (~1000) question_id
  
  # 질문 좋아요 / 좋아요 취소 [ POST ]
  >>> unit_tests.like_question(1)
  ``` 

## 4. 상세 테스트를 위한 API Document (제시된 양식에 맞춤)

- ## Question List
- **URL:** `/questions/`
- **Method:** `GET`
- **URL Params** `none`
- **Request Header:** `none`
- **Sample Call:**
  ```commandline
  curl -XGET "curl -XGET http://localhost:8000/questions/"
  ```
- **Success Response:**
  - **Code:** `200`
  - **Content:**
  ```json
  {
    "count": 1006,
    "next": "http://127.0.0.1:8000/questions/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "created": "2021-08-01T01:20:59.572355Z",
            "modified": "2021-08-01T07:55:42.215700Z",
            "title": "title",
            "content": "content",
            "user": 1,
            "likes": 0
        }, ... ]
  }
  ```

- ## Question Instance
- **URL:** `/questions/:id`
- **Method:** `GET`
- **URL Params** `question_id`
- **Request Header:** `none`
- **Sample Call:**
  ```commandline
  curl -XGET http://localhost:8000/questions/1/
  ```
- **Success Response:**
  - **Code:** `200`
  - **Content:**
  ```json
  {
    "id": 1,
    "created": "2021-08-01T01:20:59.572355Z",
    "modified": "2021-08-01T07:55:42.215700Z",
    "title": "updated question no.1",
    "content": "updated contents for question no.1",
    "user": 1,
    "likes": 92
  }
  ```
- **Error Response:**
  - **Code:** `404`
  - **Content:**
    ```json
    {
      "detail": "Not found."
    }
    ```

- ## Question Find
- **URL:** `/questions/find/:params`
- **Method:** `GET`
- **URL Params** `title_key`, `content_key`
- **Request Header:** `none`
- **Sample Call:**
    ```commandline
    curl -XGET http://localhost:8000/questions/find/?title_key=모두&content_key=백엔드
    ```
- **Success Response:**
  - **Code:** `200`
  - **Content:**
  ```json
  [
    {
        "id": 4006,
        "created": "2021-08-01T17:53:28.951684Z",
        "modified": "2021-08-01T17:53:28.951684Z",
        "title": "모두의연구소",
        "content": "모두의연구소",
        "user": 1,
        "likes": 0
    },
    {
        "id": 4008,
        "created": "2021-08-01T17:54:05.590229Z",
        "modified": "2021-08-01T17:54:05.590229Z",
        "title": "백엔드 엔지니어",
        "content": "백엔드 엔지니어",
        "user": 1,
        "likes": 0
    }, ...
  ]
  ```
- **Error Response:**
  - **Code:** `400`
  - **Content:**
  ```json
  {
    "message": "search keyword is required"
  }
  ```


- ## Question Like
- **URL:** `/questions/:id/like/`
- **Method:** `POST`
- **URL Params** `none`
- **Request Header:** `Authentication needed (username, password)`
- **Sample Call:**
    ```commandline
    curl -XPOST http://localhost:8000/questions/1/like/ --user dummy_user_4:aiffel123!
    ```
- **Success Response:**
  - **Code:** `200`
  - **Content:**
  ```json
  {
    "like_count":93,
    "message":"liked question no.1"
  }
  ```
- **Error Response:**
  - **Code:** `405`
  - **Content:**
  ```json
  {
    "detail": "Method \"GET\" not allowed."
  }
  ```

( 이하 요청패턴 생략 )