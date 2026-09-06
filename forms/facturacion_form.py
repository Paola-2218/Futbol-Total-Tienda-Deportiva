from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange


class FacturacionForm(FlaskForm):

    numero = StringField(
        "Número de factura",
        validators=[
            InputRequired(message="El número de factura es obligatorio."),
            Length(
                min=3,
                max=20,
                message="Ingrese un número de factura válido."
            )
        ]
    )

    cliente = StringField(
        "Cliente",
        validators=[
            InputRequired(message="El cliente es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    total = FloatField(
        "Total",
        validators=[
            InputRequired(message="El total es obligatorio."),
            NumberRange(
                min=0.01,
                message="El total debe ser mayor que 0."
            )
        ]
    )

    submit = SubmitField("Registrar factura")