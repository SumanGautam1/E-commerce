from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Categories of Products
class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	
	class Meta:
		verbose_name_plural = 'categories'
		
    
# All of our Products
class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.PositiveIntegerField()
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	description = models.CharField(max_length=250, default='', blank=True, null=True)
	image = models.ImageField(upload_to='uploads/product/')

	def __str__(self):
		return self.name
	
class CartItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.quantity} x {self.product.name}'
	
	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total




class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
	

class Customer(models.Model):
		name = models.CharField(max_length=200)
		email = models.EmailField()
		phone = models.CharField(max_length=10)
		address = models.CharField(max_length=50)
		city = models.CharField(max_length=50)
		state = models.CharField(max_length=50)

		def __str__(self):
			return self.name