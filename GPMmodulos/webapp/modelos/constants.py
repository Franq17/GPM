# -*- coding: utf-8 -*-

# User role
ADMIN = 0
STAFF = 1
USER = 2
USER_ROLE = {
    ADMIN: 'admin',
    STAFF: 'staff',
    USER: 'user',
}

# User estados
INACTIVE = 0
NEW = 1
ACTIVE = 2
USER_STATUS = {
    INACTIVE: 'inactive',
    NEW: 'new',
    ACTIVE: 'active',
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

# LineaBase_estados
ABIERTA=0
CERRADA=1
COMPROMETIDA=3

LINEABASE_ESTADOS = {
    ABIERTA: "abierta",
    CERRADA: "cerrada",
    COMPROMETIDA: "comprometida",
}


DEFAULT_USER_AVATAR = 'default.png'
