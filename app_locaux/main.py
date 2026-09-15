from nicegui import ui
from pages import locaux
from pages import page_formulaire
from pages import page_details

page_formulaire.creer_page()
page_details.creer_page()
locaux.creer_page()

ui.run()
