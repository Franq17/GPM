# -*- coding: utf-8 -*-

# User estados
INACTIVE = 0
ACTIVE = 1
# Rol estados
NO_ASIGNADO = 0
ASIGNADO = 1

#Proyecto_estados
NO_INICIADO = 0
INICIADO = 1
FINALIZADO = 2

# Fase_estados
INICIAL=0
DESARROLLO=1
COMPLETA=2
COMPROMETIDA=3

# ITEM_estados
DESAPROBADO=0
APROBADO=1
ELIMINADO=2
BLOQUEADO=3
REVISION=4

# LineaBase_estados
ABIERTA=0
CERRADA=1
PARA_REVISION=2
COMPROMETIDA=3

# Tipos de Roles
NINGUNO=0
ADMIN=1
LIDER_PROYECTO=2
LIDER_FASE=3
DESARROLLADOR=4
# Tipos de Atributos
STRING=1
INTEGER=2
DATE=3

USER_STATUS = {
    INACTIVE: 'inactivo',
    ACTIVE: 'activo',
}

ROL_ESTADOS = {
    NO_ASIGNADO: 'no asignado',
    ASIGNADO: 'asignado',
}

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


FASE_ESTADOS = {
    INICIAL: "inicial",
    DESARROLLO: "desarrollo",
    COMPLETA: "completa",
    COMPROMETIDA: "comprometida",
}


ITEM_ESTADOS = {
    DESAPROBADO: 'desaprobado',
    APROBADO: 'aprobado',
    ELIMINADO: 'eliminado',
    BLOQUEADO: 'bloqueado',
    REVISION: 'revision',
}


LINEABASE_ESTADOS = {
    ABIERTA: "abierta",
    CERRADA: "cerrada",
    PARA_REVISION: "para revision",
    COMPROMETIDA: "comprometida",
}



TIPOS_ROLES = {
    ADMIN: "administrador",
    LIDER_PROYECTO: "lider de Proyecto",
    LIDER_FASE: "lider de Fase",
    DESARROLLADOR: "desarrollador",
    NINGUNO: "ninguno",
}


TIPOS_ATRIBUTOS = {
    STRING: "String",
    INTEGER: "Integer",
    DATE: "Date",
}


DEFAULT_USER_AVATAR = 'default.png'
