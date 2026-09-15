from nicegui import ui
from models.local import TypeLocal, Local
import httpx
from layout import bouton_retour

lst_type_local = [TypeLocal.LABORATOIRE, TypeLocal.SALLE_SECHE]
API_URL = "http://localhost:8000"


def creer_page():
    @ui.page("/ajouter-local")
    def page_formulaire():

        with ui.column().classes("w-full h-full"):
            with ui.row():
                bouton_retour()
            ui.label("Ajouter un local").classes("font-bold ")

            numero_local = ui.input(
                label="Numéro de local",
                placeholder="ex. 2.271",
                validation={
                    "Le numéro doit être entre 2.267 et 2.273 ": lambda e: (
                        Local.field_validator(e)
                    ),
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
                label="ex. prises électriques au plafond, accès fauteil roulant...",
                validation={"Le texte est trop long": lambda e: len(e) >= 200},
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

        print("local ENVOYÉ:", local)
        print("STATUS:", response.status_code)
        print("ERREUR API:", response.text)

        if response.status_code == 422:
            ui.notify(f"{response.text}", color="red")
        else:
            ui.notify(f"Le local {local['nom']} a été ajouté !!", color="green")
            ui.navigate.to("/")
        response.raise_for_status()

        nouveau_gardien = response.json()

        print("local ajouté par l'API:", nouveau_gardien)
