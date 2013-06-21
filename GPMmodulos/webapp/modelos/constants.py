# -*- coding: utf-8 -*-

# User estados
INACTIVE = 0
ACTIVE = 1
USER_STATUS = {
    INACTIVE: 'inactivo',
    ACTIVE: 'activo',
}

# Rol estados
NO_ASIGNADO = 0
ASIGNADO = 1
ROL_ESTADOS = {
    NO_ASIGNADO: 'no asignado',
    ASIGNADO: 'asignado',
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
REVISION=4

ITEM_ESTADOS = {
    DESAPROBADO: 'desaprobado',
    APROBADO: 'aprobado',
    ELIMINADO: 'eliminado',
    BLOQUEADO: 'bloqueado',
    REVISION: 'revision',
}


# LineaBase_estados
ABIERTA=0
CERRADA=1
PARA_REVISION=2
COMPROMETIDA=3

LINEABASE_ESTADOS = {
    ABIERTA: "abierta",
    CERRADA: "cerrada",
    PARA_REVISION: "para revision",
    COMPROMETIDA: "comprometida",
}

# Tipos de Roles
NINGUNO=0
ADMIN=1
LIDER_PROYECTO=2
LIDER_FASE=3
DESARROLLADOR=4


TIPOS_ROLES = {
    ADMIN: "administrador",
    LIDER_PROYECTO: "lider de Proyecto",
    LIDER_FASE: "lider de Fase",
    DESARROLLADOR: "desarrollador",
    NINGUNO: "ninguno",
}

# Tipos de Atributos
STRING=1
INTEGER=2
DATE=3
TIPOS_ATRIBUTOS = {
    STRING: "String",
    INTEGER: "Integer",
    DATE: "Date",
}


DEFAULT_USER_AVATAR = 'default.png'
