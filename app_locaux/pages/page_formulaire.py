from nicegui import ui
from models.local import TypeLocal

lst_type_local = [TypeLocal.LABORATOIRE, TypeLocal.SALLE_SECHE]


def creer_page():
    @ui.page("/ajouter-local")
    def page_formulaire():

        with ui.column().classes("w-full h-full"):
            ui.label("Ajouter un local").classes("font-bold ")

            numero_local = ui.input(label="Numéro de local", placeholder="ex. 2.271")

            numero_local = ui.input(
                label="Nom du local", placeholder="ex. Margaret Hamilton"
            )

            nom_local = ui.input(label="Nombre de places maximum", placeholder="ex. 24")

            nombre_place_max = ui.select(
                label="Type de local",
                options=lst_type_local,
                value=TypeLocal.LABORATOIRE,
            )

            ui.label("Autres informations").classes("")

            commentaire = ui.textarea(
                label="ex. prises électriques au plafond, accès fauteil roulant..."
            ).props("clearable")

            ui.button(icon="check", text="Ajouter le local")
