from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('latest', views.LatestRevisionAPIView.as_view()),
    path('all', views.AllRevisionsAPIView.as_view()),
    path('revision<int:revision_id>/', views.GetRevisionAPIView.as_view()),
    path('visit/<str:public_id>/', views.UpdateDeleteVisitAPIView.as_view()),
    path('', views.AddVisitAPIView.as_view())
]