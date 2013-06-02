# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
try:
    from sqlalchemy.ext.mutable import Mutable
except ImportError:
    from sqlalchemy.types import MutableType as Mutable
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin

from ..extensions import db
from ..utils import get_current_time
from .constants import USER, USER_ROLE, ADMIN, INACTIVE, USER_STATUS,NO_INICIADO, PROYECTO_ESTADOS, LINEABASE_ESTADOS
from .constants import INICIAL

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

atributoPorTipoItem = db.Table('atributoPorTipoItem',
    Column('tipoItem_id', db.Integer, db.ForeignKey('tipoItem.id')),
    Column('atributo_id', db.Integer, db.ForeignKey('atributo.id'))
)


solicitudPorUsuario = db.Table('solicitudPorUsuario',
    Column('user_id', db.Integer, db.ForeignKey('users.id')),
    Column('solicitud_id', db.Integer, db.ForeignKey('solicitud.id'))
)

class Rol(db.Model):

    __tablename__ = 'rol'

    id = Column(db.Integer, primary_key=True)
    nombre = Column(db.String(32), nullable=False, unique=True)
    descripcion = Column(db.String)
    permisoPorRol = db.relationship('Permiso', secondary=permisoPorRol,
        backref=db.backref('permisoPorRol', lazy='dynamic'))
    
    # =========================
    # One-to-many relationship
    proyecto_id = Column(db.Integer, db.ForeignKey('proyecto.id'))

    # ================================================================
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

class Fase(db.Model):
    __tablename__='fase'
    
    id = Column(db.Integer, primary_key=True)
    nombre = Column(db.String(32), nullable=False, unique=True)
    descripcion = Column(db.String(),nullable=True)
    numero_fase = Column(db.Integer,nullable=True)
    numero_items = Column(db.Integer,default=0)
    numero_lb = Column(db.Integer,default=0)
    
    # =========================
    # One-to-many relationship
    estado = Column(db.SmallInteger,default=INICIAL)
    # =========================
    # One-to-many relationship
    proyecto_id = Column(db.Integer, db.ForeignKey('proyecto.id'))
    
    # One-to-many relationship between fases and lineas base
    lineaBase = db.relationship('LineaBase', backref='fase',lazy='dynamic')
    
    
class Comite(db.Model):
    
    __tablename__ = 'comite'

    id = Column(db.Integer, primary_key=True)
    nombre = Column(db.String(32), nullable=False, unique=True)
    descripcion = Column(db.String)

    # One-to-one (uselist=False) relationship between proyecto and comite.  
    proyecto_id = Column(db.Integer, db.ForeignKey("proyecto.id"), nullable=True)
    
    usuarioPorComite = db.relationship('User', secondary=usuarioPorComite,
        backref=db.backref('comites', lazy='dynamic')) 
    
    solicitudes = db.relationship('Solicitud', backref='comite',lazy='dynamic')
    
    
    # ================================================================
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

    
class Permiso(db.Model):

    __tablename__ = 'permiso'

    id = Column(db.Integer, primary_key=True)
    nombre = Column(db.String(50), nullable=False, unique=True)
    descripcion = Column(db.String)
    
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

    # ================================================================
    # Avatar
    avatar = Column(db.String)

    # ================================================================
    # Password
    _password = Column('password', db.String, nullable=False)

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
        

    # ================================================================
    # Many-to-many relationship between users and roles.
    
    rolPorUsuario = db.relationship('Rol', secondary=rolPorUsuario,
       backref=db.backref('users', lazy='dinamic'))
    
    solicitudPorUsuario = db.relationship('Solicitud', secondary=solicitudPorUsuario,
       backref=db.backref('users', lazy='dinamic'))
    
    role_id = Column(db.SmallInteger, default=USER)
    

    def comprobarPermiso (self, key):
        roles = self.rolPorUsuario
        for item in roles: 
            rol=Rol.query.filter_by(id=item.id).first_or_404()
            permisos=rol.permisoPorRol
            for permiso in permisos:
                if permiso.nombre==key:
                    return True          
        return False
    
    
    def getProyectos (self):
        todosProyectos = Proyecto.query.all()
        
        misProyectos=[]
        for proyecto in todosProyectos:
            #misProyectos.append(proyecto.nombre)
            unProyecto=Proyecto.query.filter_by(id=proyecto.id).first_or_404()
            miembros=unProyecto.usuarioPorProyecto
            for miembro in miembros:
                if self.id==miembro.id:
                    misProyectos.append(unProyecto)
        return misProyectos
        
    def getCantSolicitudes (self):
        listaSolicitudes = self.solicitudPorUsuario
        return len(listaSolicitudes)
    
    def getSolicitudes (self):
        listaSolicitudes = self.solicitudPorUsuario
        listaItem=[]
        for solicitud in listaSolicitudes:
            item = Item.query.filter_by(id = solicitud.item_id).first_or_404()
            print '#############################33'
            print item.nombre
            listaItem.append(item)
        return listaItem    
    
                   
   
    
        
        
            
    def getRole(self):
        return USER_ROLE[self.role_id]

    def is_admin(self):
        return self.role_id == ADMIN

    # ================================================================
    # One-to-many relationship between users and user_statuses.
    status_id = Column(db.SmallInteger, default=INACTIVE)

    def getStatus(self):
        return USER_STATUS[self.status_id]

    # ================================================================
    # One-to-one (uselist=False) relationship between users and user_details.
#    user_detail_id = Column(db.Integer, db.ForeignKey("user_details.id"))
#    user_detail = db.relationship("UserDetail", uselist=False, backref="user")

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

#class Lista(object):
#    comite = {"item": Item, "Bar":Proyecto}
    



class Proyecto(db.Model):

    __tablename__ = 'proyecto'

    id = Column(db.Integer, primary_key=True)
    nombre = Column(db.String(32), nullable=False, unique=True)
    descripcion = Column(db.String(200), nullable=True)
    complejidad_total = Column(db.Integer, nullable=False, default=0)
    numero_fases = Column(db.Integer, nullable=False)
    created_time = Column(db.DateTime, default=get_current_time)
    lider_proyecto = Column(db.Integer(), nullable=True)

    usuarioPorProyecto = db.relationship('User', secondary=usuarioPorProyecto,
                                         backref=db.backref('usuarioPorProyecto', lazy='dynamic'))  
    
    # One-to-one relationship between comite and proyecto 
    comite = db.relationship('Comite', backref='proyecto', uselist=False)
    
    # One-to-many relationship between proyecto and fases
    fases = db.relationship('Fase', backref='proyecto',lazy='dynamic')
    
    # One-to-many relationship between proyecto and roles
    roles = db.relationship('Rol', backref='proyecto',lazy='dynamic')
    
    # One-to-many relationship between proyecto and tipoItem
    tiposItem = db.relationship('TipoItem', backref='proyecto',lazy='dynamic')
    
    # One-to-many relationship between proyecto and fases
    items = db.relationship('Item', backref='proyecto',lazy='dynamic')
    
    
    # ================================================================
    # One-to-many relationship betwee    n projects and project_statuses.
    estado_id = Column(db.SmallInteger, default=NO_INICIADO)

    def getStatus(self):
        return PROYECTO_ESTADOS[self.estado_id]

    # ================================================================
    # Follow / Following
    followers = Column(DenormalizedText)
    following = Column(DenormalizedText)

    def getTodosProyectos(self):
        todosProyectos = Proyecto.query.filter(Proyecto.id != self.id)
        return todosProyectos
   

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
    
class TipoItem(db.Model):
    
    __tablename__ = 'tipoItem'
    
    id = Column(db.Integer, primary_key=True)
    nombre= Column(db.String(32), nullable=False)
    descripcion= Column(db.String(200), nullable=True)
    proyecto_id = Column(db.Integer, db.ForeignKey('proyecto.id'))


    atributoPorTipoItem = db.relationship('Atributo', secondary=atributoPorTipoItem,
        backref=db.backref('atributoPorTipoItem', lazy='dynamic'))
    
    
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

class HistorialItem(db.Model):

    __tablename__ = 'historialItem'

    id = Column(db.Integer, primary_key=True)
    itemId= Column(db.Integer, nullable=False)
    descripcion = Column(db.String)
    fecha= Column(db.DateTime, default=get_current_time)

class Item(db.Model):
    __tablename__='item'
    
    id = Column(db.Integer, primary_key=True)
    nombre = Column(db.String(32), nullable=False, unique=True)
    descripcion = Column(db.String(),nullable=True)
    version = Column(db.Integer)
    complejidad= Column(db.Integer)
    
    # Estado del item 
    estado = Column(db.SmallInteger,default=INICIAL)
    
    # Relacion del item por proyecto
    proyecto_id = Column(db.Integer, db.ForeignKey('proyecto.id'))
    
    #Relacion del item con su tipo de Item
    tipoItem_id= Column(db.Integer, db.ForeignKey('tipoItem.id'), nullable=True)
    
    #Relacion del item con una solicitud de cambio
    solicitudes = db.relationship('Solicitud', backref='item',lazy='dynamic')
    
    #Relacion del item con su linea base
    lineaBase_id = Column(db.Integer, db.ForeignKey('lineaBase.id'))
    
    """
    Colummnas para relaciones de versiones de items
    """
    versionSuperior_id = Column(db.Integer, ForeignKey('item.id'))
    versionAnterior = relationship('Item')
    
    """
    Relacion con el item sucesor
    """
    relacionSucesor= relationship('RelacionSucesor', primaryjoin=id==RelacionSucesor.left_id, backref='items')
    
    relacionHijo= relationship('RelacionHijo', primaryjoin=id==RelacionHijo.left_id, backref='item')
    
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
    
    def tienePadre(self, fase):
        for item in fase.items:
            if item.getEstado() != 'Eliminado' and item != self:
                for relacion in item.relacionHijo:
                    if relacion.hijo == self:
                        return True
        return False
    
    """
    note: metodo que devuelve el padre del item, devuelve None en caso de no tener
    """
#    def getPadre(self, fase):
#        for item in fase.items:
#            if item.getEstado() != 'Eliminado' and item != self:
#                for relacion in item.relacionHijo:
#                    if relacion.hijo == self:
#                        return item
#        return None
#    
    """
    note metodo que pregunta si un item es descendiente de otro en una fase dada
    """
#    def esDescendiente(self, fase, item):
#        lista_hijos= self.getGeneraciones(fase, self)
#        print "\n\n\n\n\n\n\n"
#        for aux in lista_hijos:
#            print aux.getNombre()
#        print "\n\n\n\n\n\n\n"
#        return item in lista_hijos


    

class RelacionSucesor(db.Model):
    __tablename__ = 'relacion_sucesor'
    left_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship('Item', primaryjoin="Item.id==RelacionSucesor.right_id", backref='relacion_sucesor')
    

class RelacionHijo(db.Model):
    __tablename__ = 'relacion_hijo'
    left_id = Column(db.Integer, ForeignKey('item.id'), primary_key=True)
    right_id = Column(db.Integer, ForeignKey('item.id'), primary_key=True)
    hijo = relationship('Item', primaryjoin="Item.id==RelacionHijo.right_id", backref='relacion_hijo')
    

class Atributo(db.Model):
    
    __tablename__ = 'atributo'
    
    id = Column(db.Integer, primary_key=True)
    nombre= Column(db.String(32), nullable=False, unique=True)
    tipo= Column(db.Integer)
    descripcion= Column(db.String(200), nullable=True)
    valorString= Column(db.String(32))
    valorInteger= Column(db.Integer)
    valorFecha=  Column(db.DateTime)
    

class LineaBase(db.Model):
    __tablename__='lineaBase'
    
    id = Column(db.Integer, primary_key=True)
    numero_lb = Column(db.Integer, nullable=False)
    descripcion = Column(db.String(),nullable=True)
    
    # =========================
    # One-to-many relationship
    estado = Column(db.SmallInteger,default=INICIAL)
    # =========================
    # One-to-many relationship between proyecto and fases
    items = db.relationship('Item', backref='lineaBase',lazy='dynamic')
    
    fase_id = Column(db.Integer, db.ForeignKey('fase.id'))
    
    def getStatus(self):
        return LINEABASE_ESTADOS[self.estado]

class HistorialLineaBase(db.Model):

    __tablename__ = 'historialLB'

    id = Column(db.Integer, primary_key=True)
    lineaBase_id = Column(db.Integer, nullable=False)
    descripcion = Column(db.String(200))
    fecha = Column(db.DateTime, default=get_current_time)

class Solicitud(db.Model):
    __tablemame__ = 'solicitud'
    
    id = Column(db.Integer, primary_key=True)
    comite_id = Column(db.Integer, db.ForeignKey('comite.id'))
    item_id = Column(db.Integer, db.ForeignKey('item.id'))
    estado = Column(db.SmallInteger, default=NO_INICIADO)
    si = Column(db.Integer, nullable=False, default=0)
    no = Column(db.Integer, nullable=False, default=0)
    

