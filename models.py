from flask_login import UserMixin


class Usuario(UserMixin):

    def __init__(self, id_usuario, usuario, password):
        self.id_usuario = id_usuario
        self.usuario = usuario
        self.password = password

    def get_id(self):
        return str(self.id_usuario)