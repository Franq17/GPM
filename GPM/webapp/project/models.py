
from sqlalchemy import Column, types
try:
    from sqlalchemy.ext.mutable import Mutable
except ImportError:
    from sqlalchemy.types import MutableType as Mutable

from ..extensions import db
from ..utils import get_current_time
from .constants import PROJECT_STATUS, NO_INICIADO


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

class Project(db.Model):

    __tablename__ = 'projects'

#Columnas
   
    id_proyecto = Column(db.Integer, primary_key=True)
    nombre = Column(db.String(32), nullable=False, unique=True)
    descripcion = Column(db.String(200), nullable=True)
    complejidad_total = Column(db.Integer, nullable=False, default=0)
    numero_fases = Column(db.Integer, nullable=False)
    created_time = Column(db.DateTime, default=get_current_time)
    lider_proyecto = Column(db.String(), nullable=False)
    
    # ================================================================
    # One-to-many relationship between projects and project_statuses.
    estado_id = Column(db.SmallInteger, default=NO_INICIADO)

    def getStatus(self):
        return PROJECT_STATUS[self.estado_id]

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

    def follow(self, project):
        project.followers.add(self.id_proyecto)
        self.following.add(project.id_proyecto)

    def unfollow(self, project):
        if self.id in project.followers:
            project.followers.remove(self.id_proyecto)

        if project.id in self.following:
            self.following.remove(project.id_proyecto)

    def get_following_query(self):
        return Project.query.filter(Project.id.in_(self.following or set()))

    def get_followers_query(self):
        return Project.query.filter(Project.id.in_(self.followers or set()))

    # ================================================================
    # Class methods

    @classmethod
    def search(cls, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(
                Project.nombre.ilike(keyword),
            ))
        q = reduce(db.and_, criteria)
        return cls.query.filter(q)
