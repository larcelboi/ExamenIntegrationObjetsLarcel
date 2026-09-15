from statistics import mean

from fastapi import FastAPI, HTTPException

import donnees_locaux
from models import EtatLocal, Local, ModificationPurificateur

app = FastAPI()


def _trouver_local(numero: str) -> Local:
    """Recherche un local par son numéro.

    Args:
        numero (str): Numéro du local recherche.

    Raises:
        HTTPException: Si aucun local ne correspond à ce numéro.

    Returns:
        Local: Le local trouvé.
    """
    local = next((l for l in donnees_locaux.locaux if l.numero == numero), None)
    if local is None:
        raise HTTPException(status_code=404, detail="Local introuvable")
    return local


def _trouver_etat(numero: str) -> EtatLocal:
    """Recherche l'etat d'un local par son numéro.

    Args:
        numero (str): Numéro du local recherche.

    Raises:
        HTTPException: Si aucun etat ne correspond à ce numéro.

    Returns:
        EtatLocal: L'état trouvé.
    """
    etat = donnees_locaux.etats.get(numero)
    if etat is None:
        raise HTTPException(status_code=404, detail="Local introuvable")
    return etat


@app.get("/api/locaux")
def liste_locaux() -> list[dict]:
    """Liste tous les locaux avec leur etat actualise.

    Returns:
        list[dict]: Chaque local fusionné avec son etat.
    """
    resultat = []
    for local in donnees_locaux.locaux:
        # Recupere l'etat courant du local et le rafraichit avec les dernieres simulations.
        etat = donnees_locaux.etats[local.numero]
        donnees_locaux.simuler_qualite_air(etat)
        donnees_locaux.simuler_occupation(etat, local.places_max)

        local_avec_etat = {}
        # model_dump() convertit une instance du modèle en un dict Python
        for champ, valeur in local.model_dump().items():
            local_avec_etat[champ] = valeur

        for champ, valeur in etat.model_dump().items():
            local_avec_etat[champ] = valeur

        resultat.append(local_avec_etat)

    return resultat


@app.get("/api/locaux/moyenne-occupation")
def moyenne_occupation_par_local() -> dict[str, float]:
    """Calcule l'occupation moyenne horaire de chaque local.

    Returns:
        dict[str, float]: Moyenne d'occupation par numéro de local.
    """
    return {
        numero: round(mean(valeurs.values()), 1)
        for numero, valeurs in donnees_locaux.historique_horaire.items()
    }


@app.get("/api/locaux/{numero}")
def detail_local(numero: str) -> dict:
    """Recupere le détail d'un local avec son état actualise.

    Args:
        numero (str): Numéro du local recherche.

    Raises:
        HTTPException: Si le local est introuvable.

    Returns:
        dict: Le local fusionne avec son état.
    """
    local = _trouver_local(numero)
    etat = _trouver_etat(numero)
    donnees_locaux.simuler_qualite_air(etat)
    donnees_locaux.simuler_occupation(etat, local.places_max)

    local_avec_etat = {}
    # model_dump() convertit une instance du modèle en un dict Python
    for champ, valeur in local.model_dump().items():
        local_avec_etat[champ] = valeur

    for champ, valeur in etat.model_dump().items():
        local_avec_etat[champ] = valeur

    return local_avec_etat


@app.post("/api/locaux/ajouter")
def ajouter_local(local: Local) -> Local:
    """Ajoute un nouveau local et initialise son état.

    Args:
        local (Local): Local a ajouter.

    Raises:
        HTTPException: Si le numero ou le nom existe deja.

    Returns:
        Local: Le local ajoute.
    """
    if any(l.numero == local.numero for l in donnees_locaux.locaux):
        raise HTTPException(status_code=409, detail="Ce numéro de local existe déjà")

    if any(l.nom.lower() == local.nom.lower() for l in donnees_locaux.locaux):
        raise HTTPException(status_code=409, detail="Ce nom de local existe déjà")

    donnees_locaux.locaux.append(local)
    donnees_locaux.etats[local.numero] = donnees_locaux.creer_etat_initial(local)
    donnees_locaux.historique_horaire[local.numero] = (
        donnees_locaux.generer_historique_horaire(local)
    )

    return local


@app.put("/api/locaux/{numero}/purificateur")
def changer_etat_purificateur(
    numero: str, nouvel_etat_purificateur: ModificationPurificateur
) -> EtatLocal:
    """Allume ou éteint le purificateur d'air d'un local.

    Args:
        numero (str): Numéro du local.
        nouvel_etat_purificateur (ModificationPurificateur): Nouvel état (allumé/éteint).

    Raises:
        HTTPException: Si le local est introuvable.

    Returns:
        EtatLocal: L'etat mis a jour.
    """
    etat = _trouver_etat(numero)
    etat.purificateur_actif = nouvel_etat_purificateur.actif
    return etat


@app.get("/api/locaux/{numero}/historique-horaire")
def historique_horaire(numero: str) -> dict[str, float]:
    """Recupere l'historique horaire d'occupation d'un local.

    Args:
        numero (str): Numero du local.

    Raises:
        HTTPException: Si le local est introuvable.

    Returns:
        dict[str, float]: Valeurs d'occupation par heure.
    """
    _trouver_local(numero)
    return donnees_locaux.historique_horaire[numero]
