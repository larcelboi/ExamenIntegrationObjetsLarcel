from nicegui import ui
from models.local import TypeLocal, Local
import httpx

lst_type_local = [TypeLocal.LABORATOIRE, TypeLocal.SALLE_SECHE]
API_URL = "http://localhost:8000"


def creer_page():
    @ui.page("/ajouter-local")
    def page_formulaire():

        with ui.column().classes("w-full h-full"):
            ui.label("Ajouter un local").classes("font-bold ")

            numero_local = ui.input(
                label="Numéro de local",
                placeholder="ex. 2.271",
                validation={
                    "Le numero est invalide": lambda e: len(e) >= 5,
                },
            )

            nom_local = ui.input(
                label="Nom du local",
                placeholder="ex. Margaret Hamilton",
                validation={
                    "Le nom du local est trop court": lambda e: len(e) >= 5,
                    "Le nom du local est trop long": lambda e: len(e) <= 30,
                },
            )

            nombre_place_max = ui.number(
                label="Nombre de places maximum",
                placeholder="ex. 24",
                min=0,
                max=50,
            ).classes("w-50")

            type_local = ui.select(
                label="Type de local",
                options=lst_type_local,
                value=TypeLocal.LABORATOIRE,
            )

            with ui.row():
                checkbox_tableau = ui.checkbox("Tableau")
                checkbox_tele = ui.checkbox("Télé")
                checkbox_projecteur = ui.checkbox("Projecteur")

            ui.label("Autres informations").classes("")

            commentaire = ui.textarea(
                label="ex. prises électriques au plafond, accès fauteil roulant..."
            ).props("clearable")

            ui.button(
                icon="check",
                text="Ajouter le local",
                on_click=lambda e: ajouterlocal(
                    numero_local,
                    nom_local,
                    nombre_place_max,
                    type_local,
                    checkbox_tableau,
                    checkbox_tele,
                    checkbox_projecteur,
                    commentaire,
                ),
            )


async def ajouterlocal(
    numero,
    nom_local,
    nombre_place_max,
    type_local,
    checkbox_tableau,
    checkbox_tele,
    checkbox_projecteur,
    commentaire,
):
    local = {
        "id": 0,
        "numero": numero.value,
        "nom": nom_local.value,
        "places_max": nombre_place_max.value,
        "type_local": type_local.value,
        "tableau": checkbox_tableau.value,
        "tele": checkbox_tele.value,
        "projecteur": checkbox_projecteur.value,
        "autres_infos": commentaire.value,
    }
    # TODO ajouter afficher validatio nerreur
    print("bob")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/api/locaux/ajouter",
            json=local,
        )

        print("asdas ENVOYÉ:", local)
        print("STATUS:", response.status_code)
        print("ERREUR API:", response.text)

        response.raise_for_status()

        nouveau_gardien = response.json()

        print("Gardien ajouté par l'API:", nouveau_gardien)
