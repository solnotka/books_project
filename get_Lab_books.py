from xml_lab import save_lab_books
from webapp.config import LABIRINT_SITEMAP_URL
from webapp import create_app


app = create_app()
with app.app_context():
    save_lab_books(LABIRINT_SITEMAP_URL)