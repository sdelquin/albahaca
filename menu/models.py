from django.db import models


class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class Item(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='items')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    @property
    def price_display(self) -> str:
        return f'{self.price:.2f}€' if self.price is not None else '-'

    # Managers
    objects = ActiveManager()


class SubItem(models.Model):
    details = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='subitems')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'SubItem'
        ordering = ['order']

    def __str__(self):
        return self.details

    @property
    def name(self) -> str:
        return f'{self.item.name} ({self.details})'

    @property
    def price_display(self) -> str:
        return f'{self.price:.2f}€' if self.price is not None else '-'


class Category(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    cover = models.ImageField(upload_to='categories/covers/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order']

    def __str__(self):
        return self.name
