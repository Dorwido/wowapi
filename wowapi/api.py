from urllib2 import Request, urlopen, URLError,quote
import gzip
import StringIO
import json
from .exceptions import APIError,NotModified,NotFound
from .utilities import parse_http_datetime,http_datetime

regions = {
    'us' : {
        'domain':'us.battle.net',
         'locales' : [
             'en_US',
             'es_MX'
         ]
        },
    'eu' : {
        'domain':'eu.battle.net',
         'locales' : [
             'en_GB',
             'es_ES',
             'fr_FR',
             'ru_RU',
             'de_DE'
         ]
        },
    'kr' : {
        'domain':'kr.battle.net',
         'locales' : [
             'ko_KR'
         ]
        },
    'tw' : {
        'domain':'tw.battle.net',
         'locales' : [
             'zh_TW'
         ]
        },
    'cn' : {
        'domain':'battlenet.com.cn',
         'locales' : [
             'zh_CN'
         ]
        },
}

datatypes = {
    'character' : {
        'path':'character/%s/%s',
        'param':'fields'
    },
    'guild' : {
        'path':'guild/%s/%s',
        'param':'fields'
    },
    'realm' : {
        'path': 'realm/status',
        'param':'realms'
    },
    'auction' : {
        'path' : 'auction/data/%s'
    },
    'item' : {
        'path' : 'item/%d'
    },
    'arena_team' : {
        'path' : 'arena/%s/%s/%s'
    },
    'arena_ladder' : {
        'path' : 'pvp/arena/%s/%s',
        'param' : 'size'
    },
    'character_races':{
        'path' : 'data/character/races'
    },
    'character_classes':{
        'path' : 'data/character/classes'
    },
    'guild_rewards':{
        'path' : 'data/guild/rewards'
    },
    'guild_perks':{
        'path':'data/guild/perks'
    },
    'item_classes':{
        'path':'data/item/classes'
    }
}

class WoWApi():
    
    def _decode_response(self,response):
        
        if 'content-encoding' in response.info() and response.info()['content-encoding'] == 'gzip':
 	        response = gzip.GzipFile(fileobj=StringIO.StringIO(response.read()))
        try:
            data = json.loads(response.read())
        except json.JSONDecodeError:
            raise APIError('Non-JSON Response')
        return data


    def _do_request(self,request):
        try:
            response = urlopen(request)
        except URLError, e:
            if hasattr(e, 'reason'):
                raise APIError(e.reason)
            elif hasattr(e, 'code'):
                if e.code == 304:
                    raise NotModified
                elif e.code == 404:
                    raise NotFound
                else:
                    raise APIError(e.code)
        else:
            return response

    def _get_data(self,region,data,params=None,lastmodified=None,lang=None,datatype=None):
        if region not in regions:
            raise ValueError('Region not found')
        if lang and lang not in regions[region]['locales']:
            raise ValueError('Locales not valid for current region')
        if params:
            data += '?'+datatypes[datatype]['param']+'='+','.join(map(str, params))

        if lang and params:
            data+='&locale='+lang
        elif lang:
            data+='?locale='+lang

        url = 'http://'+regions[region]['domain']+'/api/wow/'+data
        header = {
            'Accept-Encoding': 'gzip'
        }
        if lastmodified:
            header['If-Modified-Since'] = http_datetime(lastmodified)

        request = Request(url, None, header)

        response = self._do_request(request)

        rlastmodified = None
        if 'Last-Modified' in response.info():
            rlastmodified = parse_http_datetime(response.info()['Last-Modified'])

        return {'lastmodified':(rlastmodified),'data':self._decode_response(response)}

    def get_item(self,region,itemid,lastmodified=None,lang=None):
        """
        Get infos about an item

        | ``Example:``
        ::

            get_item('eu',25)
        """
        if not int(itemid):
            raise ValueError('Itemid must be a integer')
        return self._get_data(region,datatypes['item']['path'] % (itemid),None,lastmodified,lang)


    def get_character(self,region,realm,character,params=None,lastmodified=None,lang=None):
        """
        Get infos about an character, params is a array taking optional fields to look up infos like achievements,talents etc

        | ``Example:``
        ::

            get_character('eu','Doomhammer','Thetotemlord',['talents'])
        """
        return self._get_data(region,datatypes['character']['path'] % (quote(realm),quote(character)),params,lastmodified,lang,'character')

    def get_guild(self,region,realm,guild,params=None,lastmodified=None,lang=None):
        """
        Get infos about an guild, params is a array taking optional fields to look up infos like achievements,members etc

        | ``Example:``
        ::

            get_guild('eu','Doomhammer','Dawn Of Osiris')
        """
        return self._get_data(region,datatypes['guild']['path'] % (quote(realm),quote(guild)),params,lastmodified,lang,'guild')

    def get_realm(self,region,params=None,lastmodified=None,lang=None):
        """
        Get infos about realm(s), params is a array taking optional which realms to look up otherwise returning all realms of an region

        | ``Example:``
        ::

            get_realm('eu',['Doomhammer'])
        """
        return self._get_data(region,datatypes['realm']['path'],params,lastmodified,lang,'realm')

    def get_auctions(self,region,realm,lastmodified=None,lang=None):
        """
        Returns all auctions of a realms

        | ``Example:``
        ::

            get_auction('eu','Doomhammer')
        """
        data = self._get_data(region,datatypes['auction']['path'] % (quote(realm)),None,lastmodified,lang)
        request = Request(data['data']['files'][0]['url'], None, {'Accept-Encoding': 'gzip'})
        return self._decode_response(self._do_request(request))

    def get_arena_team(self,region,realm,teamsize,teamname,lastmodified=None,lang=None):
        """
        Get infos about a arena team

        | ``Example:``
        ::

            get_arenea_team('eu','Doomhammer','2v2','We win')
        """
        return self._get_data(region,datatypes['arena_team']['path'] % (quote(realm),teamsize,quote(teamname)),None,lastmodified,lang)

    def get_arena_ladder(self,region,battlegroup,teamsize,howmany=None,lastmodified=None,lang=None):
        """
        Get the arena ladder of the specified battlegroup, optional with howmany you can define how many teams should be included

        | ``Example:``
        ::

            get_arena_ladder('eu','Blackout','5v5',100)
        """
        return self._get_data(region,datatypes['arena_ladder']['path'] % (quote(battlegroup),teamsize),[howmany],lastmodified,lang,'arena_ladder')

    def get_character_races(self,region,lastmodified=None,lang=None):
        """
        Get infos about all character races

        | ``Example:``
        ::

            get_character_races('us',None,'es_MX')
        """
        return self._get_data(region,datatypes['character_races']['path'],None,lastmodified,lang)

    def get_character_classes(self,region,lastmodified=None,lang=None):
        """
        Get infos about all character classes

        | ``Example:``
        ::

            get_character_class('eu')
        """
        return self._get_data(region,datatypes['character_classes']['path'],None,lastmodified,lang)

    def get_guild_rewards(self,region,lastmodified=None,lang=None):
        """
        Get infos about all guild rewards

        | ``Example:``
        ::

            get_guild_rewards('cn')
        """
        return self._get_data(region,datatypes['guild_rewards']['path'],None,lastmodified,lang)

    def get_guild_perks(self,region,lastmodified=None,lang=None):
        """
        Get infos about all guild perks

        | ``Example:``
        ::

            get_guild_perks('tw')
        """
        return self._get_data(region,datatypes['guild_perks']['path'],None,lastmodified,lang)

    def get_item_classes(self,region,lastmodified=None,lang=None):
        """
        Get infos about all item classes

        | ``Example:``
        ::

            get_item_classes('eu',None,'fr_FR')
        """
        return self._get_data(region,datatypes['item_classes']['path'],None,lastmodified,lang)

    
