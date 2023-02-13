from django.db import models  # noqa F401
from django.utils import timezone
from django.utils.timezone import localtime


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=1)
    strength = models.IntegerField(default=1)
    defence = models.IntegerField(default=1)
    stamina = models.IntegerField(default=1)

    def __str__(self):
        return self.pokemon.title

    def is_active(self):
        now = localtime(timezone.now())
        if not localtime(self.appeared_at) > now and \
           not localtime(self.disappeared_at) < now:
            return True
        return False