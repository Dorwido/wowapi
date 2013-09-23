# -*- coding: utf-8 -*-
from wowapi.api import WoWApi

try:
    import unittest2 as unittest
except ImportError:
    import unittest as unittest

wowapi = WoWApi()
class Test_GetData(unittest.TestCase):

    def test_get_character(self):
        character = wowapi.get_character('eu','Doomhammer','Thetotemlord')
        self.assertEqual(character['data']['name'],'Thetotemlord')


    def test_get_item(self):
        item = wowapi.get_item('eu',25)
        self.assertEqual(item['data']['name'],'Worn Shortsword')

    def test_get_guild(self):
        guild = wowapi.get_guild('eu','Doomhammer','Dawn Of Osiris')
        self.assertEqual(guild['data']['name'],'Dawn Of Osiris')

    def test_get_realm(self):
        realm = wowapi.get_realm('eu')
        self.assertGreater(len(realm['data']['realms']),1)
       

    def test_get_auctions(self):
        auctions = wowapi.get_auctions('eu','Defias Brotherhood')
        self.assertEqual(len(auctions['data']),4)

    def test_get_arena_ladder_team(self):
        arena_ladder = wowapi.get_arena_ladder('eu','2v2')
        self.assertGreater(len(arena_ladder['data']['rows']),1)



    def test_get_character_races (self):
        character_races = wowapi.get_character_races('eu')
        self.assertGreater(len(character_races['data']['races']),1)

    def test_get_character_classes (self):
        character_classes = wowapi.get_character_classes('eu')
        self.assertGreater(len(character_classes['data']['classes']),1)

    def test_get_guild_rewards (self):
        guild_rewards = wowapi.get_guild_rewards('eu')
        self.assertGreater(len(guild_rewards['data']['rewards']),1)

    def test_get_guild_perks (self):
        guild_perks = wowapi.get_guild_perks('eu')
        self.assertGreater(len(guild_perks['data']['perks']),1)

    def test_get_item_classes (self):
        item_classes = wowapi.get_item_classes('eu')
        self.assertGreater(len(item_classes['data']['classes']),1)

    def test_get_quest(self):
        quest_info = wowapi.get_quest('eu',25)
        self.assertEqual(quest_info['data']['id'],25)

    def test_get_recipe (self):
        recipe_info = wowapi.get_recipe('us',33994)
        self.assertEqual(recipe_info['data']['id'],33994)

    def test_get_achievements_character(self):
        char_achievements = wowapi.get_achievements_character('eu')
        self.assertGreater(len(char_achievements['data']['achievements']),1)

    def test_get_achievements_guild(self):
        guild_achievements = wowapi.get_achievements_guild('eu')
        self.assertGreater(len(guild_achievements['data']['achievements']),1)

    def test_get_achievement (self):
        achievement_info = wowapi.get_achievement('us',2144)
        self.assertEqual(achievement_info['data']['id'],2144)

    def test_get_battlepet_ability (self):
        battlepet_ability_info = wowapi.get_battlepet_ability('us',640)
        self.assertEqual(battlepet_ability_info['data']['id'],640)

    def test_get_battlepet_species (self):
        battlepet_species_info = wowapi.get_battlepet_species('us',258)
        self.assertEqual(battlepet_species_info['data']['speciesId'],258)

    #def test_get_battlepet_stats (self):
    #    battlepet_stats_info = wowapi.get_battlepet_stats('us',258,['level=25'])
    #    self.assertEqual(battlepet_stats_info['data']['level'],25)

    def test_get_challenge_realm(self):
        challenge_realm_info = wowapi.get_challenge_realm('eu','Doomhammer')
        self.assertGreater(len(challenge_realm_info['data']['challenge']),1)

    def test_get_challenge_region(self):
        challenge_region_info = wowapi.get_challenge_region('eu')
        self.assertGreater(len(challenge_region_info['data']['challenge']),1)

    def test_get_spell (self):
        spell_info = wowapi.get_spell('us',8056)
        self.assertEqual(spell_info['data']['id'],8056)

    def test_get_battlegroups (self):
        battlegroups = wowapi.get_battlegroups('eu')
        self.assertGreater(len(battlegroups['data']['battlegroups']),1)


    def test_get_talents (self):
        talents = wowapi.get_talents('eu')
        self.assertGreater(len(talents['data']),1)


    def test_get_pet_types (self):
        pet_types = wowapi.get_pet_types('eu')
        self.assertGreater(len(pet_types['data']['petTypes']),1)