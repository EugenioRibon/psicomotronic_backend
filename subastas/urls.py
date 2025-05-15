from django.urls import path
from .views import (
    AuctionListCreate,
    AuctionRetrieveUpdateDestroy, 
    CategoryListCreate, 
    CategoryRetrieveUpdateDestroy, 
    UserAuctionListView, 
    UserBidListView, 
    BidListCreateView, 
    BidDetailView,
    RatingListCreate,
    RatingDetail,
    CommentListCreateView,
    CommentRetrieveUpdateDestroyView
    )


app_name="subastas"

urlpatterns = [
    # Categories
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),

    # Auctions
    path('', AuctionListCreate.as_view(), name='auction-list-create'),
    path('<int:pk>/', AuctionRetrieveUpdateDestroy.as_view(), name='auction-detail'),

    # Bids
    path('<int:auction_id>/bid', BidListCreateView.as_view(), name='bid-list-create'),
    path('<int:auction_id>/bid/<int:pk>', BidDetailView.as_view(), name='bid-detail'),

    # Ratings
    path('<int:auction_id>/ratings/', RatingListCreate.as_view(), name='rating-list-create'),
    path('ratings/<int:pk>/', RatingDetail.as_view(), name='rating-detail'),

    # Users
    path('users/', UserAuctionListView.as_view(), name='action-from-users'),
    path("users/bids/", UserBidListView.as_view(), name="user-bid-list"),
    
    #Comments
    # urls.py

    path('<int:auction_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),

]
