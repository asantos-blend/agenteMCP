import re
import pandas as pd
import matplotlib.pyplot as plt

def extract_sql(llm_text: str) -> str:
    # 1. Convertir a string por seguridad
    text = str(llm_text)
    
    # 2. Cortar el texto si detectas que se colaron los metadatos de LangChain
    # Buscamos donde termina la consulta (usualmente en la comilla antes de additional_kwargs)
    if 'additional_kwargs=' in text:
        text = text.split('additional_kwargs=')[0]

    # 3. Limpiar los saltos de línea literales que se ven como 'n' pegada a las palabras
    # Primero quitamos los \n reales
    text = text.replace('\\n', ' ').replace('\n', ' ')
    
    # 4. EXTRACCIÓN CON REGEX (Ignorando todo lo que no sea el SELECT)
    # Buscamos desde SELECT hasta el final del string o un punto y coma
    match = re.search(r"SELECT.*?(?:;|$)", text, re.IGNORECASE | re.DOTALL)
    
    if match:
        sql = match.group(0).strip()
        
        # Limpiar comillas dobles residuales al final (común en el error que muestras)
        sql = sql.rstrip('"').rstrip("'")
        
        # 5. ELIMINAR LAS 'n' QUE QUEDARON PEGADAS (Ej: 'ventasnWHERE')
        # Buscamos una 'n' que esté entre una palabra y el inicio de una palabra clave SQL
        sql = re.sub(r'(\w)n(FROM|WHERE|ORDER|LIMIT|GROUP|JOIN|SET|VALUES)', r'\1 \2', sql, flags=re.IGNORECASE)
        
        # Asegurar un solo punto y coma
        sql = sql.rstrip(';') + ';'
        return sql
    
    raise ValueError(f"No se pudo encontrar un SELECT válido en: {text}") 
   
class SQLAgent:
    def __init__(self, llm):
        self.llm = llm
        self.columns = ['id', 'vendedor', 'sede', 'producto', 'cantidad', 'precio', 'fecha']
        self.table = 'ventas'

    def generate_sql(self, user_input: str) -> str:
        # Prompt mejorado para forzar limpieza desde el modelo
        prompt = (
            f"Eres un experto en SQLite. Convierte la petición del usuario a SQL.\n"
            f"TABLA: {self.table}\n"
            f"COLUMNAS: {', '.join(self.columns)}\n"
            f"REGLA 1: Si mencionan 'ciudad' usa la columna 'sede'.\n"
            f"REGLA 2: No uses saltos de línea ni caracteres especiales. Devuelve todo en una sola línea.\n"
            f"REGLA 3: Solo devuelve el código SQL, nada de texto adicional.\n"
            f"REGLA 4: Para filtrar sedes o productos, usa siempre la cláusula LIKE con comodines y COLLATE NOCASE.\n"
            f"Ejemplo: WHERE sede LIKE 'Medellín%%' COLLATE NOCASE o WHERE sede LIKE '%%edell%%' COLLATE NOCASE.\n"
            f"Nota: La base de datos tiene nombres con tildes y mayúsculas iniciales (ej: 'Medellín', 'Bogotá').\n"
            f"Usuario: {user_input}"
        )

        # 1. Llamada correcta al LLM
        response = self.llm.invoke(prompt)

        # 2. Extraer SOLO el contenido de texto
        # LangChain devuelve un AIMessage, el texto está en .content
        if hasattr(response, 'content'):
            text_response = response.content
        else:
            text_response = str(response)

        # 3. Limpieza de emergencia antes de enviar a extract_sql
        # Esto elimina los saltos de línea literales que Bedrock a veces escapa
        text_response = text_response.replace('\\n', ' ').replace('\n', ' ')
        
        return text_response
    
    def procesar_peticion(self, user_input: str):
        # 1. Clasificar intención
        plan = self.router.classify(user_input)
        
        # 2. Obtener y ejecutar SQL
        sql_query = self.sql_agent.generate_sql(user_input)
        results = self.mcp_client.run_query(sql_query)

        # --- VALIDACIÓN DE ORO ---
        if results is None:
            print("❌ Error técnico: La base de datos no respondió.")
            return 
        
        if not results or len(results) == 0:
            print("⚠️ No hay datos para los criterios buscados (revisa mayúsculas/tildes).")
            return
        # -------------------------

        # 3. Ejecutar el plan según el Router
        if plan["show_table"]:
            print("\n=== TABLA DE DATOS ===")
            # Aquí puedes usar tabulate o pandas para que se vea lindo
            import pandas as pd
            df = pd.DataFrame(results)
            print(df.to_string(index=False))

        if plan["show_chart"]:
            print("\n📊 Generando gráfico...")
            self.generar_grafico(results)

        if plan["export_file"]:
            print("\n💾 Exportando archivo...")
            df.to_csv("reporte_ventas.csv", index=False)
            print("Archivo 'reporte_ventas.csv' creado exitosamente.")

    def generar_grafico(self, df):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10,5))
        
        # Intentar usar la primera columna como X y la última como Y (típico en agregaciones)
        eje_x = df.columns[0]
        eje_y = df.columns[-1]
        
        df.plot(kind='bar', x=eje_x, y=eje_y, legend=False)
        plt.title(f"Análisis: {eje_x} vs {eje_y}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("grafico.png")
        print("✅ Gráfico guardado como 'grafico.png'")