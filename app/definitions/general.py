from enum import Enum


class EmissionType(str, Enum):
    EMISIONES_DIRECTAS = "EMISIONES DIRECTAS"
    EMISIONES_INDIRECTAS = "EMISIONES INDIRECTAS"
    OTRAS_EMISIONES_INDIRECTAS = "OTRAS EMISIONES INDIRECTAS"


class FuelType(str, Enum):
    COMBUSTIBLE_ADMINISTRATIVO = "COMBUSTIBLE ADMINISTRATIVO"
    COMBUSTIBLE_INDIRECTO_DE_PROVEEDOR = "COMBUSTIBLE INDIRECTO DE PROVEEDOR"
    COMBUSTIBLE_DE_LOGISTICA = "COMBUSTIBLE DE LOGISTICA"


class EnergyCategory(str, Enum):
    CONSUMO_ADMINISTRATIVO = "CONSUMO ADMINISTRATIVO"
    CONSUMO_LOGISTICO = "CONSUMO LOGISTICO"
    CONSUMO_DE_DISTIBUCION = "CONSUMO DE DISTRIBUCION"


class EnergyLocation(str, Enum):
    LOCAL = "LOCAL"
    OFICINAS_ADMINISTRATIVAS = "OFICINAS ADMINISTRATIVAS"
    PLANTA_DE_ENVASADO = "PLANTA DE ENVASADO"
    DESCONOCIDO = "DESCONOCIDO"


class OilType(str, Enum):
    CONSUMO_ADMINISTRATIVO = "CONSUMO ADMINISTRATIVO"
    CONSUMO_LOGISTICO = "CONSUMO LOGISTICO"
    CONSUMO_DE_OPERACION = "CONSUMO DE OPERACION"