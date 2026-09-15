"""Définit la page de gestion des locaux."""

import httpx
from nicegui import ui

from composants import CarteLocal, Graphique
from layout import entete
from models import EtatLocal, Local

API_URL = "http://localhost:8000"


def creer_page():
    @ui.page("/")
    @ui.page("/locaux")
    async def page_local():
        entete("Locaux")

        ui.button(
            "Ajouter un local", on_click=lambda: ui.navigate.to("/ajouter-local")
        ).classes("self-end")

        ui.label("Répartition de l'occupation moyenne par local").classes(
            "text-xl font-bold"
        )

        async with httpx.AsyncClient() as client:
            try:
                reponse_moyennes = await client.get(
                    f"{API_URL}/api/locaux/moyenne-occupation"
                )
                reponse_moyennes.raise_for_status()
                moyennes = reponse_moyennes.json()
            except httpx.HTTPError:
                ui.notify("Impossible de contacter l'API", type="negative")
                moyennes = {}

        Graphique(
            type_graphique="pie",
            titre="Occupation moyenne par local",
            nom_axe_x="Local",
            nom_axe_y="Occupation moyenne",
            donnees_axe_x=list(moyennes.keys()),
            donnees_axe_y=list(moyennes.values()),
        ).classes("w-full")

        conteneur_cartes = ui.grid(columns=2).classes("w-full gap-4")

        cartes: dict[str, CarteLocal] = {}
        etats: dict[str, EtatLocal] = {}

        async def rafraichir():
            """Actualise les données affichées pour chaque local."""
            async with httpx.AsyncClient() as client:
                try:
                    reponse = await client.get(f"{API_URL}/api/locaux")
                    reponse.raise_for_status()
                except httpx.HTTPError:
                    ui.notify("Impossible de contacter l'API", type="negative")
                    return

            for donnees in reponse.json():
                numero = donnees["numero"]
                if numero not in cartes:
                    local = Local(**donnees)
                    etat = EtatLocal(**donnees)
                    etats[numero] = etat
                    with conteneur_cartes:
                        cartes[numero] = CarteLocal(
                            local=local,
                            etat=etat,
                            on_click=lambda numero: ui.navigate.to(
                                # TODO FIX
                                # Modifier le lien vers le bon api
                                f"{API_URL}/api/locaux/{numero}"
                            ),
                        )
                else:
                    etat = etats[numero]
                    etat.occupation_actuelle = donnees["occupation_actuelle"]
                    etat.qualite_air_ppm = donnees["qualite_air_ppm"]
                    etat.purificateur_actif = donnees["purificateur_actif"]
                    cartes[numero].rafraichir()

        await rafraichir()
        ui.timer(3.0, rafraichir)
