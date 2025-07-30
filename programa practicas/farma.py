import streamlit as st
import sys
import bcrypt
import json
import os
from gtts import gTTS
from io import BytesIO
from PIL import Image
import random


# ---------- CONFIGURACIÓN DE PÁGINA Y ESTILO GLOBAL ----------
st.set_page_config(page_title="farma", layout="wide")

# Estilo global
st.markdown("""
    <style>
    .stApp {
        background-color: #EDE8D0;
    }
    input, textarea {
        border: 2px solid white !important;
        background-color: white !important;
        color: black !important;
    }
    .stTextInput > div > div > input {
        border: 2px solid white !important;
        background-color: white !important;
        color: black !important;
    }
    button {
        background-color: white !important;
        color: black !important;
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown, label {
        color: black !important;
    }
    .logo-container {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 9999;
    }
    </style>
""", unsafe_allow_html=True)

# Mostrar logo siempre arriba a la derecha
logo = Image.open("logo_farma.webp")
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image(logo, width=80)
st.markdown('</div>', unsafe_allow_html=True)

# Función para centrar contenido
def centrar_contenido(contenido):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        contenido()

# --------------------- GESTIÓN DE USUARIOS ---------------------
USERS_FILE = "usuarios.json"

def cargar_usuarios():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def guardar_usuarios(usuarios):
    with open(USERS_FILE, "w") as f:
        json.dump(usuarios, f)

def registrar_usuario(nombre_usuario, contraseña):
    usuarios = cargar_usuarios()
    if nombre_usuario in usuarios:
        return False
    hashed = bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt())
    usuarios[nombre_usuario] = hashed.decode()
    guardar_usuarios(usuarios)
    return True

def verificar_credenciales(nombre_usuario, contraseña):
    usuarios = cargar_usuarios()
    if nombre_usuario in usuarios:
        return bcrypt.checkpw(contraseña.encode(), usuarios[nombre_usuario].encode())
    return False


# --------------------- GESTIÓN DE PACIENTES ---------------------
PATIENT_FILE = "pacientes.json"

def cargar_usuarios():
    if os.path.exists(PATIENT_FILE):
        with open(PATIENT_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def guardar_usuarios(usuarios):
    with open(PATIENT_FILE, "w") as f:
        json.dump(usuarios, f)

def registrar_paciente(nombre, primer_apellido, segundo_apellido, fecha_nacimiento, genero, telefono, correo_electronico):
   
    pacientes = {}

    if os.path.exists(PATIENT_FILE):
        with open(PATIENT_FILE, "r") as f:
            try:
                pacientes = json.load(f)
            except json.JSONDecodeError:
                pacientes = {}

    # Creamos un ID único basado en nombre + nacimiento (puedes mejorarlo)
    clave = numero_aleatorio = random.randint(100000, 999999)
    if clave in pacientes:
        return False  # Ya existe

    pacientes[clave] = {
        "nombre": nombre,
        "primer_apellido": primer_apellido,
        "segundo_apellido": segundo_apellido,
        "fecha_nacimiento": fecha_nacimiento,
        "genero": genero,
        "telefono": telefono,
        "correo_electronico": correo_electronico
    }

    with open(PATIENT_FILE, "w") as f:
        json.dump(pacientes, f, indent=4)

    return True


def verificar_credenciales(nombre_usuario, contraseña):
    usuarios = cargar_usuarios()
    if nombre_usuario in usuarios:
        return bcrypt.checkpw(contraseña.encode(), usuarios[nombre_usuario].encode())
    return False

# --------------------- ESTADO DE LA APP ---------------------
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "auth"
if "usuario" not in st.session_state:
    st.session_state.usuario = None


# --------------------- INTERFAZ DE LOGIN ---------------------
if st.session_state.pantalla == "auth":
    def login_ui():
        st.title("farma")
        st.subheader("Iniciar sesión")
        usuario = st.text_input("Nombre de usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Iniciar sesión"):
            if verificar_credenciales(usuario, password):
                st.success("¡Inicio de sesión exitoso!")
                st.session_state.usuario = usuario
                st.session_state.pantalla = "inicio"
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

        if st.button("Registrarse"):
            st.session_state.pantalla = "registro"
            st.rerun()

    centrar_contenido(login_ui)

# --------------------- INTERFAZ DE REGISTRO ---------------------
elif st.session_state.pantalla == "registro":
    def registro_ui():
        st.title("Registrarse")
        nuevo_usuario = st.text_input("Nuevo usuario")
        nueva_contra = st.text_input("Nueva contraseña", type="password")

        if st.button("Crear cuenta"):
            if registrar_usuario(nuevo_usuario, nueva_contra):
                st.success("Usuario creado. Ahora puedes iniciar sesión.")
                st.session_state.pantalla = "auth"
                st.rerun()
            else:
                st.error("Ese usuario ya existe.")

        if st.button("Volver al inicio de sesión"):
            st.session_state.pantalla = "auth"
            st.rerun()

    centrar_contenido(registro_ui)

# --------------------- INTERFAZ PRINCIPAL ---------------------
elif st.session_state.pantalla == "inicio":
    st.markdown(f"### Bienvenido: {st.session_state.usuario}")
    if st.button("Cerrar sesión"):
        st.session_state.pantalla = "auth"
        st.session_state.usuario = None
        st.rerun()

    st.markdown("<h1 style='text-align: center;'>farma</h1>", unsafe_allow_html=True)

    if "pantalla_app" not in st.session_state:
        st.session_state.pantalla_app = "inicio"


    if st.session_state.pantalla_app == "inicio":
        st.subheader("busqueda de paciente:")