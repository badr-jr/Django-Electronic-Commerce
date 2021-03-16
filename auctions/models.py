from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Categories(models.Model):
    code = models.CharField(max_length=3)
    category = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.category}"
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid = models.IntegerField()
    image = models.TextField()
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    listing_owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="owners")
    winner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="winners",null=True)
    def __str__(self):
        return f"title:{self.title} descrip:{self.description}"
class Bid(models.Model):
    bid = models.IntegerField()
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return f"Bid: {self.bid}"
class Comment(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    commenator = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return f"comment: '{self.comment}' (by) {self.commenator}"
class Watchlist(models.Model):
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="user_watchlists")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
