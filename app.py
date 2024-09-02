from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import filedialog

from tkinter import ttk

"""
Crud para agregar y modificar proveedores 
Por Odil Martinez 
"""

class App:
    def __init__(self) -> None:
        self.raiz = Tk()  # Inicializar Tk() en el constructor
        self.miID = StringVar()
        self.miNombre = StringVar()
        self.miApellido = StringVar()
        self.miDireccion = StringVar()
        self.barraMenu = Menu(self.raiz)

        # Configuración de la ventana principal
        self.raiz.config(menu=self.barraMenu)
        miFrame = Frame(self.raiz, width=400, height=500, bg="#2BE6B9")
        miFrame.pack()
        self.raiz.iconbitmap("htmx.ico")
        self.raiz.title("Gestion proveedores")

        # Configuración del menú
        crearDB = Menu(self.barraMenu, tearoff=0)
        crearDB.add_cascade(label="Crear DB", command=self.crearBase)
        crearDB.add_separator()
        crearDB.add_cascade(label="Salir", command=self.salir)

        limpiar = Menu(self.barraMenu, tearoff=0)
        limpiar.add_cascade(label="Limpiar", command=self.limpiarCampos)

        acercaDe = Menu(self.barraMenu, tearoff=0)
        acercaDe.add_cascade(label="informacion", command=self.uso)
        acercaDe.add_cascade(label="Acerca De", command=self.infoAcercaDe)

        consultar = Menu(self.barraMenu, tearoff=0)
        consultar.add_cascade(label="Consultar", command=self.consultarDatos)

        # Agregar menús al menú principal
        self.barraMenu.add_cascade(label="Archivos", menu=crearDB)
        self.barraMenu.add_cascade(label="Limpiar", menu=limpiar)
        self.barraMenu.add_cascade(label="Acerca De", menu=acercaDe)
        self.barraMenu.add_cascade(label="Consultar", menu=consultar)

        # Configuración de los widgets
        self.labelID = Label(miFrame, text="ID", bg="#2BE6B9", font=("consolas"))
        self.labelID.place(x=20, y=20)
        self.inputID = Entry(miFrame, textvariable=self.miID, bg="#DEE6DC", font=("consolas"))
        self.inputID.place(x=120, y=20)

        self.labelNombre = Label(miFrame, text="Nombre", bg="#2BE6B9", font=("consolas"))
        self.labelNombre.place(x=20, y=60)
        self.inputNombre = Entry(miFrame, textvariable=self.miNombre, bg="#DEE6DC", font=("consolas"))
        self.inputNombre.place(x=120, y=60)

        self.labelApellido = Label(miFrame, text="Apellido", bg="#2BE6B9", font=("consolas"))
        self.labelApellido.place(x=20, y=100)
        self.inputApellido = Entry(miFrame, textvariable=self.miApellido, bg="#DEE6DC", font=("consolas"))
        self.inputApellido.place(x=120, y=100)

        self.labelDireccion = Label(miFrame, text="Direccion", bg="#2BE6B9", font=("consolas"))
        self.labelDireccion.place(x=20, y=140)
        self.inputDireccion = Entry(miFrame, textvariable=self.miDireccion, bg="#DEE6DC", font=("consolas"))
        self.inputDireccion.place(x=120, y=140)

        self.labelTextarea = Label(miFrame, text="Mensaje", bg="#2BE6B9", font=("consolas"))
        self.labelTextarea.place(x=20, y=200)
        self.inputMensaje = Text(miFrame, font=("consolas", 12), bg="#DEE6DC", width=16, height=5, pady=5)
        self.inputMensaje.place(x=120, y=200)

        self.btnCrear = Button(miFrame, font=("consolas", 12), text="Crear", bg="#2BB9E6", command=self.crearRegistro)
        self.btnCrear.place(x=40, y=360)
        self.btnLeer = Button(miFrame, font=("consolas", 12), text="Leer", command=self.leerBase)
        self.btnLeer.place(x=115, y=360)
        self.btnModificar = Button(miFrame, font=("consolas", 12), text="Modificar", command=self.modificarBase)
        self.btnModificar.place(x=180, y=360)
        self.btnEliminar = Button(miFrame, font=("consolas", 12), text="Eliminar", bg="#F73030", command=self.eliminarBase)
        self.btnEliminar.place(x=290, y=360)

        messagebox.showinfo(
            "BBDD",
            """Bienvenido a Gestor de proveedores 
        para comenzar te recomendamos dar click en 'Acerca De' informacion""",
        )

        self.raiz.mainloop()

    def crearBase(self):
        try:
            miConexion = sqlite3.connect("primeraBase.sqlite3")
            miCursor = miConexion.cursor()

            miCursor.execute(
                """
                CREATE TABLE PROVEEDORES(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NOMBRE VARCHAR(100),
                    APELLIDO VARCHAR(100),
                    DIRECCION VARCHAR(150),
                    MENSAJE TEXT
                )
                """
            )
            messagebox.showinfo("BBDD", "Base de datos creada")

        except:
            messagebox.showwarning("Atencion", "Esta base de datos ya existe")

        miConexion.close()

    def crearRegistro(self):
        miConexion = sqlite3.connect("primeraBase.sqlite3")
        miCursor = miConexion.cursor()
        # datos=inputNombre.get(),inputApellido.get(),inputDireccion.get(),inputMensaje.get("1.0", END)

        nombre = self.inputNombre.get()
        apellido = self.inputApellido.get()
        direccion = self.inputDireccion.get()
        mensaje = self.inputMensaje.get("1.0", END)

        if nombre and apellido:
            miCursor.execute(
                "INSERT INTO PROVEEDORES VALUES(NULL,?,?,?,?)",
                (nombre, apellido, direccion, mensaje),
            )
            messagebox.showinfo("BBDD", "Se insertaron los datos")
        else:
            messagebox.showwarning(
                "BBDD", "Los campos estan vacios por favor rellenalos"
            )

        miConexion.commit()
        miConexion.close()
        self.limpiarCampos()
        self.inputID.focus()

    def leerBase(self):

        miConexion = sqlite3.connect("primeraBase.sqlite3")
        miCursor = miConexion.cursor()
        ID = self.inputID.get()
        if ID:
            miCursor.execute(
                "SELECT * FROM PROVEEDORES WHERE ID = '" + self.inputID.get() + "'"
            )

            elUsuario = miCursor.fetchall()

            for usuario in elUsuario:
                self.miID.set(usuario[0])
                self.miNombre.set(usuario[1])
                self.miApellido.set(usuario[2])
                self.miDireccion.set(usuario[3])
                self.inputMensaje.insert(1.0, usuario[4])
        else:
            messagebox.showwarning("BBDD", "El campo ID esta vacio")

        miConexion.commit()
        miConexion.close()
        # return elUsuario

    def salir(self):
        valor = messagebox.askquestion("Salir?", "Deseas Salir?")
        if valor == "yes":
            self.raiz.destroy()

    def modificarBase(self):
        miConexion = sqlite3.connect("primeraBase.sqlite3")
        miCursor = miConexion.cursor()
        inputID1 = self.inputID.get()

        datos = (
            self.inputNombre.get(),
            self.inputApellido.get(),
            self.inputDireccion.get(),
            self.inputMensaje.get("1.0", END),
        )
        nombre = self.inputNombre.get()
        apellido = self.inputApellido.get()
        direccion = self.inputDireccion.get()
        mensaje = self.inputMensaje.get("1.0", END)

        if inputID1 == "":
            messagebox.showwarning("BBDD", "El campo ID esta vacio")
        if nombre:
            miCursor.execute(
                "UPDATE PROVEEDORES SET NOMBRE='"
                + nombre
                + "' WHERE ID ="
                + self.inputID.get()
            )
        if apellido:
            miCursor.execute(
                "UPDATE PROVEEDORES SET APELLIDO='"
                + apellido
                + "' WHERE ID ="
                + self.inputID.get()
            )
        if direccion:
            miCursor.execute(
                "UPDATE PROVEEDORES SET DIRECCION='"
                + direccion
                + "' WHERE ID ="
                + self.inputID.get()
            )
        if mensaje:
            miCursor.execute(
                "UPDATE PROVEEDORES SET MENSAJE='"
                + mensaje
                + "' WHERE ID ="
                + self.inputID.get()
            )

        miConexion.commit()
        messagebox.showinfo("BBDD", "Se actualizo")
        miConexion.close()
        self.limpiarCampos()
        self.inputID.focus()

    def eliminarBase(self):
        miConexion = sqlite3.connect("primeraBase.sqlite3")
        miCursor = miConexion.cursor()
        inputID1 = self.inputID.get()

        miCursor.execute(
            "DELETE FROM PROVEEDORES WHERE ID = '" + self.inputID.get() + "'"
        )

        miConexion.commit()
        messagebox.showinfo("BBDD", "Se elimino correctamente")
        miConexion.close()

    def limpiarCampos(self):
        self.miID.set("")
        self.miNombre.set("")
        self.miApellido.set("")
        self.miDireccion.set("")
        self.v.delete(1.0, END)

    def infoAcercaDe(self):
        messagebox.showinfo(
            "BBDD",
            """
            Aplicacion 'Crud' Odil Martinez
            1- click 'Crear DB' y crear base de datos
            2- Puedes ingresar los datos y modificarlos
            3- Puedes consultar presionando Consultar
            """,
        )

    def filtrarBusqueda(self):
        miConexion = sqlite3.connect("primeraBase.sqlite3")
        miCursor = miConexion.cursor()

        global tv
        global ventanaConsultar
        global inputFiltrar
        global selected
        tv.destroy()
        tv = ttk.Treeview(ventanaConsultar, columns=("col1", "col2", "col3", "col4"))
        tv.grid(row=0, column=0)
        tv.column("#0", width=40)
        tv.column("col1", width=85, anchor=CENTER)
        tv.column("col2", width=85, anchor=CENTER)
        tv.column("col3", width=85, anchor=CENTER)
        tv.column("col4", width=150, anchor=CENTER)

        tv.heading("#0", text="ID", anchor=CENTER)
        tv.heading("col1", text="Nombre", anchor=CENTER)
        tv.heading("col2", text="Apellido", anchor=CENTER)
        tv.heading("col3", text="Direccion", anchor=CENTER)
        tv.heading("col4", text="Mensaje", anchor=CENTER)
        dato = inputFiltrar.get()
        seleccion = ""
        if selected.get() == 1:
            miCursor.execute("SELECT * FROM PROVEEDORES WHERE ID = '" + dato + "'")
            datos = miCursor.fetchall()
            for dato in datos:
                tv.insert(
                    "", END, text=dato[0], values=(dato[1], dato[2], dato[3], dato[4])
                )

        if selected.get() == 2:
            miCursor.execute(
                "SELECT * FROM PROVEEDORES WHERE NOMBRE LIKE '" + dato + "%'"
            )
            datos = miCursor.fetchall()
            for dato in datos:
                tv.insert(
                    "", END, text=dato[0], values=(dato[1], dato[2], dato[3], dato[4])
                )

        if selected.get() == 3:
            miCursor.execute(
                "SELECT * FROM PROVEEDORES WHERE APELLIDO LIKE '" + dato + "%'"
            )
            datos = miCursor.fetchall()
            for dato in datos:
                tv.insert(
                    "", END, text=dato[0], values=(dato[1], dato[2], dato[3], dato[4])
                )

        if selected.get() == 4:
            miCursor.execute(
                "SELECT * FROM PROVEEDORES WHERE DIRECCION LIKE '" + dato + "%'"
            )
            datos = miCursor.fetchall()
            for dato in datos:
                tv.insert(
                    "", END, text=dato[0], values=(dato[1], dato[2], dato[3], dato[4])
                )

            miConexion.commit()
            miConexion.close()

    def consultarDatos(self):
        global ventanaConsultar
        ventanaConsultar = Toplevel()
        ventanaConsultar.title("Consultar Datos")
        ventanaConsultar.iconbitmap("htmx.ico")
        menuConsultar = Menu(ventanaConsultar)
        ventanaConsultar.config(bg="#2BE6B9", menu=menuConsultar)

        acercaDe = Menu(self.barraMenu, tearoff=0)
        acercaDe.add_cascade(label="informacion", command=self.uso)
        acercaDe.add_cascade(label="Acerca De", command=self.infoAcercaDe)

        menuConsultar.add_cascade(label="Acerca De", menu=acercaDe)

        # ventanaConsultar.config(width=400, height=200, bg='darkgreen')
        ventanaConsultar.geometry("650x500")
        valorInput = self.inputNombre.get()

        """ Estilos para TTK Tree View"""

        style = ttk.Style()
        style.theme_use("clam")
        # configurando colores
        style.configure(
            "Treeview",
            background="silver",
            foreground="black",
            rowheight=25,
            fieldbackground="silver",
        )
        # configurando seleccionado
        style.map("Treeview", background=[("selected", "green")])

        global tv
        tv = ttk.Treeview(ventanaConsultar, columns=("col1", "col2", "col3", "col4"))
        tv.grid(row=0, column=0)
        tv.column("#0", width=40)
        tv.column("col1", width=85, anchor=CENTER)
        tv.column("col2", width=85, anchor=CENTER)
        tv.column("col3", width=85, anchor=CENTER)
        tv.column("col4", width=150, anchor=CENTER)

        tv.heading("#0", text="ID", anchor=CENTER)
        tv.heading("col1", text="Nombre", anchor=CENTER)
        tv.heading("col2", text="Apellido", anchor=CENTER)
        tv.heading("col3", text="Direccion", anchor=CENTER)
        tv.heading("col4", text="Mensaje", anchor=CENTER)

        def datosLeer():
            try:
                for campos in tv.get_children():
                    tv.delete(campos)
                miConexion = sqlite3.connect("primeraBase.sqlite3")
                miCursor = miConexion.cursor()
                miCursor.execute("SELECT * FROM PROVEEDORES")

                datos = miCursor.fetchall()

                for dato in datos:
                    tv.insert(
                        "",
                        END,
                        text=dato[0],
                        values=(dato[1], dato[2], dato[3], dato[4]),
                    )
            except:
                messagebox.showwarning("BBDD", "base de datos no se ha creado")
                self.crearBase()
            miConexion.commit()
            miConexion.close()

        datosLeer()

        global selected
        selected = IntVar()
        r1 = Radiobutton(
            ventanaConsultar, text="ID", value=1, variable=selected, bg="#2BE6B9"
        )
        r1.grid(row=2, column=0)
        r2 = Radiobutton(
            ventanaConsultar, text="Nombre", value=2, variable=selected, bg="#2BE6B9"
        )
        r2.grid(row=3, column=0)
        r3 = Radiobutton(
            ventanaConsultar, text="Apellido", value=3, variable=selected, bg="#2BE6B9"
        )
        r3.grid(row=4, column=0)
        r3 = Radiobutton(
            ventanaConsultar, text="Direccion", value=4, variable=selected, bg="#2BE6B9"
        )
        r3.grid(row=5, column=0)
        labelFiltrar = Label(
            ventanaConsultar, text="Filtrar por:", font=("consolas", 12), bg="#2BE6B9"
        ).grid(row=1, column=0)
        global inputFiltrar
        inputFiltrar = Entry(ventanaConsultar, font=("consolas"), bg="#DEE6DC")
        inputFiltrar.grid(row=6, column=0)

        def filtrarBusqueda():
            miConexion = sqlite3.connect("primeraBase.sqlite3")
            miCursor = miConexion.cursor()

            global tv
            tv = ttk.Treeview(
                ventanaConsultar, columns=("col1", "col2", "col3", "col4")
            )
            tv.grid(row=0, column=0)
            tv.column("#0", width=40)
            tv.column("col1", width=85, anchor=CENTER)
            tv.column("col2", width=85, anchor=CENTER)
            tv.column("col3", width=85, anchor=CENTER)
            tv.column("col4", width=150, anchor=CENTER)

            tv.heading("#0", text="ID", anchor=CENTER)
            tv.heading("col1", text="Nombre", anchor=CENTER)
            tv.heading("col2", text="Apellido", anchor=CENTER)
            tv.heading("col3", text="Direccion", anchor=CENTER)
            tv.heading("col4", text="Mensaje", anchor=CENTER)
            dato = inputFiltrar.get()
            seleccion = ""
            if selected.get() == 1:
                miCursor.execute("SELECT * FROM PROVEEDORES WHERE ID = '" + dato + "'")
                datos = miCursor.fetchall()
                for dato in datos:
                    tv.insert(
                        "",
                        END,
                        text=dato[0],
                        values=(dato[1], dato[2], dato[3], dato[4]),
                    )

            if selected.get() == 2:
                miCursor.execute(
                    "SELECT * FROM PROVEEDORES WHERE NOMBRE LIKE '" + dato + "%'"
                )
                datos = miCursor.fetchall()
                for dato in datos:
                    tv.insert(
                        "",
                        END,
                        text=dato[0],
                        values=(dato[1], dato[2], dato[3], dato[4]),
                    )

            if selected.get() == 3:
                miCursor.execute(
                    "SELECT * FROM PROVEEDORES WHERE APELLIDO LIKE '" + dato + "%'"
                )
                datos = miCursor.fetchall()
                for dato in datos:
                    tv.insert(
                        "",
                        END,
                        text=dato[0],
                        values=(dato[1], dato[2], dato[3], dato[4]),
                    )

            if selected.get() == 4:
                miCursor.execute(
                    "SELECT * FROM PROVEEDORES WHERE DIRECCION LIKE '" + dato + "%'"
                )
                datos = miCursor.fetchall()
                for dato in datos:
                    tv.insert(
                        "",
                        END,
                        text=dato[0],
                        values=(dato[1], dato[2], dato[3], dato[4]),
                    )

            miConexion.commit()
            miConexion.close()

        botonFiltrarPor = Button(
            ventanaConsultar,
            text="Filtrar",
            bg="#2BB9E6",
            font=("consolas", 12),
            command=filtrarBusqueda,
        )
        botonFiltrarPor.grid(row=7, column=0)

        # botonFiltrar = Button(ventanaConsultar, text="Filtrar", bg="#2BB9E6", font=("consolas",12),command=filtrarID)
        # botonFiltrar.grid(row=1,column=0)
        botonRecargar = Button(
            ventanaConsultar,
            text="Recargar",
            bg="#2BB9E6",
            font=("consolas", 12),
            command=datosLeer,
        )
        botonRecargar.grid(row=0, column=1)

    def uso(self):
        mensajeInfo = messagebox.showinfo(
            "BBDD",
            """
    1-Crear base de datos en 'Archivos' selecciona 'Crear DB', solo 1 vez, si se creo anteriormente esta en la misma carpeta del EXE.

    2-Una vez creada puedes agregar proveedores.

    3-El campo de ID se crea automaticamente, solo se usa para 'leer', 'modificar' y 'eliminar'.

    4-Para consultar, modificar y eliminar datos, coloca el ID en el campo ID y click en el boton correspondiente.

    5-Para consultas generales presiona 'Consulta'.

    6-Al presionar 'Recargar' scrolea hacea abajo.

    7-Al filtrar tienes que seleccionar el filtro luego escribir.
            """,
        )


App()
