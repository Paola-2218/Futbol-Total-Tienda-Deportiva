from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ClienteForm(FlaskForm):

    nombre = StringField(
        "Nombre del cliente",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=100, message="El nombre debe tener entre 3 y 100 caracteres.")
        ]
    )

    correo = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingrese un correo electrónico válido.")
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(min=7, max=15, message="Ingrese un número de teléfono válido.")
        ]
    )

    submit = SubmitField("Registrar cliente")