from django.db import models


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=150, unique=True)
    category_description = models.TextField(null=True)
    category_image = models.ImageField(upload_to='category_images/')

    class Meta:
        ordering = ['category_name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return '{}'.format(self.category_name)


class ProductBrand(models.Model):
    brand_name = models.CharField(max_length=150, unique=True)
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)
    product_description = models.TextField(blank=True)
    product_image = models.ImageField(upload_to='product_images/', blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['product_name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return '{}'.format(self.product_name)


class ProductVariant(models.Model):
    variant_name = models.CharField(max_length=150, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['product_size']

    def __str__(self):
        return f"{self.product_id.product_name} - size : {self.product_size.size}"
    

class MultipleImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=250, null=False, default='product')
    images = models.ImageField(upload_to='multiple_images/', blank=True)




