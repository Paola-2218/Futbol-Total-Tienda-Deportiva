from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ProveedorForm(FlaskForm):

    empresa = StringField(
        "Empresa proveedora",
        validators=[
            DataRequired(message="El nombre de la empresa es obligatorio."),
            Length(min=3, max=100, message="La empresa debe tener entre 3 y 100 caracteres.")
        ]
    )

    producto = StringField(
        "Producto suministrado",
        validators=[
            DataRequired(message="El producto es obligatorio."),
            Length(min=3, max=100, message="El producto debe tener entre 3 y 100 caracteres.")
        ]
    )

    ciudad = StringField(
        "Ciudad",
        validators=[
            DataRequired(message="La ciudad es obligatoria."),
            Length(min=3, max=50, message="La ciudad debe tener entre 3 y 50 caracteres.")
        ]
    )

    submit = SubmitField("Registrar proveedor")