# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
try:
    from sqlalchemy.ext.mutable import Mutable
except ImportError:
    from sqlalchemy.types import MutableType as Mutable
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from datetime import date

#librerias para reportes
from geraldo import Report, ReportBand, DetailBand, SystemField, Label, ObjectValue, ReportGroup
from geraldo.utils import cm, BAND_WIDTH, TA_CENTER, TA_RIGHT

from ..extensions import db
from ..utils import get_current_time

from .constants import INACTIVE, USER_STATUS,NO_INICIADO, PROYECTO_ESTADOS, LINEABASE_ESTADOS, FASE_ESTADOS, ITEM_ESTADOS, SOLICITUD_ESTADOS, VOTACION_ESTADOS, NO_VOTADO

from .constants import INICIAL, DESARROLLO, COMPLETA, DESAPROBADO, ROL_ESTADOS, TIPOS_ROLES, NO_ASIGNADO, ABIERTA, TIPOS_ATRIBUTOS



class DenormalizedText(Mutable, types.TypeDecorator):
    """
    Stores denormalized primary keys that can be
    accessed as a set.

    :param coerce: coercion function that ensures correct 
    type is returned

    :param separator: separator character
    """

    impl = types.Text

    def __init__(self, coerce=int, separator=" ", **kwargs):

        self.coerce = coerce
        self.separator = separator

        super(DenormalizedText, self).__init__(**kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            items = [str(item).strip() for item in value]
            value = self.separator.join(item for item in items if item)
        return value

    def process_result_value(self, value, dialect):
        if not value:
            return set()
        return set(self.coerce(item) for item in value.split(self.separator))

    def copy_value(self, value):
        return set(value)


permisoPorRol = db.Table('permisoPorRol',
    Column('rol_id', db.Integer, db.ForeignKey('rol.id')),
    Column('permiso_id', db.Integer, db.ForeignKey('permiso.id'))
)

usuarioPorComite = db.Table('usuarioPorComite',
    Column('comite_id', db.Integer, db.ForeignKey('comite.id')),
    Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

usuarioPorProyecto = db.Table('usuarioPorProyecto',
    Column('proyecto_id', db.Integer, db.ForeignKey('proyecto.id')),
    Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

rolPorUsuario = db.Table('rolPorUsuario',
    Column('rol_id', db.Integer, db.ForeignKey('rol.id')),
    Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

rolPorProyecto = db.Table('rolPorProyecto',
    Column('rol_id', db.Integer, db.ForeignKey('rol.id')),
    Column('proyecto_id', db.Integer, db.ForeignKey('proyecto.id'))
)

atributoPorTipoItem = db.Table('atributoPorTipoItem',
    Column('tipoItem_id', db.Integer, db.ForeignKey('tipoItem.id')),
    Column('atributo_id', db.Integer, db.ForeignKey('atributo.id'))
)

atributoPorItem = db.Table('atributoPorItem',
    Column('item_id', db.Integer, db.ForeignKey('item.id')),
    Column('atributo_id', db.Integer, db.ForeignKey('atributo.id'))
)

solicitudPorUsuario = db.Table('solicitudPorUsuario',
    Column('user_id', db.Integer, db.ForeignKey('users.id')),
    Column('solicitud_id', db.Integer, db.ForeignKey('solicitud.id'))
)

tipoItemPorFase = db.Table ('tipoItemPorFase',
    Column('tipoItem_id', db.Integer, db.ForeignKey('tipoItem.id')),
    Column('fase_id', db.Integer, db.ForeignKey('fase.id'))
)

############################################################################################
#            Agregado de Adolfismo
############################################################################################



archivoPorItem = db.Table('asociacion_item_archivo',
    Column('item_id', db.Integer, db.ForeignKey('item.id')),
    Column('archivo_id', db.Integer, db.ForeignKey('archivo.id'))
)

class Antecesores(db.Model):
    __tablename__ = 'sucesores'
    id = Column(db.Integer, primary_key=True)
    item_id = Column(db.Integer)
    antecesor_id = Column (db.Integer)
    
    
class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(32), nullable=False, unique=True)
    nombre = Column(db.String)
    apellido = Column(db.String)
    email = Column(db.String)
    telefono = Column(db.String)
    ci = Column(db.String)
    activation_key = Column(db.String)
    created_time = Column(db.DateTime, default=get_current_time)
    _password = Column('password', db.String, nullable=False)
    avatar = Column(db.String)
    status_id = Column(db.SmallInteger, default=INACTIVE)
    
# RELACIONES ==========================================================================

    #esLiderFase = db.relationship('Fase', backref='users',lazy='dynamic')
    # Many-to-many relationship    
    rolPorUsuario = db.relationship('Rol', secondary=rolPorUsuario,
       backref=db.backref('users', lazy='dynamic'))
    
    solicitudPorUsuario = db.relationship('Solicitud', secondary=solicitudPorUsuario,
       backref=db.backref('users', lazy='dynamic'))
    
    
# FUNCIONES ======================================================================
    # Password
    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)
    # Hide password encryption by exposing password field only.
    password = db.synonym('_password',
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)
        
    def comprobarPermiso (self, key):
        roles = self.rolPorUsuario
        for item in roles: 
            rol=Rol.query.filter_by(id=item.id).first_or_404()
            permisos=rol.permisoPorRol
            for permiso in permisos:
                if permiso.nombre==key:
                    return True          
        return False  
    
    def getNombreUsuario(self):
        return self.name
    
    def getNombre(self):
        return self.nombre
    
    def getApellido(self):
        return self.apellido
    
    def getTelefono(self):
        return self.telefono
    
    def getCI(self):
        return self.ci
    
    def getEmail(self):
        return self.email
    
    def getProyectos (self):
        todosProyectos = Proyecto.query.all()
        
        misProyectos=[]
        for proyecto in todosProyectos:
            unProyecto=Proyecto.query.filter_by(id=proyecto.id).first_or_404()
            miembros=unProyecto.usuarioPorProyecto
            for miembro in miembros:
                if self.id==miembro.id:
                    misProyectos.append(unProyecto)
        return misProyectos
    
    def getProyectosDeLider(self):
        todosProyectos = Proyecto.query.all()
        
        misProyectos=[]
        for proyecto in todosProyectos:
            if self.id == proyecto.lider_proyecto:
                misProyectos.append(proyecto)
        return misProyectos
        
    def getCantSolicitudes (self):
        listaTotal = []
        listaSolicitudes = self.solicitudPorUsuario
        for solicitud in listaSolicitudes:
            if solicitud.getEstado()=='no votado':
                listaTotal.append(solicitud)
        return len(listaTotal)
    
    def getItemsDeSolicitudes (self):
        listaSolicitudes = self.solicitudPorUsuario
        listaItem=[]
        for solicitud in listaSolicitudes:
            item = Item.query.filter_by(id = solicitud.item_id).first_or_404()
            listaItem.append(item)
        return listaItem
    
    def getSolicitud(self):
        listaSolicitudes = []
        listaSolicitudes = self.solicitudPorUsuario
        if listaSolicitudes is not None:
            for solicitud in listaSolicitudes:
                if solicitud.getEstado()=='no votado':
                    return solicitud
                    break
        

    def estaEnComite(self, comite_id):
        comite = Comite.query.filter_by(id=comite_id).first_or_404()
        members = comite.usuarioPorComite
        for member in members:
            if self.id == member.id:
                return True
        return False
    
    ## Falta arreglar para el caso de desasignar el rol de un usuario en un Proyecto
    def puedeSerLiderFase(self):
        roles = self.rolPorUsuario
        for rol in roles:
            unRol = Rol.query.filter_by(id=rol.id).first_or_404()
            if unRol.getTipo() == 'lider de Fase':
                return True
        return False
    
    def puedeSerLiderProyecto(self):
        roles = self.rolPorUsuario
        for rol in roles:
            unRol = Rol.query.filter_by(id=rol.id).first_or_404()
            if unRol.getTipo() == 'lider de Proyecto':
                return True
        return False
    
    def puedeSerDesarrollador(self):
        roles = self.rolPorUsuario
        for rol in roles:
            unRol = Rol.query.filter_by(id=rol.id).first_or_404()
            if unRol.getTipo() == 'desarrollador':
                return True
        return False
     
    def esLiderDeFase(self, proyecto_id):
        proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
        fases = proyecto.fases
        for fase in fases:
            fase = Fase.query.filter_by(id=fase.id).first_or_404()
            if self.id == fase.lider_fase:
                return True
        return False

    def getStatus(self):
        return USER_STATUS[self.status_id]
    
    def setStatus(self, estado):
        self.status_id = estado

    def setNombre(self, nombre):
        self.nombre= nombre
    
    def setNombreUsuario(self, name):
        self.name = name
    
    def setApellido(self, apellido):
        self.apellido = apellido
    
    def setTelefono(self, telefono):
        self.telefono = telefono
    
    def setCI(self, ci):
        self.ci = ci
    
    def setEmail(self, email):
        self.email= email

    # ================================================================
    # Follow / Following
    followers = Column(DenormalizedText)
    following = Column(DenormalizedText)

    @property
    def num_followers(self):
        if self.followers:
            return len(self.followers)
        return 0

    @property
    def num_following(self):
        return len(self.following)

    def follow(self, user):
        user.followers.add(self.id)
        self.following.add(user.id)

    def unfollow(self, user):
        if self.id in user.followers:
            user.followers.remove(self.id)

        if user.id in self.following:
            self.following.remove(user.id)

    def get_following_query(self):
        return User.query.filter(User.id.in_(self.following or set()))

    def get_followers_query(self):
        return User.query.filter(User.id.in_(self.followers or set()))

    # ================================================================
    # Class methods

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(db.or_(User.name == login, User.email == login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    @classmethod
    def search(cls, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(
                User.name.ilike(keyword),
                User.email.ilike(keyword),
            ))
        q = reduce(db.and_, criteria)
        return cls.query.filter(q)  
    

class Rol(db.Model):

    __tablename__ = 'rol'

    id = Column(db.Integer, primary_key=True)
    nombre = Column(db.String(32), nullable=False, unique=True)
    tipo = Column(db.SmallInteger)
    descripcion = Column(db.String)
    estado_id = Column(db.SmallInteger, default=NO_ASIGNADO)
    
# RELACIONES =================================================================
    permisoPorRol = db.relationship('Permiso', secondary=permisoPorRol,
        backref=db.backref('permisoPorRol', lazy='dynamic'))
 
# FUNCIONES  ==================================================================
    def getNombre(self):
        return self.nombre
    
    def getDescripcion(self):
        return self.descripcion
    
    def setNombre(self, nombre):
        self.nombre= nombre
    
    def setDescripcion(self, descripcion):
        self.descripcion= descripcion
    
    def getTipo(self):
        return TIPOS_ROLES[self.tipo]
    
    def setTipo(self, tipo):
        self.tipo = tipo
    
    def getEstado(self):
        return ROL_ESTADOS[self.estado_id]
    
    def setEstado(self, estado):
        self.estado_id = estado
    
    def getUsuarios(self):
        users = User.query.all()
        userList = []
        for user in users:
            roles = user.rolPorUsuario
            if self in roles:
                userList.append(user)
        return userList

    def comprobarAsignacion(self):
        users = self.getUsuarios()
        if len(users)==0:
            self.setEstado(0)
    
    def cargarPermisos(self):
        if self.getTipo()=="administrador":
            for pid in range(1,32):
                permiso = Permiso.query.filter_by(id=pid).first_or_404()
                self.permisoPorRol.append(permiso)
        elif self.getTipo()=="lider de Proyecto":
            perLider = Permiso.query.filter_by(id=32).first_or_404()
            perReporte = Permiso.query.filter_by(id=35).first_or_404()
            self.permisoPorRol.append(perLider)
            self.permisoPorRol.append(perReporte)
            for pid in range(10,19):
                permiso = Permiso.query.filter_by(id=pid).first_or_404()
                self.permisoPorRol.append(permiso)
        elif self.getTipo()=="lider de Fase":
            perLider = Permiso.query.filter_by(id=33).first_or_404()
            self.permisoPorRol.append(perLider)
            for pid in range(19,27):
                permiso = Permiso.query.filter_by(id=pid).first_or_404()
                self.permisoPorRol.append(permiso)
        elif self.getTipo()=="desarrollador":
            perDesarrollador = Permiso.query.filter_by(id=34).first_or_404()
            self.permisoPorRol.append(perDesarrollador)
            for pid in range(19,23):
                permiso = Permiso.query.filter_by(id=pid).first_or_404()
                self.permisoPorRol.append(permiso)
            for pid in range(27,31):
                permiso = Permiso.query.filter_by(id=pid).first_or_404()
                self.permisoPorRol.append(permiso)
    
    # Class methods

    @classmethod
    def search(cls, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_
            (Rol.nombre.ilike(keyword))
            )
        q = reduce(db.and_, criteria)
        return cls.query.filter(q)


class Proyecto(db.Model):

    __tablename__ = 'proyecto'

    id = Column(db.Integer, primary_key=True)
    nombre = Column(db.String(32), nullable=False, unique=True)
    descripcion = Column(db.String(200), nullable=True)
    complejidad_total = Column(db.Integer, nullable=False, default=0)
    numero_fases = Column(db.Integer, nullable=False)
    created_time = Column(db.DateTime, default=get_current_time)
    lider_proyecto = Column(db.Integer(), nullable=True)
    estado_id = Column(db.SmallInteger, default=NO_INICIADO)
       
# RELACIONES  ===========================================================================
    
    # One-to-one relationship
    comite = db.relationship('Comite', backref='proyecto', uselist=False)
    # One-to-many relationship
    fases = db.relationship('Fase', backref='proyecto',lazy='dynamic')

    tiposItem = db.relationship('TipoItem', backref='proyecto',lazy='dynamic')
    items = db.relationship('Item', backref='proyecto',lazy='dynamic')
    
    # Many-to-many relationship
    rolPorProyecto = db.relationship('Rol', secondary=rolPorProyecto,
        backref=db.backref('proyectos', lazy='dynamic'))

    usuarioPorProyecto = db.relationship('User', secondary=usuarioPorProyecto,
        backref=db.backref('usuarioPorProyecto', lazy='dynamic'))  
        

# FUNCIONES ===============================================================================
    def calcularCosto(self):
        cont = 0
        for item in self.items:
            cont = cont + item.getComplejidad()
        return cont
    
    def getNombre(self):
        return self.nombre
    
    def getDescripcion(self):
        return self.descripcion
    
    def getComplejidad(self):
        return self.complejidad_total
    
    def getEstado(self):
        return PROYECTO_ESTADOS[self.estado_id]
    
    def setEstado(self, estado):
        self.estado_id = estado
            
    def getNroFases(self):
        return self.numero_fases
    
    def getFases(self):
        return self.fases
    
    def setNombre(self, nombre):
        self.nombre= nombre
    
    def setDescripcion(self, descripcion):
        self.descripcion= descripcion
    
    def setComplejidad(self, complejidad):
        self.complejidad_total= complejidad
    
    def setNroFases(self, numero):
        self.numero_fases= numero

    def getTodosProyectos(self):
        todosProyectos = Proyecto.query.filter(Proyecto.id != self.id)
        return todosProyectos
    
    def getLider(self):
        lider = User.query.filter_by(id=self.lider_proyecto).first_or_404()
        return lider.nombre+' '+lider.apellido
    
    def getUsuariosLideresFase(self):
        users = self.usuarioPorProyecto
        usuariosLideres=[]
        for user in users:
            usuario = User.query.filter_by(id=user.id).first_or_404()
            if usuario.puedeSerLiderFase():
                usuariosLideres.append(usuario)
        return usuariosLideres
    
    def getUsuariosLideresProyecto(self):
        users = self.usuarioPorProyecto
        usuariosLideres=[]
        for user in users:
            usuario = User.query.filter_by(id=user.id).first_or_404()
            if usuario.puedeSerLiderProyecto():
                usuariosLideres.append(usuario)
        return usuariosLideres
    
    def existeTipoItem(self):
        tipos = self.tiposItem
        count=0
        for tipo in tipos:
            count+=1
        if count==0:
            return False
        else:
            return True
        
    def existeTipoItemEnFase(self):
        fases = self.fases
        for fase in fases:
            if not fase.tipoItemPorFase:
                return False
        return True
    
    def getFasePorNumero(self, numero_orden):
        fases = self.fases
        for fase in fases:
            if fase.numero_fase == numero_orden:
                return fase
        return None    
    # ================================================================
    # Follow / Following
    followers = Column(DenormalizedText)
    following = Column(DenormalizedText)
    
    @property
    def num_followers(self):
        if self.followers:
            return len(self.followers)
        return 0

    @property
    def num_following(self):
        return len(self.following)

    def follow(self, proyecto):
        proyecto.followers.add(self.id)
        self.following.add(proyecto.id)

    def unfollow(self, proyecto):
        if self.id in proyecto.followers:
            proyecto.followers.remove(self.id)

        if proyecto.id in self.following:
            self.following.remove(proyecto.id)

    def get_following_query(self):
        return Proyecto.query.filter(Proyecto.id.in_(self.following or set()))

    def get_followers_query(self):
        return Proyecto.query.filter(Proyecto.id.in_(self.followers or set()))

    # ================================================================
    # Class methods

    @classmethod
    def search(cls, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(
                Proyecto.nombre.ilike(keyword)
            ))
        q = reduce(db.and_, criteria)
        return cls.query.filter(q)

    
class Fase(db.Model):
    __tablename__='fase'
    
    id = Column(db.Integer, primary_key=True)
    nombre = Column(db.String(32), nullable=False)
    descripcion = Column(db.String(),nullable=True)
    numero_fase = Column(db.Integer,nullable=True)
    numero_lb = Column(db.Integer,default=0)
    estado_id = Column(db.SmallInteger,default=INICIAL)
    lider_fase = Column(db.Integer, nullable=True)
    
# RELACIONES =================================================================
    # Many-to-one relationship
    proyecto_id = Column(db.Integer, db.ForeignKey('proyecto.id'))
    #liderFase_id = Column(db.Integer(), db.ForeignKey('users.id'))
    # One-to-many relationship
    lineaBase = db.relationship('LineaBase', backref='fase',lazy='dynamic')
    items = db.relationship('Item', backref='fase',lazy='dynamic')
    # Many-to-many relationship
    tipoItemPorFase = db.relationship('TipoItem', secondary=tipoItemPorFase,
       backref=db.backref('fases', lazy='dynamic'))
    
    
# FUNCIONES =================================================================    

    def getNombre(self):
        return self.nombre
    
    def getDescripcion(self):
        return self.descripcion
    
    def getNroItems(self):
        cont= 0
        for item in self.items:
            if item.getEstado() != 'Eliminado':
                cont= cont + 1
        return cont
    
    def getEstado(self):
        return FASE_ESTADOS[self.estado_id]
    
    def getNroLB(self):
        return self.numero_lb
    
    def getNroFase(self):
        return self.numero_fase
    
    def setNombre(self, nombre):
        self.nombre= nombre
    
    def setDescripcion(self, descripcion):
        self.descripcion= descripcion
    
    def setNroLB(self, cantidad):
        self.numero_lb= cantidad
    
    def setEstado(self, estado):
        self.estado_id = estado
    
    def getItems (self):
        misItems = Item.query.filter_by(fase_id=self.id).order_by("nombre asc")
        return misItems
    
    def existeTipoItem (self, tipoItem_id):
        
        for tipo in self.tipoItemPorFase:
            print tipo.nombre
            if tipo.id == tipoItem_id:
                return True
        return False
    
    def getLider(self):
        lider = User.query.filter_by(id=self.lider_fase).first_or_404()
        return lider.nombre+' '+lider.apellido
    
    def setLider(self, lider):
        self.lider_fase = lider
    
    def actualizarEstado(self):
        inicial= True
        completo= False
        desarrollo= False
        for item in self.items:
            if item.getEstado() != 'eliminado':
                completo= True
                if item.getEstado() != 'bloqueado':
                    desarrollo= True
        
        if inicial and not(completo) and not(desarrollo):
            self.estado_id = INICIAL
        if inicial and completo and not(desarrollo):
            self.estado_id= COMPLETA
        if inicial and completo and desarrollo:
            self.estado_id= DESARROLLO
        
    def getFaseSiguiente(self, proyecto):
        for fase in proyecto.fases:
            if fase.numero_fase == self.numero_fase+1:
                faseSiguiente = fase
        return faseSiguiente
    
    def tieneSiguiente(self, proyecto):
        for fase in proyecto.fases:
            if fase.numero_fase == self.numero_fase+1:
                return True
        return False

    
class TipoItem(db.Model):
    
    __tablename__ = 'tipoItem'
    
    id = Column(db.Integer, primary_key=True)
    nombre= Column(db.String(32), nullable=False)
    descripcion= Column(db.String(200), nullable=True)
    proyecto_id = Column(db.Integer, db.ForeignKey('proyecto.id'))

# RELACIONES  ===========================================================================
    atributoPorTipoItem = db.relationship('Atributo', secondary=atributoPorTipoItem,
        backref=db.backref('tiposItem', lazy='dynamic'))
    
# FUNCIONES =============================================================================   
    
    def getNombre(self):
        return self.nombre
    
    def getDescripcion(self):
        return self.descripcion
    
    def getAtributos(self):
        return self.atributos
    
    def getNroAtributos(self):
        return len(self.atributoPorTipoItem)
    
    def setNombre(self, nombre):
        self.nombre= nombre
    
    def setDescripcion(self, descripcion):
        self.descripcion= descripcion
    
    # ================================================================
    # Class methods

    @classmethod
    def search(cls, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_
            (TipoItem.nombre.ilike(keyword))
            )
        q = reduce(db.and_, criteria)
        return cls.query.filter(q)


class Item(db.Model):
    __tablename__='item'
    
    id = Column(db.Integer, primary_key=True)
    nombre = Column(db.String(32), nullable=False)
    descripcion = Column(db.String(),nullable=True)
    version = Column(db.Integer)
    complejidad= Column(db.Integer, default=0) 
    estado_id = Column(db.SmallInteger,default=DESAPROBADO)
    marcado = Column(db.String(2),nullable=True)

    
# RELACIONES  ====================================================================

    proyecto_id = Column(db.Integer, db.ForeignKey('proyecto.id'))
    fase_id = Column(db.Integer, db.ForeignKey('fase.id')) 

    solicitudes = db.relationship('Solicitud', backref='item',lazy='dynamic')
    lineaBase_id = Column(db.Integer, db.ForeignKey('lineaBase.id'))
    
    """
    estas dos columnas son para relacionar muchos items con un tipo de item
    """
    tipoItem_id= Column(db.Integer, db.ForeignKey('tipoItem.id'), nullable=True)
#    tipoItem = db.relationship("TipoItem", backref='item', lazy='dynamic')
    #atributos = db.relationship('Atributo', backref='item',lazy='dynamic')
    
    atributos= db.relationship('Atributo', secondary=atributoPorItem,
       backref=db.backref('items', lazy='dynamic'))
    
    archivoPorItem= db.relationship('Archivo', secondary=archivoPorItem,
       backref=db.backref('archivo', lazy='dynamic'))
    """
    estas dos columnas son para relaciones de versiones de items
    """
    #versionSuperior_id = Column(db.Integer, db.ForeignKey('item.id'))
    #versionAnterior = db.relationship("Item")
    
    padre_id = Column(db.Integer,db.ForeignKey('item.id'))
    hijo = db.relationship("Item",
                backref=db.backref('padre', remote_side=[id])
            )
    sucesor_id = Column(db.Integer)
    """
    relacion con el item sucesor
    """
    #sucesores = db.relationship('Item', secondary=sucesorPorItem,
    #                            backref=db.backref('antecesor', lazy='dynamic'))
    def getAntecesores(self):
        todosAntecesores = Antecesores.query.all()
        misAntecesores = []
        for relacion in todosAntecesores:
            if relacion.item_id == self.id and relacion.antecesor_id != self.id:
                item = Item.query.filter_by(id=relacion.antecesor_id).first()
                misAntecesores.append(item)
        misAntecesores = self.eliminar_duplicados(misAntecesores)
        return misAntecesores
    
    def getSucesor(self):
        sucesor = Item.query.filter_by(id=self.sucesor_id).first()
        return sucesor
    
    def getSucesores(self):
        proyecto = Proyecto.query.filter_by(id=self.proyecto_id).first_or_404()
        fase = Fase.query.filter_by(id=self.fase_id).first_or_404()
        lista_hijos = self.getGeneraciones(fase, self)
        ubicacion = fase.numero_fase
        lista=[]
        for aux in lista_hijos:
            fase= proyecto.getFasePorNumero(ubicacion+1)
                # agregar funcion if tieneSucesor
            sucesor = aux.getSucesor()
            if (sucesor is None) == False:
                if sucesor.getEstado() != 'eliminado' and aux.getSucesor() in fase.items:
                    lista = lista + sucesor.getSucesores()
            
            lista = lista + [aux]
        lista= self.eliminar_duplicados(lista)  
        return lista
    
    def getAntecesores2 (self):
        lista= []
        proyecto = Proyecto.query.filter_by(id=self.proyecto_id).first_or_404()
        fase = Fase.query.filter_by(id=self.fase_id).first_or_404()
        
        ubicacion= fase.numero_fase
        lista= self.getAscendientes(fase)
        if ubicacion > 1:
            listaAdd= []
            for aux in lista:
                #for candidato in faseAnterior.items:
                for antecesor in aux.getAntecesores():
                    if antecesor.getEstado() != 'eliminado':
                        listaAdd= listaAdd + antecesor.getAntecesores2()
            lista = lista + listaAdd
        lista= self.eliminar_duplicados(lista)    
        return lista
    
    def calcular_impacto_delante(self):
        """
        note: items que son sucesores, inclyendo el item
        """
        lista= self.getSucesores()
        cont= 0
        for aux in lista:
                cont= cont + aux.getComplejidad()
        return cont        
    
    def calcular_impacto_atras(self):
        """
        note: items que son antecesores, inclyendo el item
        """
        lista= self.getAntecesores2()
        cont= 0
        for aux in lista:
                cont= cont + aux.getComplejidad()
        return cont        

    def calcular_impacto_total(self):
        """
        note: calculo hacia adelante + calculo hacia atras
        """
        impacto = self.calcular_impacto_delante() + self.calcular_impacto_atras() - self.getComplejidad()
        return impacto        


# FUNCIONES  ====================================================================   
    def eliminar_duplicados(self, lista):
        refinada= []
        for aux in lista:
            if aux not in refinada:
                refinada.append(aux)
        return refinada

    def getHistorial(self):
        todosHistoriales = HistorialItem.query.all()
        historiales=[]
        for historial in todosHistoriales:
            if historial.itemId==self.id:
                historiales.append(historial)
        return historiales

    def getNombre(self):
        return self.nombre
       
    def getNumeroTipoItem(self):
        return self.numeroTipoItem
    
    def getVersion(self):
        return self.version
    
    def getEstado(self):
        return ITEM_ESTADOS[self.estado_id]
    
    def setEstado(self, estado):
        self.estado_id = estado
    
    def getComplejidad(self):
        return self.complejidad
    
    def getDescripcion(self):
        return self.descripcion
    
    def getMarcado(self):
        return self.marcado
    
    def marcarRevision(self):
        self.estado_id = 4 #Estado: 'revision'
    
    def tieneLineaBase(self):
        if self.lineaBase_id != None:
            return True
        else:
            return False
    
    def getFase(self):
        fase = Fase.query.filter_by(id=self.fase_id).first_or_404()
        return fase
    
#    def getLineaBase(self, session):
#        lb= session.query(LineaBase).filter_by(id= self.lineaBase_id).first()
#        return lb
    
    def tieneVersionAnterior(self):
        if len(self.versionAnterior) > 0:
            return True
        else:
            return False
    
    def getVersionAnterior(self):
        return self.versionAnterior[0]
    
    def tieneVersionSuperior(self):
        if self.versionSuperior_id == None:
            return False
        else:
            return True
    
    def getVersionSuperior(self, session):
        item= session.query(Item).filter_by(id= self.versionSuperior_id).first()
        return item
    
    def getTipoItem(self):
        return self.tipoItem.getNombre()
    
    def getAtributos(self):
        return self.atributos
    
    def tienePadre(self, fase):
        for item in fase.items:
            if item.getEstado() != 'eliminado' and item != self:
                if self.padre_id is not None:
                    return True
        return False
    
    """
    note: metodo que devuelve el padre del item, devuelve String en caso de no tener
    """
    def getPadre(self):
        padre = Item.query.filter_by(id=self.padre_id).first()
        if padre is None:
            return None
        return padre.nombre
    
    """
    note: metodo que devuelve el padre del item, devuelve String en caso de no tener
    """
    def getItemPadre(self):
        padre = Item.query.filter_by(id=self.padre_id).first()
        return padre
    """
    note metodo que pregunta si un item es descendiente de otro en una fase dada
    """
    def esDescendiente(self, fase, item):
        lista_descendientes = self.getGeneraciones(fase, self)
        return item in lista_descendientes
    
    """
    note: metodo que acumula los hijos, nietos etc. de un item en una lista incluyendose al item
    """
    def getGeneraciones(self, fase, item):
        lista= []
        for hij in item.hijo:
            if hij.getEstado() != 'Eliminado' and hij in fase.items:
                lista= lista + item.getGeneraciones(fase, hij)
        lista = lista + [item]
        return lista
    
    """
    note: metodo que acumula los hijos, nietos etc. de un item en una lista incluyendose al item
    """
    def setNombre(self, nombre):
        self.nombre= nombre
    
    def setNumeroTipoItem(self, numeroTipoItem):
        self.numeroTipoItem= numeroTipoItem
    
    def setVersion(self, version):
        self.version= version
    
    def setComplejidad(self, complejidad):
        self.complejidad= complejidad
    
    def setDescripcion(self, descripcion):
        self.descripcion= descripcion
    
    def setMarcar(self):
        self.marcado= 'Si'
    
    def setDesMarcar(self):
        self.marcado= 'No'
    
    def getRelacionArchivos(self):
        return self.relacionArchivo
    """
    note: metodo que acumula en una lista los padres, abuelos etc de un item incluyendose a el
    """
    def getAscendientes(self, fase):
        lista= []
        item_aux= self
        while item_aux.tienePadre(fase):
            lista.append(item_aux.getItemPadre())
            item_aux= item_aux.getItemPadre()
        lista = lista + [self]
        return lista
    
    def getAntecesoresParaLb(self, fase):
        proyecto= Proyecto.query.filter_by(id=fase.proyecto_id).first()
        #proyecto.fases.sort(comparaFase)
        ubicacion= fase.numero_fase
        lista= []
        if ubicacion > 1:
            """ note: copia las relaciones que estan en la fase anterior """
            faseAnterior= proyecto.fases[ubicacion-1]
            for candidato in faseAnterior.items:
                for relacion in candidato.relacionSucesor:
                    if relacion.item == self and candidato.getEstado() != 'eliminado':
                        lista.append(candidato)
        return lista
    
    def inicializarAtributos(self):
        tipoItemElegido = TipoItem.query.filter_by(id=self.tipoItem_id).first()
        for atributo in tipoItemElegido.atributoPorTipoItem:
            nuevoAtributo = Atributo()
            nuevoAtributo.nombre = atributo.nombre
            nuevoAtributo.tipo = atributo.tipo
            nuevoAtributo.setValor(atributo.getValor())
            nuevoAtributo.descripcion = atributo.descripcion
            self.atributos.append(nuevoAtributo)
    
    def todosYaVotaron(self):
        solicitudes = Solicitud.query.filter_by(item_id=self.id).order_by("id asc")
        for solicitud in solicitudes:
            if solicitud.getEstado()=='no votado':
                return False
        return True
    
    def contarVotos(self):
        aprobado=0
        rechazado=0
        solicitudes = Solicitud.query.filter_by(item_id=self.id).order_by("id asc")
        for solicitud in solicitudes:
            if solicitud.getVoto()=='aprobado':
                aprobado+=1
            if solicitud.getVoto()=='rechazado':
                rechazado+=1
            solicitud.setEstado(2) #Estado Finalizado
            self.solicitudes.append(solicitud)
        
        if aprobado > rechazado:
            return 'aprobado'
        else:
            return 'rechazado'
        

class Atributo(db.Model):
    
    __tablename__ = 'atributo'
    
    id = Column(db.Integer, primary_key=True)
    nombre= Column(db.String(32), nullable=False)
    tipo= Column(db.Integer)
    descripcion= Column(db.String(100), nullable=True)
    valorString= Column(db.String(32))
    valorInteger= Column(db.Integer)
    valorFecha=  Column(db.DateTime)
    
# FUNCIONES =======================================================================

    def getNombre(self):
        return self.nombre
    
    def getTipo(self):
        return TIPOS_ATRIBUTOS[self.tipo]
    
    def getValor(self):
        if self.getTipo() == 'String':
            return self.valorString
        elif self.getTipo() == 'Integer':
            return self.valorInteger
        else:
            if self.valorFecha != None:
                return self.valorFecha.strftime("%d-%m-%Y")
            else:
                return 'No existe fecha'
    
    def getDescripcion(self):
        return self.descripcion
    
    def setNombre(self, nombre):
        self.nombre= nombre
    
    def setValor(self, valor):
        if self.getTipo() == 'String':
            self.valorString= valor
        if self.getTipo() == 'Integer':
            self.valorInteger= int(valor)
        if self.getTipo() == 'Date':
            valor= valor.split('-')
            valorDiccionario= {}
            valorDiccionario['anho']= int(valor[2])
            valorDiccionario['mes']= int(valor[1])
            valorDiccionario['dia']= int(valor[0])
            self.valorFecha= date(valorDiccionario['anho'], valorDiccionario['mes'], valorDiccionario['dia'])
    def setDescripcion(self, descripcion):
        self.descripcion= descripcion
              
    
class Permiso(db.Model):

    __tablename__ = 'permiso'

    id = Column(db.Integer, primary_key=True)
    nombre = Column(db.String(50), nullable=False, unique=True)
    descripcion = Column(db.String)

# FUNCIONES ================================================================
    def getNombre(self):
        return self.nombre
    
    def getDescripcion(self):
        return self.descripcion
    
    def setNombre(self, nombre):
        self.nombre= nombre
    
    def setDescripcion(self, descripcion):
        self.descripcion= descripcion


class Archivo(db.Model):
    __tablename__ = 'archivo'
    
    id = Column(db.Integer, primary_key=True)
    valor= Column(db.LargeBinary)
    tipoArchivo= Column(db.String(100))
    nombreArchivo= Column(db.String(100))
    
    def setArchivo(self, valor):
        self.valor= valor
    
    def setTipoArchivo(self, valor):
        self.tipoArchivo= valor
    
    def setNombreArchivo(self, valor):
        self.nombreArchivo= valor
    
    def getArchivo(self):
        return self.valor
    
    def getTipoArchivo(self):
        return self.tipoArchivo
    
    def getNombreArchivo(self):
        return self.nombreArchivo
    
    
class HistorialItem(db.Model):
    __tablename__ = 'historialItem'

    id = Column(db.Integer, primary_key=True)
    itemId= Column(db.Integer, nullable=False)
    descripcion = Column(db.String)
    fecha= Column(db.DateTime, default=get_current_time)

    
class LineaBase(db.Model):
    __tablename__='lineaBase'
    
    id = Column(db.Integer, primary_key=True)
    numero_lb = Column(db.Integer)
    nombre = Column(db.String(25), nullable=False)
    estado_id = Column(db.SmallInteger,default=ABIERTA)   
    complejidad = Column(db.Integer)
    
# RELACIONES ===================================================================
    # Many-to-One relationship
    fase_id = Column(db.Integer, db.ForeignKey('fase.id'))
    # One-to-many relationship 
    items = db.relationship('Item', backref='lineaBase',lazy='dynamic')
    
 # FUNCIONES =====================================================================    

    def getNombre(self):
        return self.nombre
    
    def getNumero(self):
        return self.numero_lb
    
    def getEstado(self):
        return LINEABASE_ESTADOS[self.estado_id]
    
    def getComplejidad(self):
        cont= 0
        for item in self.items:
            cont= cont + item.getComplejidad()
        return cont
    
    def setComplejidad(self, nro):
        self.complejidad=nro
    
    def actualizarComplejidad(self):
        cant=0
        for item in self.items:
            cant=cant + item.getComplejidad()
            self.complejidad=cant    
        
    
    def getNroItems(self):
        cant = 0
        for item in self.items:
            cant=cant + 1
        return  cant#len(self.items)
    
    def getItems(self):
        lista= []
        for aux in self.items:
            lista.append(aux)
        return lista
    
    def setNombre(self, nombre):
        self.nombre= nombre
    
    def setNumero(self, numero):
        self.numero_lb = numero
    
    def setEstado(self, estado_id):
        self.estado_id = estado_id
    
    def romper(self):
        self.estado_id = 'Abierta'
        for item in self.items:
            item.setEstado('para revision')
    
    def comprometer(self, session):
        self.estado_id = 'comprometida'
        for item in self.items:
            item.setEstado('revision')
        session.add(self)
    
    def removerItemsEliminados(self, session):
        for item in self.items:
            if item.getEstado() == 'eliminado':
                self.items.remove(item)
        session.add(self)
    
    def removerItemsDesVersionados(self, session, fase):
        for item in self.items:
            if not (item in fase.items):
                self.items.remove(item)
        session.add(self)
    
    def estaVacia(self):
        lista= []
        cont = 0
        for item in self.items:
            if item != None:
                print str(cont) +' : '+ str(self.getNombre())
                cont = cont + 1
                lista.append(item)
        if lista == []:
            return True
        else:
            return False
    
    def estaEnLineaBase(self, item):
        return item in self.items
    
    def actualizarLineaBase(self, session, item, nuevaVersion):
        #self.items.sort(compara)
        for aux in self.items:
            print str(aux.id)+ " : "+ str(aux.getNombre())+" : "+ str(aux.getNumero())
        
        indice= self.items.index(item)
        self.items.insert(indice, nuevaVersion)
        
        for aux in self.items:
            print str(aux.id)+ " : "+str(aux.getNombre()) +" : "+ str(aux.getNumero())
        
        #session.add(self)
        self.items.remove(item)
        #self.reEnumerarItems()
        #self.reEnumerarItemsPorTipo()
        
        for aux in self.items:
            print str(aux.id)+ " : "+str(aux.getNombre()) +" : "+str(aux.getNumero())
        
        session.add(self)
    
    def imprimirItems(self):
        for aux in self.items:
            if aux != None:
                print "\n"
                print aux.getNombre()
                print "\n"
            else:
                print "\n"
                print "Es None..."
                print "\n"

class HistorialLineaBase(db.Model):

    __tablename__ = 'historialLB'

    id = Column(db.Integer, primary_key=True)
    lineaBase_id = Column(db.Integer, nullable=False)
    descripcion = Column(db.String(200))
    fecha = Column(db.DateTime, default=get_current_time)


class Solicitud(db.Model):
    __tablename__ = 'solicitud'
    
    id = Column(db.Integer, primary_key=True)
    estado = Column(db.SmallInteger, default=NO_VOTADO)
    voto = Column(db.SmallInteger, default=NO_VOTADO)
    solicitante = Column(db.Integer, nullable=True)
    
# RELACIONES ===============================================================================
    # Many-to-one relationship
    comite_id = Column(db.Integer, db.ForeignKey('comite.id'))
    item_id = Column(db.Integer, db.ForeignKey('item.id'))

    def setEstado(self, estado):
        self.estado = estado
    
    def setVoto(self, voto):
        self.voto = voto
    
    def setSolicitante(self, solicitante):
        self.solicitante = solicitante
    
    def getVoto(self):
        return VOTACION_ESTADOS[self.voto]
    
    def getEstado(self):
        return SOLICITUD_ESTADOS[self.estado]
    
    def getSolicitante(self):
        return self.solicitante
    
    def getItem(self):
        return Item.query.filter_by(id=self.item_id).first_or_404()
    
    def getProyecto(self):
        comite = Comite.query.filter_by(id=self.comite_id).first_or_404()
        return comite.getProyecto()

class Comite(db.Model):
    
    __tablename__ = 'comite'

    id = Column(db.Integer, primary_key=True)
    nombre = Column(db.String(32), nullable=False, unique=True)
    descripcion = Column(db.String)

# RELACIONES ========================================================================
    # One-to-one
    proyecto_id = Column(db.Integer, db.ForeignKey("proyecto.id"), nullable=True)
    # One-to-many
    solicitudes = db.relationship('Solicitud', backref='comite',lazy='dynamic')
    #many-to-many
    usuarioPorComite = db.relationship('User', secondary=usuarioPorComite,
        backref=db.backref('comites', lazy='dynamic')) 
    

# FUNCIONES ================================================================
    
    def getProyecto(self):
        proyecto = Proyecto.query.filter_by(id=self.proyecto_id).first_or_404()
        return proyecto
    
    def getProyectoNombre(self):
        proyecto = self.getProyecto()
        return proyecto.nombre
    
    def getSolicitudes(self):
        return self.solicitudes
    
    def getItems(self):
        listaItems = []
        last_id = 0
        solicitudes = self.solicitudes.order_by("id asc")
        for solicitud in solicitudes:
            if solicitud.item_id != last_id:
                item = Item.query.filter_by(id=solicitud.item_id).first_or_404()
                listaItems.append(item)
                last_id = item.id
        return listaItems
    
    # Class methods

    @classmethod
    def search(cls, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(
                Comite.nombre.ilike(keyword)
            ))
        q = reduce(db.and_, criteria)
        return cls.query.filter(q)

class ItemPorProyectoReporte(Report):
    title = 'Lista de Items de Proyecto'
    
    #cuerpo que muestra los datos en si 
    class band_detail(DetailBand):
        height = 0.7 * cm
        elements = [
            ObjectValue(expression='id', left=1.5 * cm),
            ObjectValue(expression='nombre', left=3 * cm),
            ObjectValue(expression='estado', left=5.5 * cm),
        ]
        borders = {'bottom': True}
    #cabecera pagina
    class band_page_header(ReportBand):
        height = 1.3 * cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1 * cm, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            SystemField(expression=u'Pagina %(page_number)d de %(page_count)d', top=0.1 * cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            Label(text="ID", top=0.8 * cm, left=1.5 * cm),
            Label(text="Nombre", top=0.8 * cm, left=3 * cm),
            Label(text="Estado", top=0.8 * cm, left=5.5 * cm),
        ]
        borders = {'all': True}
    #Pie de pagina    
    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Sistema GPM', top=0.1*cm),
            SystemField(expression='Impreso %(now:%b %d, %Y)s a las %(now:%H:%M)s', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'top': True}
     
    groups = [
        ReportGroup(
            attribute_name='fase',
            band_header=DetailBand(
                height=0.6*cm,
                elements=[
                    ObjectValue(expression='fase', style={'fontName': 'Helvetica-Bold','fontSize': 12})
                ]
            ),
        ),
    ]

class HistorialPorItemReporte(Report):
    title = 'Historial de Item'
    
    #cuerpo que muestra los datos en si 
    class band_detail(DetailBand):
        height = 1.3 * cm
        elements = [
            ObjectValue(expression='id', left=1.5 * cm),
            ObjectValue(expression='descripcion', left=2.5 * cm),
            ObjectValue(expression='fecha', left=12.5 * cm),
        ]
        borders = {'bottom': True}
    #cabecera pagina
    class band_page_header(ReportBand):
        height = 1.3 * cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1 * cm, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            SystemField(expression=u'Pagina %(page_number)d de %(page_count)d', top=0.1 * cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            Label(text="ID", top=0.8 * cm, left=1.5 * cm),
            Label(text="Descripcion", top=0.8 * cm, left=2.5 * cm),
            Label(text="Fecha", top=0.8 * cm, left=12.5 * cm),
        ]
        borders = {'all': True}
    #Pie de pagina    
    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Sistema GPM', top=0.1*cm),
            SystemField(expression='Impreso %(now:%b %d, %Y)s a las %(now:%H:%M)s', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'top': True}


