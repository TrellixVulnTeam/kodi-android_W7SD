"""
    Plugin for ResolveUrl
    Copyright (C) 2019 gujal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import re
from lib import helpers
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError

class ClipWatchingResolver(ResolveUrl):
    name = "clipwatching"
    domains = ['clipwatching.com']
    pattern = r'(?://|\.)(clipwatching\.com)/(?:embed-)?(\w+)'

    def __init__(self):
        self.net = common.Net()
        
    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.RAND_UA}
        html = self.net.http_GET(web_url, headers=headers).content
        
        html += helpers.get_packed_data(html)
        sources = helpers.scrape_sources(html)
        if sources:
            return helpers.pick_source(sources) + helpers.append_headers(headers)
                
        raise ResolverError("Video not found")
        
    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/embed-{media_id}.html')