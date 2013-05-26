import datetime
from google.appengine.ext import db
from google.appengine.api import users


class CrossPostedToVK(db.Model):
  cross_posted_gplus_ids = db.ListProperty(item_type=str, required=True)