from nicegui import ui


def entete(titre: str) -> None:
    """Affiche l'en-tête d'une page.

    Args:
        titre (str): Titre à afficher.
    """
    with ui.header(bordered=True).classes("items-center"):
        ui.label(titre).classes("text-xl font-bold")


def bouton_retour(texte: str = "Retour aux locaux", route: str = "/locaux") -> None:
    """Affiche un bouton de retour.

    Args:
        texte (str): Texte du bouton.
        route (str): Route de destination.
    """
    ui.button(texte, icon="arrow_back", on_click=lambda: ui.navigate.to(route)).props(
        "flat"
    )
