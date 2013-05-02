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
NO_INICIADO = 0
INICIADO = 1

COMITE_ESTADOS = {
    NO_INICIADO: 'no iniciado',
    INICIADO: 'iniciado',
}


DEFAULT_USER_AVATAR = 'default.png'
