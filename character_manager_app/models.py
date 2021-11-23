from django.db import models
from django.forms import ModelForm
from django import forms


# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=200)
    character_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    backstory = models.TextField(max_length=10000)

    def __str__(self):
        return self.name


class Stats(models.Model):
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    strength = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    charisma = models.IntegerField(default=10)
    constitution = models.IntegerField(default=10)
    intelligence = models.IntegerField(default=10)
    wisdom = models.IntegerField(default=10)
    proficiency = models.IntegerField(default=2)
    armor_class = models.IntegerField(default=10)


class StatsPoints(models.Model):
    name = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class Skills(models.Model):
    name = models.CharField(max_length=200, default='')
    attribute = models.ForeignKey(StatsPoints, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SkillsCharacter(models.Model):
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)
    proficiency = models.BooleanField(default=False)


class StatsCharacter(models.Model):
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    stats_points = models.ForeignKey(StatsPoints, on_delete=models.CASCADE)
    proficiency = models.BooleanField(default=False)

class Weapons(models.Model):
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='')
    number_of_dice  = models.SmallIntegerField(default=4)
    dice_type = models.SmallIntegerField(default=8)

    def __str__(self):
            return self.name

class Item(models.Model):
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='')
    weight = models.SmallIntegerField(default=1)
    description = models.TextField(default='')
    
    
#FORMS

class CreateCharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'backstory', 'character_class']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control text-white bg-dark', 'aria-describedby': 'name'}),
            'backstory': forms.Textarea(attrs={'class': 'form-control text-white bg-dark'})
        }


class AlterStatsForm(ModelForm):
    class Meta:
        model = Stats
        fields = ['wisdom', 'strength', 'dexterity', 'charisma', 'constitution', 'intelligence', 'char_id']
        widgets = {
            'wisdom': forms.TextInput(attrs={'class': 'form-control'}),
            'strength': forms.Textarea(attrs={'class': 'form-control'}),
            'charisma': forms.TextInput(attrs={'class': 'form-control'}),
            'constitution': forms.TextInput(attrs={'class': 'form-control'}),
            'dexterity': forms.TextInput(attrs={'class': 'form-control'}),
            'intelligence': forms.TextInput(attrs={'class': 'form-control'}),
        }
