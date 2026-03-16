# Oficio Connect SV

Este es un proyecto desarrollado con Django (versión 6.0.3). A continuación, se detallan los pasos necesarios para configurar y ejecutar el proyecto localmente una vez clonado desde GitHub.

## Requisitos Previos

Asegúrate de tener instalado lo siguiente en tu sistema:
- [Python 3.13.0](https://www.python.org/downloads/release/python-3130/)

## Pasos de Configuración

### 1. Clonar el repositorio

Clona el proyecto en tu máquina local y accede al directorio del proyecto:

```bash
git clone https://github.com/rzvlady/oficio-connect-sv.git
cd oficio-connect-sv
```

### 2. Crear y activar un entorno virtual

Se recomienda aislar las dependencias del proyecto utilizando un entorno virtual.

En Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

En macOS y Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Seleccionar el intérprete en VS Code (Recomendado):**
Una vez creado el entorno virtual, si utilizas Visual Studio Code, puedes abrir la paleta de comandos presionando `Ctrl + Shift + P` (o `Cmd + Shift + P` en Mac), buscar la opción **Python: Select Interpreter** y elegir el entorno virtual `.venv` recién creado. Esto configurará el proyecto para utilizar tu entorno virtual y lo activará automáticamente al abrir nuevas terminales integradas.

### 3. Instalar dependencias

Con el entorno virtual activado, es importante actualizar `pip` antes de instalar los paquetes. Ejecuta el siguiente comando:

```bash
python -m pip install --upgrade pip
```

Luego, instala los paquetes requeridos desde el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```
