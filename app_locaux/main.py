from nicegui import ui
from pages import locaux
from pages import page_formulaire
from pages import detail_local

detail_local.creer_page()
page_formulaire.creer_page()

locaux.creer_page()

ui.run()
