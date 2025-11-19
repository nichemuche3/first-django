from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления"""
    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"

class Advertisement(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN,
        verbose_name="Статус"
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def clean(self):
        """Валидация - не больше 10 открытых объявлений у пользователя"""
        if (self.status == AdvertisementStatusChoices.OPEN and 
            self.creator and 
            not self.pk): 
            
            open_ads_count = Advertisement.objects.filter(
                creator=self.creator,
                status=AdvertisementStatusChoices.OPEN
            ).count()
            
            if open_ads_count >= 10:
                raise ValidationError("Нельзя иметь больше 10 открытых объявлений")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'advertisements'
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

class FavoriteAdvertisement(models.Model):
    """Избранные объявления (дополнительное задание)"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='favorites'
    )
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        verbose_name="Объявление",
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        db_table = 'favorite_advertisements'
        verbose_name = 'Избранное объявление'
        verbose_name_plural = 'Избранные объявления'
        unique_together = ['user', 'advertisement'] 