# 🤖 Agente de Ventas IA (MCP + Bedrock + SQL)

Este proyecto es un agente de inteligencia artificial capaz de entender consultas en lenguaje natural, transformarlas en consultas SQL, ejecutarlas sobre una base de datos SQLite y entregar resultados en formato de **tablas**, **gráficos** o archivos **CSV**.

Utiliza el modelo **Claude 3.5 Sonnet** a través de **Amazon Bedrock**.

## 🚀 Funcionalidades

- **Consulta en Lenguaje Natural:** Traduce preguntas como "¿Cuáles fueron las ventas en Medellín?" a SQL automáticamente.
- **Ruteador de Intenciones:** Detecta si el usuario desea visualizar una tabla, generar un gráfico de barras o exportar un reporte.
- **Generación de Gráficos:** Crea imágenes `.png` automáticas de los resultados.
- **Exportación de Datos:** Genera archivos `.csv` listos para usar en Excel.
- **Contenerizado con Docker:** Listo para desplegar en cualquier entorno.

---

## 🛠️ Requisitos Previos

1. **Credenciales de AWS:** Tener acceso a Amazon Bedrock y el modelo Claude 3.5 Sonnet habilitado.
2. **Docker y Docker Compose:** (Opcional, pero recomendado para ejecución fácil).
3. **Python 3.11+** (Si se ejecuta localmente).

---

## ⚙️ Configuración

Crea un archivo `.env` en la raíz del proyecto basándote en el archivo `.env.example`:

```env
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0

``` 

## 🐳 Ejecución con Docker (Recomendado)

Para levantar el agente sin preocuparse por las dependencias:

    Construir y levantar el contenedor:
    Bash

docker-compose up --build

Interactuar con el agente: Si no ves el prompt de entrada, usa:
Bash

    docker attach sales_mcp_agent

## 💻 Ejecución Local

Para ejecutar fuera de Docker:

    Instalar dependencias:
    Bash

pip install -r requirements.txt

Ejecutar la aplicación:
Bash

    python main.py

## 📊 Ejemplos de Consultas

Puedes probar con frases como:

    "Muéstrame las ventas totales de la sede de Medellín" (Genera tabla)

    "Dame un gráfico del top 5 de productos más vendidos" (Genera imagen .png)

    "Exporta a un archivo CSV las ventas del último mes" (Genera archivo .csv)

## 📁 Estructura del Proyecto

    agente/: Contiene la lógica del SQL Agent, el Router de intenciones y el Agente principal.

    connectors/: Cliente para la conexión con la base de datos SQLite.

    data/: Contiene la base de datos ventas.db.

    main.py: Punto de entrada de la aplicación.

    Dockerfile & docker-compose.yml: Configuración para despliegue.

## 🛡️ Seguridad

Este proyecto utiliza un archivo .gitignore para evitar la subida de credenciales sensibles (.env).