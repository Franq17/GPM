# -*- coding: utf-8 -*-

# User estados
INACTIVE = 0
ACTIVE = 1
USER_STATUS = {
    INACTIVE: 'inactivo',
    ACTIVE: 'activo',
}

#Proyecto_estados
NO_INICIADO = 0
INICIADO = 1
FINALIZADO = 2

PROYECTO_ESTADOS = {
    NO_INICIADO: 'no iniciado',
    INICIADO: 'iniciado',
    FINALIZADO: 'finalizado',
}

# Comite_estados

COMITE_ESTADOS = {
    NO_INICIADO: 'no iniciado',
    INICIADO: 'iniciado',
}

# Fase_estados
INICIAL=0
DESARROLLO=1
COMPLETA=2
COMPROMETIDA=3

FASE_ESTADOS = {
    INICIAL: "inicial",
    DESARROLLO: "desarrollo",
    COMPLETA: "completa",
    COMPROMETIDA: "comprometida",
}

# ITEM_estados
DESAPROBADO=0
APROBADO=1
ELIMINADO=2
BLOQUEADO=3

ITEM_ESTADOS = {
    DESAPROBADO: 'desaprobado',
    APROBADO: 'aprobado',
    ELIMINADO: 'eliminado',
    BLOQUEADO: 'bloqueado',
}


# LineaBase_estados
ABIERTA=0
CERRADA=1
COMPROMETIDA=3

LINEABASE_ESTADOS = {
    ABIERTA: "abierta",
    CERRADA: "cerrada",
    COMPROMETIDA: "comprometida",
}

# Fase


DEFAULT_USER_AVATAR = 'default.png'
