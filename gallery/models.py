from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name='Título')
    menu_item = models.OneToOneField(
        'menu.Item', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Ítem del menú'
    )
    image_file = models.ImageField(upload_to='gallery/images/', verbose_name='Imagen')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Subido el')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')

    class Meta:
        ordering = ['order']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(menu_item__isnull=False) | models.Q(title__isnull=False),
                name='title_or_menu_item_required',
            )
        ]
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imágenes'

    @property
    def caption(self) -> str:
        return self.title or self.menu_item.name  # type: ignore

    def __str__(self):
        return self.caption
