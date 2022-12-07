# -*- coding: utf-8 -*-

# Copyright © 2022 B Tasker.
#
# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from blinker import signal
from lxml import html

from nikola.utils import get_logger, STDERR_HANDLER
from nikola.plugin_categories import SignalHandler


class WebMentions(SignalHandler):
    name = "webmentions"
    
    # Doc https://www.getnikola.com/extending.html says
    #
    # The easiest way to do this is to reimplement set_site() and just connect to whatever signals you want there.
    # 
    # so taking the easy route
    def set_site(self, site):
        self.site = site
        self.logger = get_logger(self.name, STDERR_HANDLER)

        # Bind to the signal
        ready = signal('deployed')
        
        # Trigger analyse_posts when the signal's received
        ready.connect(self.analyse_posts)
        
        
    def analyse_posts(self, event):
        '''
            We should get an event dict
            
            Within that, there will be deployed" which gives details of all posts that have been deployed
            
            Format of that object is here: https://nikola.readthedocs.io/en/latest/nikola.html#module-nikola.post
            
            Note: Nikola won't trigger this hook for posts with a Date (or Updated) that's before the last recorded deploy. So we won't end up re-sending webmentions if we make changes to an existing post.
            
        '''
        
        for post in event["deployed"]:      
            self.logger.error('Received {0}'.format(post))
            
            title = post.title()
            
            if post.is_draft or post.post_status != "published":
                # Don't send for drafts
                self.logger.info('Skipping Draft Post {0} with status {1}'.format(title, post.post_status))
                continue
            
            link = post.permalink(absolute=True)
            text = post.text()
            self.logger.info('Processing {0}'.format(link))
        
            # Extract links from the rendered page
            links = self.extract_links(text)
            
            
        
        
    def extract_links(self, post_text):
        ''' Receive a HTML post, iterate through it looking for links out and extract the relevant URLs
        
            return: list
        '''
        tree = html.fromstring(post_text)
        
        # Map out element types and the attributes we're looking for
        # keep it simple to begin with
        #
        attribs = {
            "href" : ["a"]
            }
        
        urls = []
    
        # Iterate over each attribute type
        for attrib in attribs:
            for element in attribs[attrib]:
                xpath = "//{0}[@{1}]".format(element, attrib)
                for match in tree.xpath(xpath):
                    self.logger.info('Found {0}'.format(match.get('href')))
                    # Remove URL fragments
                    u = match.get('href').split("#")[0]
                    urls.append(u)
        
        # Make the list unique
        urls = list(set(urls))
        return urls
        


