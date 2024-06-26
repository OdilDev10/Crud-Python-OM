from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import filedialog

from tkinter import ttk

""" 
	Crud para agregar y modificar proveedores 
	Por Odil Martinez 
"""

def crearBase():
	try:
		miConexion = sqlite3.connect("primeraBase")
		miCursor=miConexion.cursor()
	
		miCursor.execute("""
			CREATE TABLE PROVEEDORES(
				ID INTEGER PRIMARY KEY AUTOINCREMENT,
				NOMBRE VARCHAR(100),
				APELLIDO VARCHAR(100),
				DIRECCION VARCHAR(150),
				MENSAJE TEXT
			)
			""")
		messagebox.showinfo("BBDD","Base de datos creada")

	except:
		messagebox.showwarning("Atencion","Esta base de datos ya existe")

	miConexion.close()

def crearRegistro():
	miConexion=sqlite3.connect("primeraBase")
	miCursor = miConexion.cursor()
	# datos=inputNombre.get(),inputApellido.get(),inputDireccion.get(),inputMensaje.get("1.0", END)

	nombre = inputNombre.get()
	apellido = inputApellido.get()
	direccion = inputDireccion.get()
	mensaje = inputMensaje.get("1.0", END)

	if nombre and apellido:
		miCursor.execute("INSERT INTO PROVEEDORES VALUES(NULL,?,?,?,?)",(nombre,apellido,direccion,mensaje))
		messagebox.showinfo("BBDD","Se insertaron los datos")
	else:	
		messagebox.showwarning("BBDD","Los campos estan vacios por favor rellenalos")

	miConexion.commit()
	miConexion.close()
	limpiarCampos()
	inputID.focus()

def leerBase():

	miConexion = sqlite3.connect("primeraBase")
	miCursor = miConexion.cursor()
	ID = inputID.get()
	if ID:
		miCursor.execute("SELECT * FROM PROVEEDORES WHERE ID = '" + inputID.get() + "'")

		elUsuario = miCursor.fetchall()

		for usuario in elUsuario:
			miID.set(usuario[0])
			miNombre.set(usuario[1])
			miApellido.set(usuario[2])
			miDireccion.set(usuario[3])
			inputMensaje.insert(1.0, usuario[4])
	else:
		messagebox.showwarning("BBDD","El campo ID esta vacio")

	miConexion.commit()
	miConexion.close()
	# return elUsuario

def salir():
	valor=messagebox.askquestion("Salir?","Deseas Salir?")
	if valor == "yes":
		raiz.destroy()
		
def modificarBase():
	miConexion = sqlite3.connect("primeraBase")
	miCursor = miConexion.cursor()
	inputID1=inputID.get()

	datos=inputNombre.get(),inputApellido.get(),inputDireccion.get(),inputMensaje.get("1.0", END)
	nombre=inputNombre.get()
	apellido=inputApellido.get()
	direccion=inputDireccion.get()
	mensaje=inputMensaje.get("1.0", END)

	if inputID1 == "":
		messagebox.showwarning("BBDD","El campo ID esta vacio")
	if nombre:
	    miCursor.execute("UPDATE PROVEEDORES SET NOMBRE='" + nombre + "' WHERE ID =" + inputID.get())	
	if apellido:
		miCursor.execute("UPDATE PROVEEDORES SET APELLIDO='" + apellido + "' WHERE ID =" + inputID.get())	
	if direccion:
		miCursor.execute("UPDATE PROVEEDORES SET DIRECCION='" + direccion + "' WHERE ID =" + inputID.get())	
	if mensaje:
		miCursor.execute("UPDATE PROVEEDORES SET MENSAJE='" + mensaje + "' WHERE ID =" + inputID.get())	

	miConexion.commit()
	messagebox.showinfo("BBDD","Se actualizo")
	miConexion.close()	
	limpiarCampos()
	inputID.focus()
	
def eliminarBase():
	miConexion = sqlite3.connect("primeraBase")
	miCursor = miConexion.cursor()
	inputID1=inputID.get()

	miCursor.execute("DELETE FROM PROVEEDORES WHERE ID = '" + inputID.get() + "'")

	miConexion.commit()
	messagebox.showinfo("BBDD","Se elimino correctamente")
	miConexion.close()	

def limpiarCampos():
	miID.set("")
	miNombre.set("")
	miApellido.set("")
	miDireccion.set("")
	inputMensaje.delete(1.0, END)

def infoAcercaDe():
	messagebox.showinfo("BBDD","""
		Aplicacion 'Crud' Odil Martinez
		1- click 'Crear DB' y crear base de datos
		2- Puedes ingresar los datos y modificarlos
		3- Puedes consultar presionando Consultar
		""")

def filtrarBusqueda():
	miConexion = sqlite3.connect("primeraBase")
	miCursor = miConexion.cursor()

	global tv
	global ventanaConsultar
	global inputFiltrar
	global selected
	tv.destroy()
	tv = ttk.Treeview(ventanaConsultar, columns=("col1","col2","col3","col4"))
	tv.grid(row=0, column=0)
	tv.column('#0', width=40)
	tv.column('col1', width=85, anchor=CENTER)
	tv.column('col2', width=85, anchor=CENTER)
	tv.column('col3', width=85, anchor=CENTER)
	tv.column('col4', width=150, anchor=CENTER)

	tv.heading("#0", text="ID", anchor=CENTER)
	tv.heading("col1", text="Nombre", anchor=CENTER)
	tv.heading("col2", text="Apellido", anchor=CENTER)
	tv.heading("col3", text="Direccion", anchor=CENTER)
	tv.heading("col4", text="Mensaje", anchor=CENTER)
	dato = inputFiltrar.get()
	seleccion = ''
	if selected.get() == 1:			
		miCursor.execute("SELECT * FROM PROVEEDORES WHERE ID = '" + dato + "'")
		datos = miCursor.fetchall()
		for dato in datos:
			tv.insert("", END, text=dato[0], values=(dato[1], dato[2], dato[3], dato[4]))

	if selected.get() == 2:
		miCursor.execute("SELECT * FROM PROVEEDORES WHERE NOMBRE LIKE '" + dato + "%'")
		datos = miCursor.fetchall()
		for dato in datos:
			tv.insert("", END, text=dato[0], values=(dato[1], dato[2], dato[3], dato[4]))
				
	if selected.get() == 3:
		miCursor.execute("SELECT * FROM PROVEEDORES WHERE APELLIDO LIKE '" + dato + "%'")
		datos = miCursor.fetchall()
		for dato in datos:
			tv.insert("", END, text=dato[0], values=(dato[1], dato[2], dato[3], dato[4]))
				
	if selected.get() == 4:
		miCursor.execute("SELECT * FROM PROVEEDORES WHERE DIRECCION LIKE '" + dato + "%'")
		datos = miCursor.fetchall()
		for dato in datos:
			tv.insert("", END, text=dato[0], values=(dato[1], dato[2], dato[3], dato[4]))
				
		miConexion.commit()
		miConexion.close()


# ventana de consultar


def consultarDatos():
	global ventanaConsultar
	ventanaConsultar = Toplevel()
	ventanaConsultar.title("Consultar Datos")
	ventanaConsultar.iconbitmap('crud.ico')
	menuConsultar = Menu(ventanaConsultar)
	ventanaConsultar.config(bg="#2BE6B9", menu=menuConsultar)

	acercaDe = Menu(barraMenu, tearoff=0)
	acercaDe.add_cascade(label="informacion", command=uso)
	acercaDe.add_cascade(label="Acerca De", command=infoAcercaDe)

	menuConsultar.add_cascade(label='Acerca De', menu=acercaDe)

	# ventanaConsultar.config(width=400, height=200, bg='darkgreen')
	ventanaConsultar.geometry("650x500")
	valorInput = inputNombre.get()


	""" Estilos para TTK Tree View"""

	style = ttk.Style()
	style.theme_use("clam")
	#configurando colores
	style.configure("Treeview",
			background="silver",
			foreground="black",
			rowheight=25,
			fieldbackground="silver"
		)
	#configurando seleccionado
	style.map("Treeview",
			background=[('selected','green')]
		)

	global tv
	tv = ttk.Treeview(ventanaConsultar, columns=("col1","col2","col3","col4"))
	tv.grid(row=0, column=0)
	tv.column('#0',width=40)
	tv.column('col1',width=85, anchor=CENTER)
	tv.column('col2',width=85, anchor=CENTER)
	tv.column('col3',width=85, anchor=CENTER)
	tv.column('col4',width=150, anchor=CENTER)

	tv.heading("#0", text="ID", anchor=CENTER)
	tv.heading("col1", text="Nombre", anchor=CENTER)
	tv.heading("col2", text="Apellido", anchor=CENTER)
	tv.heading("col3", text="Direccion", anchor=CENTER)
	tv.heading("col4", text="Mensaje", anchor=CENTER)

	def datosLeer():
		try:
			for campos in tv.get_children():
				tv.delete(campos)
			miConexion = sqlite3.connect("primeraBase")
			miCursor = miConexion.cursor()
			miCursor.execute("SELECT * FROM PROVEEDORES")

			datos = miCursor.fetchall()

			for dato in datos:
				tv.insert("", END, text=dato[0], values=(dato[1], dato[2], dato[3], dato[4]))
		except:
			messagebox.showwarning("BBDD","base de datos no se ha creado")
			crearBase()
		miConexion.commit()
		miConexion.close()	

	datosLeer()

	global selected
	selected = IntVar()
	r1 = Radiobutton(ventanaConsultar, text='ID', value=1, variable=selected, bg="#2BE6B9")
	r1.grid(row=2,column=0)
	r2 = Radiobutton(ventanaConsultar, text='Nombre', value=2, variable=selected, bg="#2BE6B9")
	r2.grid(row=3,column=0)
	r3 = Radiobutton(ventanaConsultar, text='Apellido', value=3, variable=selected, bg="#2BE6B9")
	r3.grid(row=4,column=0)
	r3 = Radiobutton(ventanaConsultar, text='Direccion', value=4, variable=selected, bg="#2BE6B9")
	r3.grid(row=5,column=0)
	labelFiltrar = Label(ventanaConsultar, text="Filtrar por:", font=('consolas',12), bg="#2BE6B9").grid(row=1,column=0)
	global inputFiltrar
	inputFiltrar=Entry(ventanaConsultar, font=("consolas"), bg="#DEE6DC")
	inputFiltrar.grid(row=6,column=0)

		
	def filtrarBusqueda():
		miConexion = sqlite3.connect("primeraBase")
		miCursor = miConexion.cursor()

		
		global tv
		tv = ttk.Treeview(ventanaConsultar, columns=("col1","col2","col3","col4"))
		tv.grid(row=0, column=0)
		tv.column('#0',width=40)
		tv.column('col1',width=85, anchor=CENTER)
		tv.column('col2',width=85, anchor=CENTER)
		tv.column('col3',width=85, anchor=CENTER)
		tv.column('col4',width=150, anchor=CENTER)

		tv.heading("#0", text="ID", anchor=CENTER)
		tv.heading("col1", text="Nombre", anchor=CENTER)
		tv.heading("col2", text="Apellido", anchor=CENTER)
		tv.heading("col3", text="Direccion", anchor=CENTER)
		tv.heading("col4", text="Mensaje", anchor=CENTER)
		dato = inputFiltrar.get()
		seleccion = ''
		if selected.get() == 1:			
			miCursor.execute("SELECT * FROM PROVEEDORES WHERE ID = '" + dato + "'")
			datos = miCursor.fetchall()
			for dato in datos:
				tv.insert("", END, text=dato[0], values=(dato[1], dato[2], dato[3], dato[4]))

		if selected.get() == 2:
			miCursor.execute("SELECT * FROM PROVEEDORES WHERE NOMBRE LIKE '" + dato + "%'")
			datos = miCursor.fetchall()
			for dato in datos:
				tv.insert("", END, text=dato[0], values=(dato[1], dato[2], dato[3], dato[4]))
				
		if selected.get() == 3:
			miCursor.execute("SELECT * FROM PROVEEDORES WHERE APELLIDO LIKE '" + dato + "%'")
			datos = miCursor.fetchall()
			for dato in datos:
				tv.insert("", END, text=dato[0], values=(dato[1], dato[2], dato[3], dato[4]))
				
		if selected.get() == 4:
			miCursor.execute("SELECT * FROM PROVEEDORES WHERE DIRECCION LIKE '" + dato + "%'")
			datos = miCursor.fetchall()
			for dato in datos:
				tv.insert("", END, text=dato[0], values=(dato[1], dato[2], dato[3], dato[4]))
				
		miConexion.commit()
		miConexion.close()

	botonFiltrarPor = Button(ventanaConsultar, text="Filtrar", bg="#2BB9E6", font=("consolas",12), command=filtrarBusqueda)
	botonFiltrarPor.grid(row=7,column=0)

	# botonFiltrar = Button(ventanaConsultar, text="Filtrar", bg="#2BB9E6", font=("consolas",12),command=filtrarID)
	# botonFiltrar.grid(row=1,column=0)
	botonRecargar = Button(ventanaConsultar, text="Recargar", bg="#2BB9E6", font=("consolas",12), command=datosLeer)
	botonRecargar.grid(row=0,column=1)





def uso():
	mensajeInfo = messagebox.showinfo("BBDD","""
1-Crear base de datos en 'Archivos' selecciona 'Crear DB', solo 1 vez, si se creo anteriormente esta en la misma carpeta del EXE.

2-Una vez creada puedes agregar proveedores.

3-El campo de ID se crea automaticamente, solo se usa para 'leer', 'modificar' y 'eliminar'.

4-Para consultar, modificar y eliminar datos, coloca el ID en el campo ID y click en el boton correspondiente.

5-Para consultas generales presiona 'Consulta'.

6-Al presionar 'Recargar' scrolea hacea abajo.

7-Al filtrar tienes que seleccionar el filtro luego escribir.
		""")

# Primero creo la ventana
raiz=Tk();


miID=StringVar()
miNombre=StringVar()
miApellido=StringVar()
miDireccion=StringVar()

barraMenu = Menu(raiz)
raiz.config(menu=barraMenu)
miFrame=Frame(raiz, width=400, height=500, bg="#2BE6B9").pack()
# raiz.iconbitmap("crud.ico")
raiz.title("Gestion proveedores")

# Segundo creo los sub-menu
crearDB = Menu(barraMenu, tearoff=0)
crearDB.add_cascade(label="Crear DB", command=crearBase)
crearDB.add_separator()
crearDB.add_cascade(label="Salir", command=salir)

limpiar = Menu(barraMenu, tearoff=0)
limpiar.add_cascade(label="Limpiar", command=limpiarCampos)

acercaDe = Menu(barraMenu, tearoff=0)
acercaDe.add_cascade(label="informacion", command=uso)
acercaDe.add_cascade(label="Acerca De", command=infoAcercaDe)

consultar = Menu(barraMenu, tearoff=0)
consultar.add_cascade(label="Consultar", command=consultarDatos)

# Tercero los agrego a el menu principal
barraMenu.add_cascade(label='Archivos', menu=crearDB)
barraMenu.add_cascade(label='Limpiar', menu=limpiar)
barraMenu.add_cascade(label='Acerca De', menu=acercaDe)
barraMenu.add_cascade(label='Consultar', menu=consultar)

labelID=Label(miFrame, text="ID", bg="#2BE6B9", font=("consolas")).place(x=20,y=20)
inputID=Entry(miFrame, textvariable=miID,bg="#DEE6DC",  font=("consolas"))
inputID.place(x=120,y=20)

labelNombre=Label(miFrame, text="Nombre",bg="#2BE6B9",  font=("consolas")).place(x=20,y=60)
inputNombre=Entry(miFrame, textvariable=miNombre,bg="#DEE6DC",  font=("consolas"))
inputNombre.place(x=120,y=60)

labelApellido=Label(miFrame, text="Apellido",bg="#2BE6B9",  font=("consolas")).place(x=20,y=100)
inputApellido=Entry(miFrame, textvariable=miApellido,bg="#DEE6DC",  font=("consolas"))
inputApellido.place(x=120,y=100)

labelDireccion=Label(miFrame, text="Direccion", bg="#2BE6B9",  font=("consolas")).place(x=20,y=140)
inputDireccion=Entry(miFrame, textvariable=miDireccion, bg="#DEE6DC", font=("consolas"))
inputDireccion.place(x=120,y=140)

labelTextarea = Label(miFrame, text="Mensaje", bg="#2BE6B9",  font=("consolas")).place(x=20,y=200)
inputMensaje = Text(miFrame, font=("consolas", 12), bg="#DEE6DC", width=16, height=5, pady=5)
inputMensaje.place(x=120, y=200)

btnCrear=Button(miFrame, font=("consolas", 12), text="Crear", bg="#2BB9E6", command=crearRegistro).place(x=40,y=360)
btnCrear=Button(miFrame, font=("consolas", 12), text="Leer", command=leerBase).place(x=115,y=360)
btnCrear=Button(miFrame, font=("consolas", 12), text="Modificar", command=modificarBase).place(x=180,y=360)
btnCrear=Button(miFrame, font=("consolas", 12), text="Eliminar",bg="#F73030", command=eliminarBase).place(x=290,y=360)

messagebox.showinfo("BBDD",
	"""Bienvenido a Gestor de proveedores 
para comenzar te recomendamos dar click en 'Acerca De' informacion""")

raiz.mainloop()
