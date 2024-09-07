from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# Conexión a la base de datos
db = mysql.connector.connect(
    host="bd",
    user="root",
    password="root",
    database="agenda_db"
)
cursor = db.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS tareas (
    id_tarea INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tarea VARCHAR(255),
    encargado_tarea VARCHAR(255),
    fecha_entrega_tarea DATE,
    estado_tarea VARCHAR(50)
)
""")

# Definir un formulario para el CRUD usando Flask-WTF
class TareaForm(FlaskForm):
    nombre_tarea = StringField('Nombre de la tarea', validators=[DataRequired()])
    encargado_tarea = StringField('Encargado de la tarea', validators=[DataRequired()])
    fecha_entrega_tarea = DateField('Fecha de entrega', format='%Y-%m-%d', validators=[DataRequired()])
    estado_tarea = SelectField('Estado', choices=[('Pendiente', 
                                                   'Pendiente'), ('Completada', 
                                                                  'Completada')], validators=[DataRequired()])
    submit = SubmitField('Guardar')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TareaForm()

    # Manejar la creación de una nueva tarea
    if form.validate_on_submit():
        cursor.execute("INSERT INTO tareas (nombre_tarea, encargado_tarea, fecha_entrega_tarea, estado_tarea) VALUES (%s, %s, %s, %s)",
                       (form.nombre_tarea.data, form.encargado_tarea.data, 
                        form.fecha_entrega_tarea.data, form.estado_tarea.data))
        db.commit()
        return redirect(url_for('index'))

    # Leer todas las tareas de la base de datos
    cursor.execute("SELECT * FROM tareas")
    tareas = cursor.fetchall()

    return render_template('index.html', form=form, tareas=tareas)

# Ruta para eliminar tarea
@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM tareas WHERE id_tarea=%s", (id,))
    db.commit()
    return redirect(url_for('index'))

# Ruta para actualizar tarea
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = TareaForm()

    # Obtener los datos de la tarea actual
    cursor.execute("SELECT * FROM tareas WHERE id_tarea=%s", (id,))
    tarea = cursor.fetchone()

    if request.method == 'GET':
        form.nombre_tarea.data = tarea[1]
        form.encargado_tarea.data = tarea[2]
        form.fecha_entrega_tarea.data = tarea[3]
        form.estado_tarea.data = tarea[4]

    if form.validate_on_submit():
        cursor.execute("UPDATE tareas SET nombre_tarea=%s, encargado_tarea=%s, fecha_entrega_tarea=%s, estado_tarea=%s WHERE id_tarea=%s",
                       (form.nombre_tarea.data, form.encargado_tarea.data, form.fecha_entrega_tarea.data, form.estado_tarea.data, id))
        db.commit()
        return redirect(url_for('index'))

    return render_template('update.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

