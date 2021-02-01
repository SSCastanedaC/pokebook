from django.db import models

# Create your models here.

class Pokemon(models.Model):
    pokeapi_id = models.IntegerField(primary_key = True)
    #General Information
    name = models.CharField(max_length = 100)
    height  = models.IntegerField()
    weight  = models.IntegerField()
    #Base Stats
    hp = models.IntegerField()
    attack  = models.IntegerField()
    special_attack  = models.IntegerField()
    deffense  = models.IntegerField()
    special_deffense  = models.IntegerField()
    speed  = models.IntegerField()
    #Image
    url_image = models.CharField(max_length = 255)

class Evolution(models.Model):
    pokeapi_id = models.IntegerField()
    evolves_from = models.ForeignKey(Pokemon, on_delete=models.PROTECT, related_name='evolves_from')
    evolves_to = models.ForeignKey(Pokemon, on_delete=models.PROTECT, related_name='evolves_to')
    class Meta:
        unique_together = ('evolves_from', 'evolves_to')