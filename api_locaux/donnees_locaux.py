import random

from models import EtatLocal, Local, TypeLocal

locaux: list[Local] = [
    Local(
        numero="2.267",
        nom="Ada Lovelace",
        places_max=24,
        type_local=TypeLocal.LABORATOIRE,
        tableau=True,
        tele=False,
        projecteur=True,
        ouvert=True,
    ),
    Local(
        numero="2.268",
        nom="Alan Turing",
        places_max=30,
        type_local=TypeLocal.SALLE_SECHE,
        tableau=True,
        tele=True,
        projecteur=True,
        ouvert=True,
    ),
    Local(
        numero="2.269",
        nom="Centre d'aide",
        places_max=15,
        type_local=TypeLocal.SALLE_SECHE,
        tableau=False,
        tele=False,
        projecteur=False,
        ouvert=False,
    ),
    Local(
        numero="2.273",
        nom="Grace Hopper",
        places_max=20,
        type_local=TypeLocal.LABORATOIRE,
        tableau=True,
        tele=False,
        projecteur=True,
        ouvert=True,
    ),
]


def creer_etat_initial(local: Local) -> EtatLocal:
    """Cree l'état initial d'un local avec des valeurs aleatoires.

    Args:
        local (Local): Local pour lequel generer l'état.

    Returns:
        EtatLocal: L'état initial genere.
    """
    return EtatLocal(
        numero=local.numero,
        occupation_actuelle=random.randint(0, local.places_max),
        qualite_air_ppm=random.randint(400, 1400),
        purificateur_actif=True,
    )


def generer_historique_horaire(local: Local) -> dict[str, float]:
    """Genere le profil moyen d'occupation par heure (8h à 20h).

    Calcule à partir de facteurs fixes mis à l'échelle de la capacité
    du local. Entièrement déterministe (pas d'aléatoire) : ce n'est pas
    un vrai historique jour par jour, juste un profil horaire type qui
    ne change pas d'un redémarrage à l'autre.

    Args:
        local (Local): Local pour lequel generer l'historique.

    Returns:
        dict[str, float]: Occupation moyenne par heure.
    """

    HEURES = [f"{heure}h" for heure in range(8, 21)]

    FACTEURS_OCCUPATION_HORAIRE = [
        0.2,
        0.4,
        0.7,
        0.85,
        0.5,
        0.5,
        0.8,
        0.9,
        0.85,
        0.7,
        0.5,
        0.3,
        0.15,
    ]
    historique = {}
    for heure, facteur in zip(HEURES, FACTEURS_OCCUPATION_HORAIRE):
        historique[heure] = round(local.places_max * facteur, 1)
    return historique


def simuler_qualite_air(etat: EtatLocal) -> None:
    """Fait évoluer la qualité de l'air à chaque appel de l'API.

    Purificateur allumé : l'air s'améliore vers le plancher (bonne
    qualité). Purificateur éteint : l'air se dégrade vers le plafond
    (mauvaise qualité).

    Args:
        etat (EtatLocal): État du local a mettre a jour.
    """

    # ppm retirés par appel quand le purificateur est allumé
    PAS_AMELIORATION = 40
    # ppm ajoutés par appel quand le purificateur est éteint
    PAS_DEGRADATION = 30
    # léger bruit de capteur, pour éviter que la valeur reste figée une
    # fois le plancher/plafond atteint (sinon plus aucune variation n'est
    # visible tant que l'état du purificateur ne change pas)
    BRUIT_CAPTEUR = 5
    PPM_MIN = 400
    PPM_MAX = 2000

    bruit = random.randint(-BRUIT_CAPTEUR, BRUIT_CAPTEUR)

    if etat.purificateur_actif:
        etat.qualite_air_ppm = max(
            PPM_MIN, min(PPM_MAX, etat.qualite_air_ppm - PAS_AMELIORATION + bruit)
        )
    else:
        etat.qualite_air_ppm = max(
            PPM_MIN, min(PPM_MAX, etat.qualite_air_ppm + PAS_DEGRADATION + bruit)
        )


def simuler_occupation(etat: EtatLocal, places_max: int) -> None:
    """Fait varier aléatoirement l'occupation, pour simuler les allées et venues.

    Args:
        etat (EtatLocal): État du local a mettre a jour.
        places_max (int): Capacite maximale du local.
    """

    variation = random.randint(-2, 2)
    etat.occupation_actuelle = min(
        places_max, max(0, etat.occupation_actuelle + variation)
    )


# État courant de chaque local, indexé par son numéro
etats: dict[str, EtatLocal] = {
    local.numero: creer_etat_initial(local) for local in locaux
}

historique_horaire: dict[str, dict[str, float]] = {
    local.numero: generer_historique_horaire(local) for local in locaux
}
