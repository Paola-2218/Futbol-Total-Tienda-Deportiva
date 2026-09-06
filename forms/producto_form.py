from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=100, message="El nombre debe tener entre 3 y 100 caracteres.")
        ]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[
            DataRequired(message="La descripción es obligatoria."),
            Length(min=5, max=300, message="La descripción debe tener entre 5 y 300 caracteres.")
        ]
    )

    categoria = SelectField(
        "Categoría",
        choices=[
            ("", "Seleccione una categoría"),
            ("Balones", "Balones"),
            ("Botines", "Botines"),
            ("Camisetas", "Camisetas"),
            ("Accesorios", "Accesorios")
        ],
        validators=[
            DataRequired(message="Debe seleccionar una categoría.")
        ]
    )

    precio = FloatField(
        "Precio",
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(min=0.01, message="El precio debe ser mayor que 0.")
        ]
    )

    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(message="El stock es obligatorio."),
            NumberRange(min=0, message="El stock no puede ser negativo.")
        ]
    )

    submit = SubmitField("Registrar producto")