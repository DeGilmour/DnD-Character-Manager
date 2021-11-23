from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import *
import random
import json
from django.shortcuts import redirect


def index(req):
    """Opens up the initial page"""
    return render(req, 'index.html', context={'title': "Character Manager"})


def create_character(req):
    form = CreateCharacterForm
    classes = Class.objects.all()
    if req.method == 'POST':
        cleaned_form = form(req.POST)
        if cleaned_form.is_valid():
            try:
                cleaned_form.save()
                return redirect('/character/{}'.format(cleaned_form.instance.pk))
            except Exception as e:
                raise Exception("Form is not valid!".format(
                    e or cleaned_form.errors))
        else:
            raise Exception("form is not valid: {}".format(form.errors))
    return render(req, 'create_character.html', context={'form': form, 'classes': classes, 'title': "Create Character"})


def load_characters(req):
    characters = Character.objects.all()
    return render(req, 'saved_characters.html', context={"characters": characters, 'title': 'Saved Characters'})


def character_self(req, c_id: int):
    character = Character.objects.get(pk=c_id)
    req.session['char_id'] = c_id
    saved = Stats.objects.filter(char_id=character).first()
    if not saved:
        stats = Stats(char_id=character)
        stats.save()
        saved = Stats.objects.filter(char_id=character).first()

    bonus = {"charisma": calculate_bonus(stat=saved.charisma) if saved else 0,
             "constitution": calculate_bonus(stat=saved.constitution) if saved else 0,
             "strength": calculate_bonus(stat=saved.strength) if saved else 0,
             "dexterity": calculate_bonus(stat=saved.dexterity) if saved else 0,
             "wisdom": calculate_bonus(stat=saved.wisdom) if saved else 0,
             "intelligence": calculate_bonus(stat=saved.intelligence) if saved else 0}
    proficiencies_attr = StatsCharacter.objects.filter(
        char_id=character, proficiency=True)
    profs = {}
    # Creating a dict with the proficiencies names
    for i in proficiencies_attr:
        profs[i.stats_points.name.lower()] = i.proficiency

    skills = calculate_skill_bonus(bonus=bonus, character=character)
    for key, value in bonus.items():
        if value > 0:
            bonus[key] = "+{}".format(value)

    weapons = Weapons.objects.filter(char_id=character).all()
    items = Item.objects.filter(char_id=character).all()
    return render(req, 'character.html',
                  context={"character": character, 'title': character.name.capitalize(), 'char_id': c_id,
                           'saved': saved, 'bonus': bonus, 'skills': skills, 'proficiencies_attr': profs,
                           'weapons': weapons, 'items': items})


def edit_character(req):
    """Edits the character stats/attributes"""
    if req.method == 'POST':
        character = Character.objects.get(pk=req.POST['char_id'])
        old_stat = Stats.objects.filter(char_id=character).first()
        if not old_stat:
            new_stat = Stats(char_id=character, charisma=req.POST['charisma'], intelligence=req.POST['intelligence'],
                             constitution=req.POST['constitution'],
                             strength=req.POST['strength'],
                             dexterity=req.POST['dexterity'],
                             wisdom=req.POST['wisdom'],
                             armor_class=req.POST['armor_class'],
                             proficiency=req.POST['proficiency'])
            new_stat.save()
        else:
            old_stat.charisma = req.POST['charisma']
            old_stat.intelligence = req.POST['intelligence']
            old_stat.constitution = req.POST['constitution']
            old_stat.strength = req.POST['strength']
            old_stat.dexterity = req.POST['dexterity']
            old_stat.wisdom = req.POST['wisdom']
            old_stat.armor_class = req.POST['armor_class']
            old_stat.proficiency = req.POST['proficiency']
            old_stat.save()
        return redirect('/character/{}'.format(req.POST['char_id']))


def calculate_bonus(stat, standard=10) -> int:
    diff = stat - standard
    bonus = diff / 2
    return int(bonus)


def calculate_skill_bonus(bonus, character) -> list:
    """Calculates the attribute bonus + skill bonus + proficiency"""
    skills = Skills.objects.all()
    saved = Stats.objects.filter(char_id=character).first()
    list_skills = []
    for skill in skills:
        skills_prof = SkillsCharacter.objects.filter(
            char_id=character, skill=skill).first()
        if skills_prof:
            prof = skills_prof.proficiency
        else:
            prof = False
        prof_bonus = saved.proficiency if skills_prof and skills_prof.proficiency else 0
        new_bonus = bonus[skill.attribute.name.lower()] + prof_bonus
        if new_bonus > 0:
            new_bonus = '+ {}'.format(str(new_bonus))

        data = {"skill": skill, "bonus": new_bonus,
                "proficiency": prof}
        list_skills.append(data)
    return list_skills


def check(req):
    """This rolls a attribute check and Rows a Saving throw and checks if its proficient"""
    roll = random.randint(1, 20)
    data = responde_to_dict(req)
    character = Stats.objects.filter(char_id=data.get("id")).first()
    bonus = ''
    stat_prof = StatsCharacter.objects.filter(
        char_id=character.char_id, proficiency=True)
    profs = {}
    for i in stat_prof:
        profs[i.stats_points.name.lower()] = i.proficiency

    if data.get('value') == 1:
        bonus = calculate_bonus(character.charisma)
        bonus += character.proficiency if data.get(
            "saving") and profs.get('charisma') else 0
    elif data.get("value") == 2:
        bonus = calculate_bonus(character.intelligence)
        bonus += character.proficiency if data.get(
            "saving") and profs.get('intelligence') else 0
    elif data.get("value") == 3:
        bonus = calculate_bonus(character.constitution)
        bonus += character.proficiency if data.get(
            "saving") and profs.get('constitution') else 0
    elif data.get("value") == 4:
        bonus = calculate_bonus(character.dexterity)
        bonus += character.proficiency if data.get(
            "saving") and profs.get('dexterity') else 0
    elif data.get("value") == 5:
        bonus = calculate_bonus(character.wisdom)
        bonus += character.proficiency if data.get(
            "saving") and profs.get('wisdom') else 0
    elif data.get("value") == 6:
        bonus = calculate_bonus(character.strength)
        bonus += character.proficiency if data.get(
            "saving") and profs.get('strength') else 0

    roll += bonus
    result = {"result": roll}
    return JsonResponse(result)


def skill_check(req) -> JsonResponse:
    """Rolls a skill check"""
    roll = random.randint(1, 20)
    data = responde_to_dict(req)
    character = Stats.objects.filter(char_id=data.get("id")).first()
    skill = Skills.objects.get(pk=data.get("value"))
    skill_prof = SkillsCharacter.objects.filter(
        skill=skill, char_id=character.char_id).first()
    bonus = character.__getattribute__(skill.attribute.name.lower())
    bonus = calculate_bonus(bonus)
    if skill_prof:
        bonus += character.proficiency
    roll += bonus

    result = {"result": roll}
    return JsonResponse(result)


def save_proficiency(req):
    """Saves a Proficiency"""
    data = responde_to_dict(req)
    char_id = data.get("id")
    character = Character.objects.filter(pk=char_id).first()
    try:
        # Saves skill proficiencies
        if data.get('skill'):
            skill = Skills.objects.get(pk=data.get("skill"))
            old_prof = SkillsCharacter.objects.filter(
                char_id=character, skill=skill).first()
            if not old_prof:
                new_prof = SkillsCharacter(
                    char_id=character, proficiency=data.get("proficiency"), skill=skill)
                new_prof.save()
            else:
                old_prof.proficiency = data.get("proficiency")
                old_prof.save()
        else:
            # Saves stat proficiencies(For saves)
            stat = StatsPoints.objects.get(pk=data.get('attribute'))
            old_prof = StatsCharacter.objects.filter(
                char_id=character, stats_points=stat).first()
            if not old_prof:
                new_prof = StatsCharacter(char_id=character, proficiency=data.get(
                    'proficiency'), stats_points=stat)
                new_prof.save()
            else:
                old_prof.proficiency = data.get("proficiency")
                old_prof.save()
        return JsonResponse({"reload": 1})
    except Exception as e:
        raise Exception(e)


def type_bonus(bonus, roll):
    if '+' in bonus:
        bonus = bonus.strip('+').strip(' ')
        roll += int(bonus)
    else:
        bonus = bonus.strip('-').strip(' ')
        roll -= int(bonus)
    return roll


def save_weapon(req):
    form_data = responde_to_dict(req)
    character = Character.objects.filter(pk=req.session.get('char_id')).first()
    splited_dice = form_data.get('weapon_damage').split('d')
    number_of_dice = int(splited_dice[0])
    dice_type = int(splited_dice[1])
    new_weapon = Weapons(char_id=character, name=form_data.get(
        'weapon_name'), number_of_dice=number_of_dice, dice_type=dice_type)
    new_weapon.save()
    return JsonResponse({"reload": 1})


def responde_to_dict(req):
    """Converts and decodes the requisition"""
    form_data = json.loads(req.body.decode())
    form_data = form_data['data']
    return form_data


def render_macro(macro, data):
    """Returns an html to be rendered"""
    t = loader.get_template(macro)
    return t.render(context=data)


def get_html_weapon(req):
    """Render a <tr> tag filled with the weapon's required attributes"""
    req_data = responde_to_dict(req)
    data = {"data": render_macro(macro='macro.html', data={
                                 'add_weapon': True, 'weapon': req_data.get('number_row')})}
    return JsonResponse(data)


def get_html_item(req):
    """Render a <tr> tag filled with the item's required attributes"""
    req_data = responde_to_dict(req)
    data = {"data": render_macro(macro='macro.html', data={
                                 'add_item': True, 'item_row': req_data.get('number_row')})}
    return JsonResponse(data)


def roll_weapon_damage(req):
    """Rolls the weapon dmg"""
    form_data = responde_to_dict(req)
    weapon = Weapons.objects.get(pk=form_data.get("weapon_id"))
    return JsonResponse(diceRoller(dice_type=weapon.dice_type, number_of_dice=weapon.number_of_dice))


def save_item(req):
    form_data = responde_to_dict(req)
    character = Character.objects.filter(pk=req.session.get('char_id')).first()
    new_item = Item(char_id=character, name=form_data.get('item_name'), weight=form_data.get('item_weight'), description=form_data.get('item_description'))
    new_item.save()
    return JsonResponse({"reload": 1})


def diceRoller(dice_type: int, number_of_dice: int) -> dict:
    """Roll dices"""
    result = []
    for i in range(0, number_of_dice):
        roll = random.randint(1, dice_type)
        result.append(roll)
    list_string = map(str, result)
    data = {'result': sum(result), 'rolled': '+'.join(list_string)}
    return data
