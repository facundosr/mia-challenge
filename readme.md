# 📝 **README - Deploy del Proyecto Scraper**  

¡Bienvenido! Este archivo explica cómo desplegar el proyecto **Scraper** utilizando 🐳 Docker y ☁️ **Google Cloud Run** de forma eficiente. 

---
## **Desarrollado por: Facundo Sosa Ruveda**

## 🚀 **Requisitos previos**
Antes de comenzar, asegúrate de tener todo lo siguiente configurado:  

1. ✅ **Cuenta de Google Cloud** con un proyecto habilitado.  
2. ✅ **Credenciales** google-application-credentials.json con las credenciales para trabajar con BigQuery.
3. ✅ Instaladas las herramientas necesarias:  
   - 🛠️ [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)  
   - 🛠️ [Docker](https://docs.docker.com/get-docker/) 

---

## 📦 **Estructura del Proyecto**
📁 Proyecto/
├── 📄 Dockerfile
└── 📁 deployment/
    ├── 📄 deploy.sh
    └── 📄 requirements.txt
└── 📁 scraper/
    └── 📄 yogonet.py

---

## 🛠️ **Configuración Inicial**

1. **Clonar el repositorio** en tu máquina local:  
   ```bash
   git clone https://github.com/facundosr/mia-challenge.git
   cd Proyecto/

## Pasos para el Despliegue
Antes de comenzar debes asegurarte de tener en la raiz del proyecto el archivo .json llamado `google-application-credentials.json`.
[Docu](https://cloud.google.com/bigquery/docs/authentication/end-user-installed?hl=es-419
) 


### 1. Construcción de la Imagen Docker

El `Dockerfile` instala todas las dependencias necesarias para la aplicación, incluido ChromeDriver y Google Chrome para la ejecución del scraper. Sigue estos pasos:

1. Ve al directorio raíz del proyecto.
2. Construye la imagen Docker:
   ```bash docker build -t yogonet-flask-app .

### 2. Ejecución del Script de Despliegue

El script `deploy.sh` configura el proyecto, habilita las APIs necesarias y despliega la aplicación en Cloud Run.

1. Da permisos de ejecución al script:
   ```bash chmod +x deploy.sh
2. Ejecuta el script:
   ```bash ./deployment/deploy.sh

### 3. Configuración de Google Cloud Run

El script realiza las siguientes acciones:

1. **Habilitar servicios necesarios:**

   - `containerregistry.googleapis.com`
   - `artifactregistry.googleapis.com`
   - `run.googleapis.com`

2. **Construir y subir la imagen:**

   - Configura Docker para trabajar con Google Cloud.
   - Subir la imagen al Container Registry del proyecto.

3. **Despliegue en Cloud Run:**

   - Despliega el servicio con 1GB de memoria y puerto 8080.
   - Permite acceso no autenticado para pruebas públicas.

4. **Obtener la URL del servicio:**

   - La URL del servicio será mostrada al final del despliegue.

5. **Ejecución del script**
   - Copiar y pegar la url en el explorador. Esto ejecutará el servicio en cloud run. Si todo es exitoso se puede ver un diccionario similar a este:

    ```{
    "data_sample": [
        {
            "CapitalizedWords": [
                "Senate"
            ],
            "CharCount": 51,
            "Img": "https://imagenesyogonet.b-cdn.net/data/imagenes/2024/12/12/70840/1734008878-us-congress-united-states-capitol-washington-dc-capitolio-estados-unidos-usa-03.jpg",
            "Kicker": "December 17",
            "Link": "https://www.yogonet.com/international/news/2024/12/12/88336-us-senate-committee-to-hold-sports-betting-hearing-next-week",
            "Title": "US Senate committee to hold sports betting hearing next week",
            "WordsCount": 10
        }],
         "message": "Scraping completed",
         "time_elapsed": 14.446839332580566
      } 

---

## Notas Adicionales

1. **Revisar la URL del servicio:**

   - Puedes verificar la URL directamente con:
     ```bash
     gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)'
     ```

2. **Actualizar dependencias:**

   - Si necesitas actualizar las dependencias, edita `deployment/requirements.txt` y reconstruye la imagen Docker.


## Ejecución Local

Si deseas probar la aplicación localmente:

1. Construye y ejecuta el contenedor:
   ```bash
   docker run -p 8080:8080 yogonet-flask-app
   ```
2. Accede a la aplicación en: [http://localhost:8080](http://localhost:8080)

---

## Recursos

- [Google Cloud Run](https://cloud.google.com/run)
- [Google Container Registry](https://cloud.google.com/container-registry)
- [Docker Documentation](https://docs.docker.com/)



