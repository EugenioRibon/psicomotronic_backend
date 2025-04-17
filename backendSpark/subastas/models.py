from django.db import models
from users.models import CustomUser

class Category(models.Model):

    name = models.CharField(max_length=50, blank=False, unique=True)

    class Meta:
        ordering=('id',)

    def __str__(self):
        return self.name


class Auction(models.Model):

    '''Modelo de subasta'''


    title = models.CharField(max_length=150)
    description = models.TextField() 
    closing_date = models.DateTimeField()
    creation_date = models.DateTimeField() 
    thumbnail = models.URLField() 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField() 
    rating = models.DecimalField(max_digits=3, decimal_places=2) 
    category = models.ForeignKey(Category, related_name='subastas', on_delete=models.CASCADE)
    brand = models.CharField(max_length=100) 
    auctioneer = models.ForeignKey(CustomUser, related_name='auctions', on_delete=models.CASCADE)

    class Meta:
        ordering=('id',) 
    
    def __str__(self):  
        return self.title


class Bid(models.Model):
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    auction = models.ForeignKey(Auction, related_name='pujas', on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f"{self.user.username} bid {self.amount} on {self.auction.title}"