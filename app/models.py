from werkzeug.security import check_password_hash, generate_password_hash
from app import db

NAME_SIZE = 300


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_SIZE))
    password = db.Column(db.String(150))

    def check_password(self, input_password):
        return check_password_hash(self.password, input_password)

    def set_password(self, input_password):
        self.password = generate_password_hash(input_password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_SIZE))
    rule = db.Column(db.String(300))


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_SIZE))
    mac_address = db.Column(db.String(17))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('Group')

    def clear_group(self):
        self.group_id = 0


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_SIZE))
