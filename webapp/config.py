import os
import requests

basedir = os.path.abspath(os.path.dirname(__file__))
DMK_SITEMAP_URL = requests.get('https://dmkpress.com/sitemap.xml')
LABIRINT_SITEMAP_URL = 'https://www.labirint.ru/sitemap.xml'
SQLALCHEMY_TRACK_MODIFICATONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')