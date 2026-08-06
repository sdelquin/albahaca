from django.db import models


class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class Item(models.Model):
    name = models.CharField(max_length=256, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Precio',
    )
    active = models.BooleanField(default=True, verbose_name='Activo')
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Categoría',
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')

    class Meta:
        ordering = ['order']
        verbose_name = 'Item del menú'
        verbose_name_plural = 'Items del menú'

    def __str__(self):
        return self.name

    @property
    def price_display(self) -> str:
        return f'{self.price:.2f}€' if self.price is not None else '-'

    # Managers
    objects = ActiveManager()


class SubItem(models.Model):
    details = models.CharField(max_length=256, verbose_name='Detalles')
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Precio',
    )
    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        related_name='subitems',
        verbose_name='Item del menú',
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')

    class Meta:
        verbose_name = 'Subitem del menú'
        verbose_name_plural = 'Subitems del menú'
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
    name = models.CharField(max_length=256, verbose_name='Nombre')
    slug = models.SlugField(max_length=256, unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Descripción')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')
    cover = models.ImageField(
        upload_to='categories/covers/', blank=True, null=True, verbose_name='Imagen de portada'
    )

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['order']

    def __str__(self):
        return self.name
