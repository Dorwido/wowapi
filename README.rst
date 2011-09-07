About
======
I am using a python framework for my website and due the current python modules for the WoW Api are not updated very often,
still missing features and I prefer to get raw data, I wrote my own little module.

| It supports: gzip compression and also If-Modified-Since header

*It dont have authentication at the moment, this is because I don't have a API Key*

Basic usage
===========
::
	
	from wowapi.api import WoWApi
	wowapi = WoWApi()
	auctions = wowapi.get_auctions('eu','Doomhammer')

``Input values:`` 

| *This only include some of the values the other should be pretty self explain*

| **region** is the 2 letter code of the region for ex: eu
| **params** the function which got thise you can add extra fields for ex if you wanna retrieve the achievements,talents for a character add ['talents','achievements'], this use the same names as in the blizzard documentation
| **lastmodified** (optional) must be a datetime variable and is optional, if set the date will be added as *If-Modified-Since* header, if nothing changed since that date a NotModified exception will be raised
| **lang** (optional) can be a any locale valid for the choosen region and uses the same format as documented in the blizzard documentation for ex if you want french for the eu region add fr_FR 
	
	
``Return Values:``

| It will always returns 2 items:

| **lastmodified** - which is a datetime value or none (based on if the last modified header is set or not)
| **data** - which will be the raw data

``Example:``
::
	
	>>> from wowapi.api import WoWApi
	>>> wowapi = WoWApi()
	>>> character = wowapi.get_character('eu','Doomhammer','Thetotemlord')
	>>> print character['lastmodified']
	2011-09-07 09:20:12
	>>> print character['data']['class']
	7
	
Advanced usage
==============

Lets say you want for example all character classes in all available languages you could do something like this:

::

	from wowapi.api import WoWApi,regions
	wowapi = WoWApi()
	for region in regions:
        for lang in regions[region]['locales']:
            char_classes = wowapi.get_character_classes(region,None,lang)
			#Do something with it
	
	
Api functions
=============

.. py:module:: wowapi.api


.. py:class:: WoWApi
   :module: wowapi.api


   
   .. py:method:: WoWApi.get_arena_ladder(region, battlegroup, teamsize, howmany=None, lastmodified=None, lang=None)
      :module: wowapi.api
   
      Get the arena ladder of the specified battlegroup, optional with howmany you can define how many teams should be included
      
      | ``Example:``
      ::
      
          get_arena_ladder('eu','Blackout','5v5',100)
      
   
   .. py:method:: WoWApi.get_arena_team(region, realm, teamsize, teamname, lastmodified=None, lang=None)
      :module: wowapi.api
   
      Get infos about a arena team
      
      | ``Example:``
      ::
      
          get_arenea_team('eu','Doomhammer','2v2','We win')
      
   
   .. py:method:: WoWApi.get_auctions(region, realm, lastmodified=None, lang=None)
      :module: wowapi.api
   
      Returns all auctions of a realms
      
      | ``Example:``
      ::
      
          get_auction('eu','Doomhammer')
      
   
   .. py:method:: WoWApi.get_character(region, realm, character, params=None, lastmodified=None, lang=None)
      :module: wowapi.api
   
      Get infos about an character, params is a array taking optional fields to look up infos like achievements,talents etc
      
      | ``Example:``
      ::
      
          get_character('eu','Doomhammer','Thetotemlord',['talents'])
      
   
   .. py:method:: WoWApi.get_character_classes(region, lastmodified=None, lang=None)
      :module: wowapi.api
   
      Get infos about all character classes
      
      | ``Example:``
      ::
      
          get_character_class('eu')
      
   
   .. py:method:: WoWApi.get_character_races(region, lastmodified=None, lang=None)
      :module: wowapi.api
   
      Get infos about all character races
      
      | ``Example:``
      ::
      
          get_character_races('us',None,'es_MX')
      
   
   .. py:method:: WoWApi.get_guild(region, realm, guild, params=None, lastmodified=None, lang=None)
      :module: wowapi.api
   
      Get infos about an guild, params is a array taking optional fields to look up infos like achievements,members etc
      
      | ``Example:``
      ::
      
          get_guild('eu','Doomhammer','Dawn Of Osiris')
      
   
   .. py:method:: WoWApi.get_guild_perks(region, lastmodified=None, lang=None)
      :module: wowapi.api
   
      Get infos about all guild perks
      
      | ``Example:``
      ::
      
          get_guild_perks('tw')
      
   
   .. py:method:: WoWApi.get_guild_rewards(region, lastmodified=None, lang=None)
      :module: wowapi.api
   
      Get infos about all guild rewards
      
      | ``Example:``
      ::
      
          get_guild_rewards('cn')
      
   
   .. py:method:: WoWApi.get_item(region, itemid, lastmodified=None, lang=None)
      :module: wowapi.api
   
      Get infos about an item
      
      | ``Example:``
      ::
      
          get_item('eu',25)
      
   
   .. py:method:: WoWApi.get_item_classes(region, lastmodified=None, lang=None)
      :module: wowapi.api
   
      Get infos about all item classes
      
      | ``Example:``
      ::
      
          get_item_classes('eu',None,'fr_FR')
      
   
   .. py:method:: WoWApi.get_realm(region, params=None, lastmodified=None, lang=None)
      :module: wowapi.api
   
      Get infos about realm(s), params is a array taking optional which realms to look up otherwise returning all realms of an region
      
      | ``Example:``
      ::
      
          get_realm('eu',['Doomhammer'])
      

.. py:module:: wowapi.exceptions


.. py:exception:: APIError
   :module: wowapi.exceptions

   Bases: :class:`exceptions.Exception`

   This is raised on all other http errors only with the error code, this will change in the future and
   include the error message
   

.. py:exception:: NotFound
   :module: wowapi.exceptions

   Bases: :class:`wowapi.exceptions.APIError`

   This is raised on 404 Errors
   

.. py:exception:: NotModified
   :module: wowapi.exceptions

   Bases: :class:`wowapi.exceptions.APIError`

   This is raised when using the last modified option and nothing changed, since last request
   
   
To Do
=====

- add authorization
- show the error message for 5xx errors