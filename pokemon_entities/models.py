from django.db import models  # noqa F401
from django.utils import timezone
from django.utils.timezone import localtime


class Pokemon(models.Model):
    """Покемон"""
    title = models.CharField(max_length=200, verbose_name="название")
    title_en = models.CharField(max_length=200, verbose_name="английское название", null=True, blank=True)
    title_jp = models.CharField(max_length=200, verbose_name="японское название", null=True, blank=True)
    image = models.ImageField(upload_to='images', verbose_name="фото", null=True, blank=True)
    description = models.TextField(default="", verbose_name="описание", blank=True)
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name="предок",
        related_name="next_evolution",
        null=True,
        blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Объект покемона"""
    latitude = models.FloatField(verbose_name="широта")
    longitude = models.FloatField(verbose_name="долгота")
    pokemon = models.ForeignKey(Pokemon, verbose_name="покемон", on_delete=models.CASCADE)
    appeared_at = models.DateTimeField(verbose_name="время_появления")
    disappeared_at = models.DateTimeField(verbose_name="время_исчезновения")
    level = models.IntegerField(default=1, verbose_name="уровень")
    health = models.IntegerField(default=1, verbose_name="здоровье")
    strength = models.IntegerField(default=1, verbose_name="сила")
    defence = models.IntegerField(default=1, verbose_name="защита")
    stamina = models.IntegerField(default=1, verbose_name="выносливость")

    def __str__(self):
        return self.pokemon.title

    def is_active(self):
        now = localtime(timezone.now())
        if not localtime(self.appeared_at) > now and \
           not localtime(self.disappeared_at) < now:
            return True
        return False