from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework_nested import routers
from account.views import UserViewSet
from question.views import QuestionViewSet
from question.views import CommentViewSet
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='AIFFEL Forum API')

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'questions', QuestionViewSet)
question_router = routers.NestedSimpleRouter(router, r'questions', lookup='question')
question_router.register(r'comments', CommentViewSet, basename='question-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(question_router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('schema/', schema_view),
]
