from sqlalchemy.orm import backref
from . import db, nlp
from datetime import datetime, date

db.create_all()


class AutoSerialize(object):
    """Mixin for retrieving public fields of model in json-compatible format"""
    __public__ = None

    def get_public(self, exclude=(), extra=()):
        """Returns model's PUBLIC data for jsonify"""
        data = {}
        keys = self._sa_instance_state.attrs.items()
        public = self.__public__ + extra if self.__public__ else extra
        for k, field in keys:
            if public and k not in public: continue
            if k in exclude: continue
            value = self._serialize(field.value)
            if value:
                data[k] = value
        return data

    @classmethod
    def _serialize(cls, value, follow_fk=False):
        if type(value) in (datetime, date):
            ret = value.isoformat()
        elif isinstance(value, str):
            ret = value
        elif hasattr(value, '__iter__'):
            ret = []
            for v in value:
                ret.append(cls._serialize(v))
        elif AutoSerialize in value.__class__.__bases__:
            ret = value.get_public()
        else:
            ret = value

        return ret


class Word(db.Model, AutoSerialize):
    __tablename__ = 'word'
    __public__ = ('id', 'name', 'category', 'tag', 'level')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=128), nullable=False)
    category = db.Column(db.String(length=16), nullable=False)
    tag = db.Column(db.String(length=128))
    value = db.Column(db.Float, default=0.0)
    level = db.Column(db.SmallInteger, default=1)

    @property
    def pos(self):
        return Word.tag_to_pos(self.tag)

    @classmethod
    def pos_to_tag(cls, posed):
        return "|".join("%s/%s" % p for p in posed)

    @classmethod
    def tag_to_pos(cls, tag):
        r = []
        for t in tag.split('|'):
            r.append(t.split('/'))
        return r


class Post(db.Model, AutoSerialize):
    __tablename__ = 'post'
    __public__ = ('id', 'author', 'text', 'score')

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(length=128))
    text = db.Column(db.Text())
    score = db.Column(db.Text())
