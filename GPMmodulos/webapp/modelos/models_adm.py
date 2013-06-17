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
from .constants import INACTIVE, USER_STATUS,NO_INICIADO, PROYECTO_ESTADOS, LINEABASE_ESTADOS, FASE_ESTADOS
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

rolPorProyecto = db.Table('rolPorProyecto',
    Column('rol_id', db.Integer, db.ForeignKey('rol.id')),
    Column('proyecto_id', db.Integer, db.ForeignKey('proyecto.id'))
)
############################################################################################
#            Agregado de Adolfismo
############################################################################################

archivoPorItem = db.Table('asociacion_item_archivo',
    Column('item_id', db.Integer, db.ForeignKey('item.id')),
    Column('archivo_id', db.Integer, db.ForeignKey('archivo.id'))
)

relacion_sucesor = db.Table('relacion_sucesor',
    Column('item1_id', db.Integer, db.ForeignKey('item.id')),
    Column('item2_id', db.Integer, db.ForeignKey('item.id')),
   # item = relationship('Item', primaryjoin="Item.id==RelacionSucesor.right_id", backref='relacion_sucesor')
    Column('datos', db.String(50))
)

relacion_hijo = db.Table('relacion_hijo',
    Column('item1_id', db.Integer, db.ForeignKey('item.id')),
    Column('item2_id', db.Integer, db.ForeignKey('item.id')),
    Column('datos', db.String(50))
# hijo = relationship('Item', primaryjoin="Item.id==RelacionHijo.right_id", backref='relacion_hijo')
)

##############################################################################################
##############################################################################################

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
        
    def getCantSolicitudes (self):
        listaSolicitudes = self.solicitudPorUsuario
        return len(listaSolicitudes)
    
    def getSolicitudes (self):
        listaSolicitudes = self.solicitudPorUsuario
        listaItem=[]
        for solicitud in listaSolicitudes:
            item = Item.query.filter_by(id = solicitud.item_id).first_or_404()
            listaItem.append(item)
        return listaItem

    def getStatus(self):
        return USER_STATUS[self.status_id]

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
    descripcion = Column(db.String)
    
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

    def getNombre(self):
        return self.nombre
    
    def getDescripcion(self):
        return self.descripcion
    
    def getComplejidad(self):
        return self.complejidad_total
    
    def getEstado(self):
        return PROYECTO_ESTADOS[self.estado_id]
    
    def getNroFases(self):
        return self.numero_fases
    
    def getFases(self):
        return self.fases
    
    def setNombre(self, nombre):
        self.nombre= nombre
    
    def setDescripcion(self, descripcion):
        self.descripcion= descripcion

    def getTodosProyectos(self):
        todosProyectos = Proyecto.query.filter(Proyecto.id != self.id)
        return todosProyectos
   
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
    nombre = Column(db.String(32), nullable=False, unique=True)
    descripcion = Column(db.String(),nullable=True)
    numero_fase = Column(db.Integer,nullable=True)
    numero_lb = Column(db.Integer,default=0)
    estado_id = Column(db.SmallInteger,default=INICIAL)
    
# RELACIONES =================================================================
    # Many-to-one relationship
    proyecto_id = Column(db.Integer, db.ForeignKey('proyecto.id'))
    # One-to-many relationship
    lineaBase = db.relationship('LineaBase', backref='fase',lazy='dynamic')
    items = db.relationship('Item', backref='fase',lazy='dynamic')
    
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
        return len(self.numero_lb)
    
    def setNombre(self, nombre):
        self.nombre= nombre
    
    def setDescripcion(self, descripcion):
        self.descripcion= descripcion
    
    def setNroLB(self, cantidad):
        self.numero_lb= cantidad
    
    def getItems (self, proyecto_id):
        misItems = self.items
        return misItems
    
    
class TipoItem(db.Model):
    
    __tablename__ = 'tipoItem'
    
    id = Column(db.Integer, primary_key=True)
    nombre= Column(db.String(32), nullable=False)
    descripcion= Column(db.String(200), nullable=True)
    proyecto_id = Column(db.Integer, db.ForeignKey('proyecto.id'))

# RELACIONES  ===========================================================================
    atributoPorTipoItem = db.relationship('Atributo', secondary=atributoPorTipoItem,
        backref=db.backref('atributoPorTipoItem', lazy='dynamic'))
    
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
    complejidad= Column(db.Integer) 
    estado_id = Column(db.SmallInteger,default=INICIAL)
    
# RELACIONES  ====================================================================
    proyecto_id = Column(db.Integer, db.ForeignKey('proyecto.id'))
    fase_id = Column(db.Integer, db.ForeignKey('fase.id')) 
    solicitudes = db.relationship('Solicitud', backref='item',lazy='dynamic')
    lineaBase_id = Column(db.Integer, db.ForeignKey('lineaBase.id'))
    """
    estas dos columnas son para relacionar muchos items con un tipo de item
    """
    tipoItem_id= Column(db.Integer, db.ForeignKey('tipoItem.id'), nullable=True)
    tipoItem = db.relationship("TipoItem", backref='item', lazy='dynamic')
#    atributos= db.relationship('Atributo', backref='item',lazy='dynamic')
    archivoPorItem= db.relationship('Archivo', secondary=archivoPorItem,
       backref=db.backref('archivo', lazy='dynamic'))
    """
    estas dos columnas son para relaciones de versiones de items
    """
    versionSuperior_id = Column(db.Integer, db.ForeignKey('item.id'))
    versionAnterior = db.relationship("Item")
    """
    relacion con el item sucesor
    """
#    relacionSucesor= relationship("RelacionSucesor", primaryjoin=id==RelacionSucesor.left_id, backref='items')
#    
#    relacionHijo= relationship("RelacionHijo", primaryjoin=id==RelacionHijo.left_id, backref='item')


# FUNCIONES  ====================================================================   
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
        return self.estado
    
    def getComplejidad(self):
        return self.complejidad
    
    def getDescripcion(self):
        return self.descripcion
    
    def marcarRevision(self):
        self.estado= 'Revision'
    
    def tieneLineaBase(self):
        if self.lineaBase_id != None:
            return True
        else:
            return False
    
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
            if item.getEstado() != 'Eliminado' and item != self:
                for relacion in item.relacionHijo:
                    if relacion.hijo == self:
                        return True
        return False
    
    """
    note: metodo que devuelve el padre del item, devuelve None en caso de no tener
    """
    def getPadre(self, fase):
        for item in fase.items:
            if item.getEstado() != 'Eliminado' and item != self:
                for relacion in item.relacionHijo:
                    if relacion.hijo == self:
                        return item
        return None
    
    """
    note metodo que pregunta si un item es descendiente de otro en una fase dada
    """
    def esDescendiente(self, fase, item):
        lista_hijos= self.getGeneraciones(fase, self)
        print "\n\n\n\n\n\n\n"
        for aux in lista_hijos:
            print aux.getNombre()
        print "\n\n\n\n\n\n\n"
        return item in lista_hijos
    
    """
    note: metodo que acumula los hijos, nietos etc. de un item en una lista incluyendose al item
    """
#    def getGeneraciones(self, fase, item):
#        lista= []
#        for relacion in item.relacionHijo:
#            if relacion.hijo.getEstado() != 'Eliminado' and relacion.hijo in fase.items:
#                lista= lista + item.getGeneraciones(fase, relacion.hijo)
#        lista = lista + [item]
#        return lista
#    
#    """
#    note: metodo que acumula en una lista los padres, abuelos etc de un item incluyendose a el
#    """
#    def getAscendientes(self, fase):
#        lista= []
#        item_aux= self
#        while item_aux.tienePadre(fase):
#            lista.append(item_aux.getPadre(fase))
#            item_aux= item_aux.getPadre(fase)
#        lista = lista + [self]
#        return lista
#    
#    """
#    note: metodo que acumula los sucesores de un item en una lista incluyendose al item, pueden existir repetidos
#    """
#    def getSucesores(self, session, fase, item):
#        lista= []
#        proyecto= session.query(Proyecto).filter_by(id= fase.proyecto_id).first()
#        proyecto.fases.sort(comparaFase)
#        ubicacion= proyecto.fases.index(fase)
#        lista_hijos= item.getGeneraciones(fase, item)
#        for aux in lista_hijos:
#            for relacion in aux.relacionSucesor:
#                fase= proyecto.fases[ubicacion + 1]
#                if relacion.item.getEstado() != 'Eliminado' and relacion.item in fase.items:
#                    lista= lista + item.getSucesores(session, fase, relacion.item)
#            lista = lista + [aux]
#        return lista
#    
#    def getAntecesores(self, session, fase, item):
#        lista= []
#        proyecto= session.query(Proyecto).filter_by(id= fase.proyecto_id).first()
#        proyecto.fases.sort(comparaFase)
#        ubicacion= proyecto.fases.index(fase)
#        lista= item.getAscendientes(fase)
#        if ubicacion > 0:
#            listaAdd= []
#            faseAnterior= proyecto.fases[ubicacion-1]
#            for aux in lista:
#                for candidato in faseAnterior.items:
#                    for relacion in candidato.relacionSucesor:
#                        if relacion.item == aux and candidato.getEstado() != 'Eliminado':
#                            listaAdd= listaAdd + item.getAntecesores(session, faseAnterior, candidato)
#            lista = lista + listaAdd
#        return lista
#    
#    def getSucesoresParaLb(self, session, fase):
#        proyecto= session.query(Proyecto).filter_by(id= fase.proyecto_id).first()
#        proyecto.fases.sort(comparaFase)
#        ubicacion= proyecto.fases.index(fase)
#        lista= []
#        if ubicacion < (len(proyecto.fases)-1):
#            """ note: copia las relaciones que estan en la fase posterior """
#            fasePosterior= proyecto.fases[ubicacion+1]
#            for relacion in self.relacionSucesor:
#                if relacion.item.getEstado() != 'Eliminado' and (relacion.item in fasePosterior.items):
#                    lista.append(relacion.item)
#        return lista
#    
#    def getAntecesoresParaLb(self, session, fase):
#        proyecto= session.query(Proyecto).filter_by(id= fase.proyecto_id).first()
#        proyecto.fases.sort(comparaFase)
#        ubicacion= proyecto.fases.index(fase)
#        lista= []
#        if ubicacion > 0:
#            """ note: copia las relaciones que estan en la fase anterior """
#            faseAnterior= proyecto.fases[ubicacion-1]
#            for candidato in faseAnterior.items:
#                for relacion in candidato.relacionSucesor:
#                    if relacion.item == self and candidato.getEstado() != 'Eliminado':
#                        lista.append(candidato)
#        return lista
#    
#    def getMarcado(self):
#        return self.marcado
#    
    def setNombre(self, nombre):
        self.nombre= nombre
    
    def setNumeroTipoItem(self, numeroTipoItem):
        self.numeroTipoItem= numeroTipoItem
    
    def setVersion(self, version):
        self.version= version
    
    def setEstado(self, estado):
        self.estado= estado
    
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
    
#    def copiarAtributos(self, atributosImportados, relacionArchivos):
#        for atributoImportado in atributosImportados:
#            nuevoAtributo= Atributo(atributoImportado.getNombre(), atributoImportado.getTipo())
#            nuevoAtributo.setDescripcion(atributoImportado.getDescripcion())
#            nuevoAtributo.setValor(atributoImportado.getValor())
#            self.atributos.append(nuevoAtributo)
#        for relacion in relacionArchivos:
#            asociacion= AsociacionItemArchivo()
#            archivo= Archivo()
#            archivo.setArchivo(relacion.archivo.getArchivo())
#            archivo.setTipoArchivo(relacion.archivo.getTipoArchivo())
#            archivo.setNombreArchivo(relacion.archivo.getNombreArchivo())
#            asociacion.archivo= archivo
#            self.relacionArchivo.append(asociacion)
#    
#    def modificarAtributo(self, atributosImportados, atributo, nombre, descripcion, valor, relacionArchivos):
#        for atributoImportado in atributosImportados:
#            if atributoImportado != atributo:
#                nuevoAtributo= Atributo(atributoImportado.getNombre(), atributoImportado.getTipo())
#                nuevoAtributo.setDescripcion(atributoImportado.getDescripcion())
#                nuevoAtributo.setValor(atributoImportado.getValor())
#                self.atributos.append(nuevoAtributo)
#            else:
#                nuevoAtributo= Atributo(nombre, atributoImportado.getTipo())
#                nuevoAtributo.setDescripcion(descripcion)
#                nuevoAtributo.setValor(valor)
#                self.atributos.append(nuevoAtributo)
#        
#        for relacion in relacionArchivos:
#            asociacion= AsociacionItemArchivo()
#            archivo= Archivo()
#            archivo.setArchivo(relacion.archivo.getArchivo())
#            archivo.setTipoArchivo(relacion.archivo.getTipoArchivo())
#            archivo.setNombreArchivo(relacion.archivo.getNombreArchivo())
#            asociacion.archivo= archivo
#            self.relacionArchivo.append(asociacion)
#    
#    def copiarArchivos(self, relacionArchivos):
#        for relacion in relacionArchivos:
#            asociacion= AsociacionItemArchivo()
#            archivo= Archivo()
#            archivo.setArchivo(relacion.archivo.getArchivo())
#            archivo.setTipoArchivo(relacion.archivo.getTipoArchivo())
#            archivo.setNombreArchivo(relacion.archivo.getNombreArchivo())
#            asociacion.archivo= archivo
#            self.relacionArchivo.append(asociacion)
#    
#    def inicializarAtributos(self):
#        tipoItemElegido= self.tipoItem
#        for atributo in tipoItemElegido.atributos:
#            nuevoAtributo= Atributo(atributo.getNombre(), atributo.getTipo())
#            nuevoAtributo.setValor(atributo.getValor())
#            nuevoAtributo.setDescripcion(atributo.getDescripcion())
#            self.atributos.append(nuevoAtributo)
#    
#    def actualizarAtributos(self):
#        """
#        note: funcion que al agregar atributos al tipo de item actualiza 
#        a todos los items de ese tipo
#        """
#        tipoItemElegido= self.tipoItem
#        numeroDeAtributosItem= len(self.atributos)
#        numeroDeAtributosTipo= len(tipoItemElegido.atributos)
#        rango= numeroDeAtributosTipo - numeroDeAtributosItem
#        for indice in range(-rango, 0):
#            atributo= tipoItemElegido.atributos[indice]
#            nuevoAtributo= Atributo(atributo.getNombre(), atributo.getTipo())
#            nuevoAtributo.setValor(atributo.getValor())
#            nuevoAtributo.setDescripcion(atributo.getDescripcion())
#            self.atributos.append(nuevoAtributo)
#    
#    def copiarRelaciones(self, item, session):
#        fase= session.query(Fase).filter_by(id= item.fase_id).first()
#        proyecto= session.query(Proyecto).filter_by(id= fase.proyecto_id).first()
#        proyecto.fases.sort(comparaFase)
#        ubicacion= proyecto.fases.index(fase)
#        if ubicacion > 0:
#            """
#            note: copia las relaciones que estan en la fase anterior
#            """
#            faseAnterior= proyecto.fases[ubicacion-1]
#            for candidato in faseAnterior.items:
#                for relacion in candidato.relacionSucesor:
#                    if relacion.item == item and candidato.getEstado() != 'Eliminado':
#                        asociacion= RelacionSucesor()
#                        asociacion.item= self
#                        asociacion.left_id= candidato.id
#                        candidato.relacionSucesor.append(asociacion)
#                        session.add(candidato)
#        if ubicacion < (len(proyecto.fases)-1):
#            """
#            note: copia las relaciones que estan en la fase posterior
#            """
#            fasePosterior= proyecto.fases[ubicacion+1]
#            for relacion in item.relacionSucesor:
#                if relacion.item.getEstado() != 'Eliminado' and (relacion.item in fasePosterior.items):
#                    asociacion= RelacionSucesor()
#                    asociacion.item= relacion.item
#                    asociacion.left_id= self.id
#                    self.relacionSucesor.append(asociacion)
#        """
#        note: copia las relaciones de los padres al nuevo item
#        """
#        for candidato in fase.items:
#            for relacion in candidato.relacionHijo:
#                if relacion.hijo == item and candidato.getEstado() != 'Eliminado':
#                    asociacion= RelacionHijo()
#                    asociacion.hijo= self
#                    asociacion.left_id= candidato.id
#                    candidato.relacionHijo.append(asociacion)
#                    session.add(candidato)
#        """
#        note: copia las relaciones hijos al nuevo item
#        """
#        for relacion in item.relacionHijo:
#            if relacion.hijo.getEstado() != 'Eliminado' and (relacion.hijo in fase.items):
#                asociacion= RelacionHijo()
#                asociacion.hijo= relacion.hijo
#                asociacion.left_id= self.id
#                self.relacionHijo.append(asociacion)
#        return self
#    
#    def copiarRelacionesParaRevertir(self, item, numeroDeFase, session):
#        fase= session.query(Fase).filter_by(id= numeroDeFase).first()
#        proyecto= session.query(Proyecto).filter_by(id= fase.proyecto_id).first()
#        proyecto.fases.sort(comparaFase)
#        ubicacion= proyecto.fases.index(fase)
#        if ubicacion > 0:
#            """
#            note: copia las relaciones que estan en la fase anterior
#            """
#            faseAnterior= proyecto.fases[ubicacion-1]
#            for candidato in faseAnterior.items:
#                for relacion in candidato.relacionSucesor:
#                    if relacion.item == item and candidato.getEstado() != 'Eliminado':
#                        asociacion= RelacionSucesor()
#                        asociacion.item= self
#                        asociacion.left_id= candidato.id
#                        candidato.relacionSucesor.append(asociacion)
#                        session.add(candidato)
#        if ubicacion < (len(proyecto.fases)-1):
#            """
#            note: copia las relaciones que estan en la fase posterior
#            """
#            fasePosterior= proyecto.fases[ubicacion+1]
#            for relacion in item.relacionSucesor:
#                if relacion.item.getEstado() != 'Eliminado' and (relacion.item in fasePosterior.items):
#                    asociacion= RelacionSucesor()
#                    asociacion.item= relacion.item
#                    asociacion.left_id= self.id
#                    self.relacionSucesor.append(asociacion)
#        """
#        note: copia las relaciones de los padres al nuevo item
#        """
#        for candidato in fase.items:
#            for relacion in candidato.relacionHijo:
#                if relacion.hijo == item and candidato.getEstado() != 'Eliminado':
#                    asociacion= RelacionHijo()
#                    asociacion.hijo= self
#                    asociacion.left_id= candidato.id
#                    candidato.relacionHijo.append(asociacion)
#                    session.add(candidato)
#        """
#        note: copia las relaciones hijos al nuevo item
#        """
#        for relacion in item.relacionHijo:
#            if relacion.hijo.getEstado() != 'Eliminado' and (relacion.hijo in fase.items):
#                asociacion= RelacionHijo()
#                asociacion.hijo= relacion.hijo
#                asociacion.left_id= self.id
#                self.relacionHijo.append(asociacion)
#        return self

 
class Atributo(db.Model):
    
    __tablename__ = 'atributo'
    
    id = Column(db.Integer, primary_key=True)
    nombre= Column(db.String(32), nullable=False, unique=True)
    tipo= Column(db.Integer)
    descripcion= Column(db.String(200), nullable=True)
    valorString= Column(db.String(32))
    valorInteger= Column(db.Integer)
    valorFecha=  Column(db.DateTime)
    
# FUNCIONES =======================================================================

    def getNombre(self):
        return self.nombre
    
    def getTipo(self):
        return self.tipo
    
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
    numero_lb = Column(db.Integer, nullable=False)
    descripcion = Column(db.String(),nullable=True)
    estado_id = Column(db.SmallInteger,default=INICIAL)   
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
        return self.numero
    
    def getEstado(self):
        return LINEABASE_ESTADOS[self.estado_id]
    
    def getComplejidad(self):
        cont= 0
        for item in self.items:
            cont= cont + item.getComplejidad()
        return cont
    
    def getNroItems(self):
        return len(self.items)
    
    def getItems(self):
        lista= []
        for aux in self.items:
            lista.append(aux)
        return lista
    
    def setNombre(self, nombre):
        self.nombre= nombre
    
    def setNumero(self, numero):
        self.numero= numero
    
    def setEstado(self, estado_id):
        self.estado_id = estado_id
    
    def romper(self):
        self.estado_id = 'Abierta'
        for item in self.items:
            item.setEstado('Revision')
    
    def comprometer(self, session):
        self.estado_id = 'Comprometida'
        for item in self.items:
            item.setEstado('Revision')
        session.add(self)
    
    def removerItemsEliminados(self, session):
        for item in self.items:
            if item.getEstado() == 'Eliminado':
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
        print "\n\n\n\n\n\n"
        for aux in self.items:
            print str(aux.id)+ " : "+ str(aux.getNombre())+" : "+ str(aux.getNumero())
        print "\n\n\n\n\n\n"
        indice= self.items.index(item)
        self.items.insert(indice, nuevaVersion)
        print "\n\n\n\n\n\n"
        for aux in self.items:
            print str(aux.id)+ " : "+str(aux.getNombre()) +" : "+ str(aux.getNumero())
        print "\n\n\n\n\n\n"
        #session.add(self)
        self.items.remove(item)
        #self.reEnumerarItems()
        #self.reEnumerarItemsPorTipo()
        print "\n\n\n\n\n\n"
        for aux in self.items:
            print str(aux.id)+ " : "+str(aux.getNombre()) +" : "+str(aux.getNumero())
        print "\n\n\n\n\n\n"
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
    __tablemame__ = 'solicitud'
    
    id = Column(db.Integer, primary_key=True)
    estado = Column(db.SmallInteger, default=NO_INICIADO)
    si = Column(db.Integer, nullable=False, default=0)
    no = Column(db.Integer, nullable=False, default=0)
    
    
# RELACIONES ===============================================================================
    # one-to-many relationship
    comite_id = Column(db.Integer, db.ForeignKey('comite.id'))
    item_id = Column(db.Integer, db.ForeignKey('item.id'))


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
    
