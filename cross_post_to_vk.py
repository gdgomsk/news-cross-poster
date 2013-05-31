#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Alex Korovyansky (ak@gdgomsk.org)"
__copyright__ = "Copyright 2013, GDG Omsk"
__email__ = "org.team@gdgomsk.org"
__license__ = 'Apache License, Version 2.0'
__version__ = '0.1a'

import time
import webapp2
import vkontakte
from apiclient.discovery import build

import constants
import constants_secret
from model import CrossPostedToVK

plus = build('plus', 'v1', developerKey=constants_secret.GOOGLE_PLUS_API_KEY)
vk = vkontakte.API(token=constants_secret.VKONTAKTE_EKATERINA_LUBIMOVA_TOKEN)

class MainHandler(webapp2.RequestHandler):
    """ Обработчик для кросс-постинга постов из g+ в вконтакте. 
        Учитываются только последние 20 постов. Каждый пост перепостчивается только один раз, независимо от кол-ва вызовов обработчика"""

    def get(self):
        response = self.fetch_last_posts()

        self.cross_post_to_vk(response)

        self.response.write("200 OK")

    def fetch_last_posts(self):
        request = plus.activities().list(userId=constants.GOOGLE_PLUS_GDG_OMSK_ID,
            collection='public',
            maxResults=constants.GOOGLE_PLUS_MAX_RESULTS)
        response = request.execute()
        response['items'] = response.get('items')
        return response

    def cross_post_to_vk(self, response):

        q = CrossPostedToVK.all()
        cross_posted_info = q.get()
        if cross_posted_info == None:
            cross_posted_info = CrossPostedToVK()
            cross_posted_info.cross_posted_gplus_ids = []

        response_ids = list(item.get('id') for item in response.get('items'))
        new_ids = self.find_positive_difference(response_ids, cross_posted_info.cross_posted_gplus_ids)

        if len(new_ids) == 0:
            pass #self.cross_post_no_changes()
        else:
            for item in reversed(response.get('items')):
               item_id = item.get('id')
               if item_id in new_ids:
                   self.cross_post_and_mark(item, cross_posted_info)
                   time.sleep(10)



    def cross_post_and_mark(self, item, cross_posted_info):
        message = item.get('title')
        url = item.get('url')
        vk.wall.post(owner_id=constants.VKONTAKTE_GDG_OMSK_NEWS_GROUP_ID, message=message, attachments=url,
           from_group=1, signed=0)
        cross_posted_info.cross_posted_gplus_ids.append(item.get('id'))
        cross_posted_info.put()

    def cross_post_no_changes(self):
        vk.wall.post(owner_id=constants.VKONTAKTE_GDG_OMSK_NEWS_GROUP_ID, message="Пока тихо... Ждем новостей!",
           from_group=1, signed=0)
        

    def find_positive_difference(self, list1, list2):
        s = set(list2)
        return [x for x in list1 if x not in s]

app = webapp2.WSGIApplication([
    ('/cross_post_to_vk', MainHandler)
], debug=True)
