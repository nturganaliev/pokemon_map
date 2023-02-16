from django.db import models  # noqa F401


class Pokemon(models.Model):
    """Покемон"""
    title = models.CharField(max_length=200, verbose_name="название")
    title_en = models.CharField(
        max_length=200,
        verbose_name="английское название",
        null=True,
        blank=True
    )
    title_jp = models.CharField(
        max_length=200,
        verbose_name="японское название",
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='images',
        verbose_name="фото",
        null=True,
        blank=True
    )
    description = models.TextField(verbose_name="описание", blank=True)
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name="предок",
        related_name="next_evolutions",
        null=True,
        blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Объект покемона"""
    latitude = models.FloatField(verbose_name="широта")
    longitude = models.FloatField(verbose_name="долгота")
    pokemon = models.ForeignKey(
        Pokemon,
        related_name="entities",
        verbose_name="покемон",
        on_delete=models.CASCADE)
    appeared_at = models.DateTimeField(verbose_name="время_появления")
    disappeared_at = models.DateTimeField(verbose_name="время_исчезновения")
    level = models.IntegerField(
        verbose_name="уровень",
        blank=True,
        null=True
    )
    health = models.IntegerField(
        verbose_name="здоровье",
        blank=True,
        null=True
    )
    strength = models.IntegerField(
        verbose_name="сила",
        blank=True,
        null=True
    )
    defence = models.IntegerField(
        verbose_name="защита",
        blank=True,
        null=True
    )
    stamina = models.IntegerField(
        verbose_name="выносливость",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.pokemon.title
