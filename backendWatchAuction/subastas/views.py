from .models import Auction, Category, Bid,Rating,Comment
from .serializers import AuctionListCreateSerializer, AuctionDetailSerializer, CategoryListCreateSerializer, CategoryDetailSerializer, BidListCreateSerializer, BidDetailSerializer,RatingListCreateSerializer,CommentSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin
from rest_framework import generics, permissions




class AuctionListCreate(generics.ListCreateAPIView):
    
    '''ListCreateAPIView:
        - Maneja las operaciones de listar (GET) y crear (POST) recursos.
        - Proporciona una lista paginada de recursos y permite la creación de nuevos recursos.
        - Útil para endpoints que necesitan mostrar una lista de recursos y permitir la creación
        de nuevos recursos.'''

    serializer_class = AuctionListCreateSerializer

    def get_queryset(self):

        queryset = Auction.objects.all()
        params = self.request.query_params

        search = params.get('search')
        categoria = params.get('categoria')
        precio_max = params.get('precioMax')
        precio_min = params.get('precioMin')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        if categoria:
            queryset = queryset.filter(category__name__iexact=categoria)

        if precio_min:
            queryset = queryset.filter(price__gte=precio_min)

        if precio_max:
            queryset = queryset.filter(price__lte=precio_max)

        return queryset
    
    def perform_create(self, serializer):
        serializer.save(auctioneer=self.request.user)

class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    '''
    RetrieveUpdateDestroyAPIView:
        - Maneja las operaciones de recuperar (GET), actualizar (PUT) y eliminar (DELETE) un
        recurso individual.
        - Combina las funcionalidades de las vistas RetrieveAPIView, UpdateAPIView y
        DestroyAPIView.
        - Útil para endpoints que necesitan mostrar un recurso específico y permitir su
        actualización y eliminación.'''
    
    permission_classes = [IsOwnerOrAdmin]
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

class CategoryListCreate(generics.ListCreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoryListCreateSerializer

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class BidListCreateView(generics.ListCreateAPIView):

    serializer_class = BidDetailSerializer

    def get_queryset(self):
        return Bid.objects.filter(auction_id=self.kwargs['auction_id']).order_by('-amount')

    def perform_create(self, serializer):
        auction = Auction.objects.get(pk=self.kwargs['auction_id'])  # obtiene el objeto completo
        serializer.save(auction=auction, user=self.request.user)


class UserBidListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = BidDetailSerializer

    def get_queryset(self):
        return Bid.objects.filter(user=self.request.user)

class BidDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = BidDetailSerializer

    def get_queryset(self):
        return Bid.objects.filter(auction_id=self.kwargs['auction_id']) 
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class UserAuctionListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Obtener las subastas del usuario autenticado
        user_auctions = Auction.objects.filter(auctioneer=request.user)
        serializer = AuctionListCreateSerializer(user_auctions, many=True)
        return Response(serializer.data)
    
    
# views.py

class RatingListCreate(generics.GenericAPIView):
    serializer_class = RatingListCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(auction_id=self.kwargs['auction_id'])

    def get(self, request, auction_id):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, auction_id):
        value = request.data.get("value")
        if value is None:
            return Response({"error": "Se requiere un valor"}, status=400)

        rating, created = Rating.objects.update_or_create(
            user=request.user,
            auction_id=auction_id,
            defaults={"value": value}
        )
        serializer = self.serializer_class(rating)
        return Response(serializer.data, status=201 if created else 200)

    def delete(self, request, auction_id):
        try:
            rating = Rating.objects.get(user=request.user, auction_id=auction_id)
            rating.delete()
            return Response(status=204)
        except Rating.DoesNotExist:
            return Response({"error": "No tienes valoración registrada"}, status=404)

        
class RatingDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RatingListCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo permite acceder a valoraciones propias
        return Rating.objects.filter(user=self.request.user)
    
    
    



class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]  # Cualquiera puede ver, pero crear requiere auth

    def get_queryset(self):
        return Comment.objects.filter(auction_id=self.kwargs['auction_id'])

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, auction_id=self.kwargs['auction_id'])


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
