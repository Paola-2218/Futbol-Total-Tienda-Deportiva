from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ProveedorForm(FlaskForm):

    nombre = StringField(
        "Nombre del proveedor",
        validators=[
            DataRequired(message="El nombre del proveedor es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(
                min=7,
                max=15,
                message="Ingrese un número de teléfono válido."
            )
        ]
    )

    correo = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingrese un correo electrónico válido.")
        ]
    )

    submit = SubmitField("Registrar proveedor")