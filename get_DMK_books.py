from DMK_parsing import save_books
from webapp.config import DMK_SITEMAP_URL
from webapp import create_app


app = create_app()
with app.app_context():
    save_books(DMK_SITEMAP_URL)
