from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    category_description = models.TextField(null=True)
    category_image = models.ImageField(upload_to='category_images/')

    class Meta:
        ordering = ['category_name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return '{}'.format(self.category_name)


class ProductBrand(models.Model):
    brand_name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    brand_description = models.TextField(null=True)
    brand_image = models.ImageField(upload_to='brand_images/')

    class Meta:
        ordering = ['brand_name']
        verbose_name = 'ProductBrand'
        verbose_name_plural = 'ProductBrands'

    def __str__(self):
        return '{}'.format(self.brand_name)


class ProductSize(models.Model):
    size = models.PositiveIntegerField(default=7, unique=True)

    class Meta:
        ordering = ['size']

    def __str__(self):
        return '{}'.format(self.size)


class Product(models.Model):
    product_name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=250, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(ProductBrand, on_delete=models.SET_NULL, null=True)
    product_description = models.TextField(blank=True)
    product_image = models.ImageField(upload_to='product_images/', blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['product_name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def get_url(self):
        return reverse('detail_view', args=[self.category.slug ,self.slug])


    def __str__(self):
        return '{}'.format(self.product_name)



class ProductVariant(models.Model):
    variant_name = models.CharField(max_length=150, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['product_size']

    def __str__(self):
        return f"{self.product.product_name} - size : {self.product_size.size}"
    

class MultipleImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='multiple_images/', blank=True)

    def __str__(self):
        return self.product.product_name
    



class Coupons(models.Model):
    description = models.TextField(blank=True)
    coupon_code = models.CharField(max_length=20, unique=True)
    coupon_title = models.CharField(max_length=250, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    valid_from = models.DateField(null=True)
    valid_to = models.DateField(null=True)
    quantity = models.PositiveIntegerField(null=True)
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.coupon_code
    


    



    




