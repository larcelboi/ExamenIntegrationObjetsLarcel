import httpx
from composants import Graphique, couleur_point_qualite_air
from layout import bouton_retour
from models import EtatLocal, Local, niveau_qualite_air
from nicegui import ui


def creer_page():
    async def page_detail_local(numero: str):
        bouton_retour()

        with httpx.Client() as client:
            reponse = await client.get(f"/api/locaux/{numero}")
            donnees = reponse.json()

        local = Local(**donnees)
        etat = EtatLocal(**donnees)

        ui.label("Actionneurs").classes("text-xl font-bold")

        with ui.row().classes("items-center gap-2"):
            ui.icon("air")
            ui.label("Purificateur d'air")

        with ui.row().classes("items-center gap-2"):
            switch_purificateur = ui.switch("Activé", value=etat.purificateur_actif)

        async def envoyer_etat_purificateur(e) -> None:
            etat_precedent = etat.purificateur_actif
            async with httpx.AsyncClient() as client:
                try:
                    reponse = await client.put(
                        f"/api/locaux/{numero}/purificateur",
                        json={"actif": bool(e.args)},
                    )
                    reponse.raise_for_status()
                except httpx.HTTPStatusError as erreur_http:
                    detail = erreur_http.response.json().get(
                        "detail", "Erreur inconnue"
                    )
                    ui.notify(detail, type="negative")
                    switch_purificateur.set_value(etat_precedent)
                    return
                except httpx.HTTPError:
                    ui.notify("Impossible de contacter l'API", type="negative")
                    switch_purificateur.set_value(etat_precedent)
                    return

            nouvel_etat = EtatLocal(**reponse.json())
            etat.purificateur_actif = nouvel_etat.purificateur_actif

        switch_purificateur.on("update:model-value", envoyer_etat_purificateur, [None])
