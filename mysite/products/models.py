from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image_url = models.URLField(blank=True, null=True)
    current_price = models.IntegerField()
    previous_price = models.IntegerField(default=0, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Cek apakah ini update (bukan create baru)
        if self.pk:
            try:
                old_entry = Product.objects.get(pk=self.pk)
                # Jika harga berubah
                if old_entry.current_price != self.current_price:
                    self.previous_price = old_entry.current_price
                    # Cek apakah sudah ada history hari ini
                    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
                    today_end = today_start + timezone.timedelta(days=1)
                    existing_history = PriceHistory.objects.filter(
                        product=self,
                        recorded_at__gte=today_start,
                        recorded_at__lt=today_end
                    ).first()
                    
                    if existing_history:
                        # Update harga history hari ini
                        existing_history.price = self.current_price
                        existing_history.save()
                    else:
                        # Buat history baru untuk hari ini
                        PriceHistory.objects.create(
                            product=self,
                            price=self.current_price,
                            recorded_at=timezone.now()
                        )
            except Product.DoesNotExist:
                pass  # Produk baru
        else:
            # Jika produk baru dibuat, previous price samakan saja atau 0
            self.previous_price = self.current_price

        super().save(*args, **kwargs)

        # Untuk produk baru, buat history awal
        if not PriceHistory.objects.filter(product=self).exists():
            PriceHistory.objects.create(
                product=self,
                price=self.current_price,
                recorded_at=timezone.now()
            )


class PriceHistory(models.Model):
    product = models.ForeignKey(Product, related_name='history', on_delete=models.CASCADE)
    price = models.IntegerField()
    recorded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.name} - {self.price} ({self.recorded_at.date()})"
