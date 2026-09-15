"""Définit le composant d'affichage des graphiques."""

from nicegui import ui


class Graphique(ui.card):
    """Affiche un graphique avec les données fournies."""

    def __init__(
        self,
        type_graphique: str,
        titre: str,
        nom_axe_x: str,
        nom_axe_y: str,
        donnees_axe_x: list[str | int | float],
        donnees_axe_y: list[str | int | float],
        type_axe_x: str = "category",
        type_axe_y: str = "value",
        lissage: bool = True,
    ) -> None:
        """Initialise un graphique.

        Args:
            type_graphique (str): Type de graphique à afficher.
            titre (str): Titre du graphique.
            nom_axe_x (str): Nom de l'axe horizontal.
            nom_axe_y (str): Nom de l'axe vertical.
            donnees_axe_x (list[str | int | float]): Données de l'axe horizontal.
            donnees_axe_y (list[str | int | float]): Données de l'axe vertical.
            type_axe_x (str): Type de l'axe horizontal.
            type_axe_y (str): Type de l'axe vertical.
            lissage (bool): Active le lissage des courbes.
        """
        super().__init__()
        with self:
            ui.label(titre)

            if type_graphique == "pie":
                # N'a pas d'axes, chaque paire (nom, valeur) devient une part du cercle.
                options = {
                    "tooltip": {"trigger": "item"},
                    "legend": {"data": donnees_axe_x},
                    "series": [
                        {
                            "name": nom_axe_y,
                            "type": "pie",
                            "radius": "50%",
                            "data": [
                                {"name": nom, "value": valeur}
                                for nom, valeur in zip(donnees_axe_x, donnees_axe_y)
                            ],
                        }
                    ],
                }
            else:
                options = {
                    "tooltip": {"trigger": "item"},
                    "legend": {"data": [nom_axe_y]},
                    "xAxis": {
                        "type": type_axe_x,
                        "data": donnees_axe_x,
                        "name": nom_axe_x,
                    },
                    "yAxis": {"type": type_axe_y},
                    "series": [
                        {
                            "name": nom_axe_y,
                            "type": type_graphique,
                            "data": donnees_axe_y,
                            "smooth": lissage,
                        }
                    ],
                }

            self._chart = ui.echart(options=options)

    def ajouter_valeur(self, x: str | int | float, y: float) -> None:
        """Ajoute une valeur au graphique.

        Args:
            x (str | int | float): Position ou nom de la nouvelle valeur.
            y (float): Valeur à ajouter.
        """
        if "xAxis" in self._chart.options:
            self._chart.options["xAxis"]["data"].append(x)
            self._chart.options["series"][0]["data"].append(y)

            self._chart.options["xAxis"]["data"].pop(0)
            self._chart.options["series"][0]["data"].pop(0)
        else:
            # Camembert : on ajoute/retire des parts plutôt que des points.
            self._chart.options["series"][0]["data"].append({"name": x, "value": y})
            self._chart.options["series"][0]["data"].pop(0)

        self._chart.update()

    def remplacer_donnees(
        self,
        donnees_axe_x: list[str | int | float],
        donnees_axe_y: list[str | int | float],
    ) -> None:
        """Remplace les données d'un graphique cartésien.

        Args:
            donnees_axe_x (list[str | int | float]): Nouvelles données horizontales.
            donnees_axe_y (list[str | int | float]): Nouvelles données verticales.
        """

        self._chart.options["xAxis"]["data"] = donnees_axe_x
        self._chart.options["series"][0]["data"] = donnees_axe_y
        self._chart.update()

    def remplacer_donnees_pie(self, donnees: dict[str, float]) -> None:
        """Remplace les données d'un graphique circulaire.

        Args:
            donnees (dict[str, float]): Noms et valeurs des parts.
        """

        self._chart.options["series"][0]["data"] = [
            {"name": nom, "value": valeur} for nom, valeur in donnees.items()
        ]
        self._chart.update()
