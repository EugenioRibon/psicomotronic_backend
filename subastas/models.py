from django.db import models
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):

    name = models.CharField(max_length=50, blank=False, unique=True)

    class Meta:
        ordering=('id',)

    def __str__(self):
        return self.name


class Auction(models.Model):


    title = models.CharField(max_length=150)
    description = models.TextField() 
    closing_date = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.URLField(max_length=1000) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField() 
    category = models.ForeignKey(Category, related_name='subastas', on_delete=models.CASCADE)
    brand = models.CharField(max_length=100) 
    auctioneer = models.ForeignKey(CustomUser, related_name='auctions', on_delete=models.CASCADE)

    class Meta:
        ordering=('id',) 
    
    def __str__(self):  
        return self.title
    
    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if not ratings.exists():
            return 1.0  # valor inicial por defecto
        total = sum(r.value for r in ratings)
        return round(total / ratings.count(), 2)


class Bid(models.Model):
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    auction = models.ForeignKey(Auction, related_name='pujas', on_delete=models.CASCADE)

    class Meta:
        ordering = ('amount',)

    def __str__(self):
        return f"{self.user.username} bid {self.amount} on {self.auction.title}"
    
    
# models.py

class Rating(models.Model):
    value = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='ratings')

    class Meta:
        unique_together = ('user', 'auction')  # <- Cada usuario solo puede valorar una vez por subasta.
        ordering = ('id',)

    def __str__(self):
        return f"{self.user} - {self.value} - {self.auction}"


class Comment(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.user.username}"