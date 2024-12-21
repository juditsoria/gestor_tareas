import db
from flask import Flask, render_template, request, redirect, url_for
from models import LibrosPendientes

app = Flask(__name__)


# Función para asignar colores a los libros
def asignar_colores(libros):
    colores = ["list-group-item-primary", "list-group-item-secondary", "list-group-item-success",
               "list-group-item-danger", "list-group-item-warning", "list-group-item-info"]
    for libro in libros:
        libro.color = colores[hash(libro.titulo) % len(colores)]
    return libros


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/deseos")
def deseos():
    todos_los_libros = db.session.query(LibrosPendientes).all()
    libros_con_colores = asignar_colores(todos_los_libros)
    return render_template("deseos.html", libros=libros_con_colores)


@app.route("/crear-libro", methods=["POST"])
def crear():
    libro = LibrosPendientes(titulo=request.form["titulo_libro"], autor=request.form["autor_libro"], leido=False)
    db.session.add(libro)
    db.session.commit()
    return redirect(url_for("deseos"))


if __name__ == "__main__":
    # Crea todas las tablas si no existen
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
