from nicegui import ui
from layout import bouton_retour
import httpx

API_URL = "http://localhost:8000"


def creer_page():
    @ui.page("/page_details")
    async def detail_local():
        local = await obtenir_local()
        with ui.row():
            bouton_retour()

        with ui.row():
            ui.label()

    async def obtenir_local():
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_URL}/api/locaux/numero",
            )

            print("STATUS:", response.status_code)
            print("ERREUR API:", response.text)

            response.raise_for_status()

            nouveau_gardien = response.json()

            print("local ajouté par l'API:", nouveau_gardien)


ui.run()
