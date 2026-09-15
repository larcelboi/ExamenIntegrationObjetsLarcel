from collections.abc import Callable

from nicegui import ui

from models import EtatLocal, Local, niveau_qualite_air


def couleur_point_qualite_air(ppm: int) -> str:
    """Retourne la couleur du niveau de qualité de l'air.

    Args:
        ppm (int): Concentration de particules dans l'air.

    Returns:
        str: Classe CSS correspondant au niveau de qualité.
    """
    niveau = niveau_qualite_air(ppm)
    if niveau == "Bonne":
        return "text-green-400"
    elif niveau == "Moyenne":
        return "text-amber-400"
    else:
        return "text-red-400"


class CarteLocal(ui.card):
    def __init__(
        self, local: Local, etat: EtatLocal, on_click: Callable[[str], None]
    ) -> None:
        """Initialise une carte de local.

        Args:
            local (Local): Local à afficher.
            etat (EtatLocal): État actuel du local.
            on_click (Callable[[str], None]): Action exécutée au clic.
        """
        super().__init__()
        self._local = local
        self._etat = etat
        with self:
            ui.label(local.numero).classes("font-bold text-lg")

            ui.label(f"Local {local.nom}").classes("text-sm text-gray-500")
            ui.label(local.type_local).classes("text-sm text-gray-500")

            # Ajouter place disponible sur la carte
            with ui.row():
                nombre_place = ui.label().bind_text_from(etat, "occupation_actuelle")
                ui.label("place disponibles")
                nombre_place_max = ui.label().bind_text_from(local, "places_max")

            with ui.row().classes("items-center gap-1"):
                self._point_qualite = ui.icon("circle").classes("text-xs")
                # Ajouter texte pour la qualité de l'air
                ui.label(
                    f"Qualité de l'air : {niveau_qualite_air(etat.qualite_air_ppm)}"
                )

            self.rafraichir()

        self.on("click", lambda: on_click(local.numero))
        self.classes("cursor-pointer")

    def rafraichir(self) -> None:
        """Met à jour la couleur selon la qualité de l'air actuelle."""
        self._point_qualite.classes(
            replace=f"text-xs {couleur_point_qualite_air(self._etat.qualite_air_ppm)}"
        )
