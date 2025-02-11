# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @Daddy_Blamo wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: Mr.Blamo

import re
import urllib
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser



class source:
    def __init__(self):
        self.priority = 1
        self.language = ['es']
        self.domains = ['peliculasdk.com']
        self.base_link = 'http://peliculasdk.com'
        self.search_link = '/index.php?s=%s&x=0&y=0'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases), year)
            return url
        except:
            return

    def __search(self, titles, year):
        try:

            query = self.search_link % (urllib.quote_plus(cleantitle.query(titles[0])+' '+year))

            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i][0]

            r = client.request(query)

            r = client.parseDOM(r, 'div', attrs={'class': 'karatula'})

            for i in r:
                title = client.parseDOM(i, 'a', ret='title')[0]
                y = re.findall('(\d{4})',title)[0]
                title = cleantitle.get_simple(title)

                if t in title and y == year :
                    x = dom_parser.parse_dom(i, 'a', req='href')
                    return source_utils.strip_domain(x[0][0]['href'])

            return
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            query = urlparse.urljoin(self.base_link, url)

            r = client.request(query)

            q = client.parseDOM(r, 'ul', attrs={'class': 'tabs'})[0]

            matches = re.compile('re">\d+.+?class="(\w{2})".+?c">([^>]+)<', re.DOTALL).findall(q)

            urls_id = re.compile('<div id="tab\d+"\s*class="tab_content"><script>(\w+)\("([^"]+)"\)</script>',re.DOTALL).findall(r)

            for i in range(0,len(urls_id)):

                lang, info = self.get_lang_by_type(matches[i][0])

                qual = matches[i][1]
                qual = 'HD' if 'HD' or 'BR' in qual else 'SD'

                url, host = self.url_function(urls_id[i][1], urls_id[i][0])
                if 'goo' in url:
                    data = client.request(url)
                    url = re.findall('var\s*videokeyorig\s*=\s*"(.+?)"', data, re.DOTALL)[0]
                    url, host = 'http://hqq.tv/player/embed_player.php?vid=%s'%(url), 'netu.tv'

                sources.append({'source': host, 'quality': qual, 'language': lang, 'url': url, 'info': info, 'direct': False,'debridonly': False})

            return sources
        except:
            return sources

    def get_lang_by_type(self, lang_type):
        if lang_type == 'la':
            return 'es', 'LAT'
        elif lang_type == 'es':
            return 'es', 'CAST'
        elif lang_type == 'su':
            return 'en', 'SUB'
        return 'es', None

    def url_function(self, url_id,server):
        url = ''
        host = ''
        if server == 'netu':
            host = 'netu.tv'
            url = 'http://hqq.tv/player/embed_player.php?vid=%s'%(url_id)
        elif server == "netv":
            host = 'goo.gl'
            url = 'http://goo.gl/%s'%(url_id)
        elif server == "mango":
            host = 'streamango'
            url = 'https://streamango.com/embed/%s'%(url_id)
        elif server == "powvideo":
            host = 'powvideo'
            url = 'http://powvideo.net/embed-%s'%(url_id)
        elif server == "gamo":
            host = 'gamovideo'
            url = 'http://gamovideo.com/embed-%s'%(url_id)
        elif server == "play":
            host = 'streamplay'
            url = 'http://streamplay.to/embed-%s'%(url_id)
        elif server == "youtube":
            host = 'youtube'
            url = 'https://www.youtube.com/embed/%s'%(url_id)
        elif server == "okru":
            host = 'okru'
            url = 'http://ok.ru/videoembed/%s'%(url_id)
        elif server == "open":
            host = 'openload'
            url = 'https://openload.co/embed/%s'%(url_id)
        elif server == "down":
            host = 'uploaded'
            url = 'http://uploaded.net/file/%s'%(url_id)

        return url,host

    def resolve(self, url):
        return url
