# Este Archivo es para trabajar el contenido de la materia Inteligencia Artificial 1
## Configuración del Ambiente Virtual de Python InteligenciaArtifical1

### Ambiente Virtual Actual: `InteligenciaArtifical1`

Para activar el ambiente virtual ya creado en este proyecto:

```powershell
# Navegar a la carpeta del proyecto
cd C:\Users\sambo\Documents\Programacion\GitHub\python

# Activar el ambiente virtual
.\InteligenciaArtifical1\Scripts\Activate.ps1

## Desactivar el Ambiente Virtual

Cuando termines de trabajar, desactiva el ambiente virtual con:

```powershell
deactivate
```

## Ejemplo Completo de Uso

```powershell
# Navegar a la carpeta del proyecto
cd C:\Users\sambo\Documents\Programacion\GitHub\python

# Activar el ambiente virtual
.\InteligenciaArtifical1\Scripts\Activate.ps1

# Entrar a la carpeta del proyecto
cd InteligenciaArtifical1 

# Instalar dependencias desde requirements.txt
pip install -r requirements.txt

# Instalar paquetes individuales (ejemplo)
pip install paquete_deseado

# Desactivar cuando termines
deactivate
```

## Solucionar Problemas de Permisos en PowerShell

Si recibes un error de permisos al ejecutar el script de activación, ejecuta:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Notas Importantes

- El ambiente virtual debe estar activado antes de instalar paquetes con `pip`
- Cuando está activado, verás el nombre del ambiente en el prompt: `(InteligenciaArtifical1) PS C:\...`
- Los paquetes instalados en este ambiente solo están disponibles cuando está activado
- Para agregar todos los paquetes instalados en el ambiente al archivo requeriments.txt:

```powershell
pip freeze > requirements.txt
```

- Si solo se desean ciertos paquetes se recomienda agregarlos manualmente en el archivo requeriments.txt por ejemplo:

```powershell
echo numpy >> requirements.txt
```
Agrega el paquete numpy a la lista de requerimentos.

# Crear un Ambiente Virtual

Para crear un nuevo ambiente virtual en Python, ejecuta el siguiente comando:

```powershell
python -m venv nombre_del_ambiente
```

# Activar el Ambiente Virtual

Una vez creado, activa el ambiente virtual con:

```powershell
.\nombre_del_ambiente\Scripts\Activate.ps1
```
