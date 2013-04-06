# -*- coding: utf-8 -*-
r"""
constants

Se define las constantes varias utilizadas por el sistema.
"""

# User role
ADMIN = 0
STAFF = 1
USER = 2
USER_ROLE = {
    ADMIN: 'admin',
    STAFF: 'staff',
    USER: 'user',
}

# User status
INACTIVE = 0
NEW = 1
ACTIVE = 2
USER_STATUS = {
    INACTIVE: 'inactivo',
    NEW: 'nuevo',
    ACTIVE: 'activo',
}

DEFAULT_USER_AVATAR = 'default.png'
