from django.db import models
from django.contrib.auth.models import User


class Banner(models.Model):
    image = models.ImageField(upload_to='hb')
    image1 = models.ImageField(upload_to='hb', blank=True, null=True)
    image2 = models.ImageField(upload_to='hb', blank=True, null=True)

    def __str__(self):
        return f"Banner {self.id}"


class Timg(models.Model):
    pd = models.ImageField(upload_to='mhb', blank=True, null=True)
    hs = models.ImageField(upload_to='mhb', blank=True, null=True)
    tt = models.ImageField(upload_to='mhb', blank=True, null=True)
    ht = models.ImageField(upload_to='mhb', blank=True, null=True)

    def __str__(self):
        return f"Timg {self.id}"


class Bannerdestination(models.Model):
    Bimg = models.ImageField(upload_to='bd')

    def __str__(self):
        return f"Bannerdestination {self.id}"


class Destination(models.Model):
    category = models.CharField(max_length=50)
    dimg = models.ImageField(upload_to='destination')
    dimg1 = models.ImageField(upload_to='destination', blank=True, null=True)
    dimg2 = models.ImageField(upload_to='destination', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(default="")
    duration = models.CharField(max_length=50, default="--", blank=True)
    includes = models.TextField(default="", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.title


class Gallery(models.Model):
    CATEGORY_CHOICES = (
        ('hill', 'Hill Station'),
        ('beach', 'Beach'),
        ('temple', 'Temple'),
    )

    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='gallery/', null=True, blank=True)
    image1 = models.ImageField(upload_to='gallery/', null=True, blank=True)
    image2 = models.ImageField(upload_to='gallery/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='hill')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title or f"Gallery {self.id}"


class Cont(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    destination = models.CharField(max_length=200)
    duration = models.CharField(max_length=100, null=True, blank=True)
    vehicle_type = models.CharField(max_length=50, null=True, blank=True)
    price_per_head = models.DecimalField(max_digits=10, decimal_places=2)
    guests = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    upi_app = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=50, default="Pending")
    QR = models.ImageField(upload_to="payment_screenshots/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking #{self.booking.id}"