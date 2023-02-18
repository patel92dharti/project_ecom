from django.db import models
from django.utils import timezone
# Create your models here.

class User(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    mobile=models.PositiveIntegerField()
    address=models.TextField()
    email=models.EmailField()
    password=models.CharField(max_length=80)
    profile_pic=models.ImageField(upload_to="profile_pic")
    usertype=models.CharField(max_length=100,default="buyer")
    
    def __str__(self) -> str:
        return self.fname+" "+self.lname
class Contact(models.Model):
    name=models.CharField(max_length=100)
    subject=models.CharField(max_length=100)
    message=models.TextField()
    email=models.EmailField()

    def __str__(self):
        return self.name

class Product(models.Model):
    category=(
        ("Men's Dresses","Men's Dresses"),
        ("Women's Dresses","Women's Dresses"),
        ("Baby's Dresses","Baby's Dresses"),

    )
    dressess_category=(
        ("Shirt","Shirt"),
        ("Jeans","Jeans"),
        ("Swimwear","Swimwear"),
        ("Sleepwear","Sleepwear"),
        ("Sportwear","Sportwear"),
        ("Jumpsuits","Jumpsuits"),
        ("Blazers","Blazers"),
        ("Jackets","Jackets"),
        ("Shoes","Shoes"),

    )
    size=(
        ("S","S"),
        ("M","M"),
        ("L","L"),
        ("XL","XL"),
        ("XXL","XXL"),
        ("ALL","ALL"),
    )
    product_seller=models.ForeignKey(User,on_delete=models.CASCADE)
    product_cate=models.CharField(max_length=100,choices=category)
    dressess_cate=models.CharField(max_length=100,choices=dressess_category)
    product_name=models.CharField(max_length=100)
    product_price=models.PositiveIntegerField()
    product_desc=models.TextField()
    product_size=models.CharField(max_length=100,choices=size)
    product_pic=models.ImageField(upload_to="product_pic/")

    def __str__(self) -> str:
        return self.product_seller.fname+" - "+self.product_cate +" - "+self.dressess_cate+" - "+self.product_name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)
    product_price=models.PositiveIntegerField()
    product_qty=models.PositiveIntegerField()
    total_price=models.PositiveIntegerField()
    total_price_shipping=models.PositiveIntegerField(default=100)
    payment_status=models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.user.fname+" - "+self.product.product_name
    
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return self.user.fname+" - "+self.product.product_name


class Shipping_Address(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email=models.EmailField()
    mobile=models.PositiveIntegerField()
    address=models.TextField()
    
    country=(
        ("USA","USA"),
        ("India","India"),
        ("UAE","UAE"),
        ("Kuwait","Kuwait"),

        )
    shipping_country=models.CharField(max_length=100,choices=country)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zip_code=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.fname +" - "+self.city+" - "+self.state+" - "+ self.zip_code

class Billing_Address(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email=models.EmailField()
    mobile=models.PositiveIntegerField()
    address=models.TextField()

    country=(
        ("USA","USA"),
        ("India","India"),
        ("UAE","UAE"),
        ("Kuwait","Kuwait"),

        )
    billing_country=models.CharField(max_length=100,choices=country)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zip_code=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.fname +" - "+self.city+" - "+self.state+" - "+ self.zip_code
class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('DHARTI%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
