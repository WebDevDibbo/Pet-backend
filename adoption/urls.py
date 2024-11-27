from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdoptionViewSet, ReviewViewSet, ReviewsViewSet

router = DefaultRouter()
router.register('adopt',AdoptionViewSet, basename='adoption' )
router.register('review',ReviewViewSet, basename='review')
# router.register('reviews',ReviewsViewSet, basename='reviews')

# urlpatterns = router.urls 

urlpatterns = [
   path('',include(router.urls)),
   path('reviews/<int:pet_id>/', ReviewsViewSet.as_view({'get': 'list'}), name='reviews-all')
]
