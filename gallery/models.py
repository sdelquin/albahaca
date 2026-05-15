from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=255, blank=True)
    menu_item = models.OneToOneField('menu.Item', on_delete=models.CASCADE, blank=True, null=True)
    image_file = models.ImageField(upload_to='gallery/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(menu_item__isnull=False) | models.Q(title__isnull=False),
                name='title_or_menu_item_required',
            )
        ]

    @property
    def caption(self) -> str:
        return self.title or self.menu_item.name  # type: ignore

    def __str__(self):
        return self.caption
