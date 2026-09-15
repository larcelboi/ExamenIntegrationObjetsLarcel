from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

NUMEROS_VALIDES = {"2.267", "2.268", "2.269", "2.270", "2.271", "2.272", "2.273"}


class TypeLocal(StrEnum):
    LABORATOIRE = "Laboratoire avec ordinateurs"
    SALLE_SECHE = "Salle sèche"


class Local(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    numero: str
    nom: str = Field(min_length=1, max_length=50)
    places_max: int = Field(gt=0, le=200)
    type_local: TypeLocal
    tableau: bool = False
    tele: bool = False
    projecteur: bool = False
    autres_infos: str = Field(default="", max_length=200)
    ouvert: bool = True

    @field_validator("numero")
    @classmethod
    def valider_numero(cls, valeur: str) -> str:
        if valeur not in NUMEROS_VALIDES:
            raise ValueError("Le numéro doit être entre 2.267 et 2.273.")
        return valeur
