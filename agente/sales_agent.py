from agente.sql_agent import SQLAgent
from connectors.mcp_sql_client import MCPSQLClient
from langchain_aws import ChatBedrock
from agente.intent_router import IntentRouter
import os
from dotenv import load_dotenv

load_dotenv()

class SalesAgent:
    def __init__(self):
        model_id=os.getenv("BEDROCK_MODEL_ID")
        region_name = os.getenv("AWS_REGION")
        self.llm = ChatBedrock(model_id = model_id,
                                region_name = region_name) 

        self.sql_agent = SQLAgent(self.llm)
        self.mcp_client = MCPSQLClient("data/ventas.db")
        self.router = IntentRouter()

    def run(self, user_input: str):
        try:
            # 1. Clasificar intención
            plan = self.router.classify(user_input)
            
            # 2. SQL y Resultados
            sql_query = self.sql_agent.generate_sql(user_input)
            print(f"\n🔍 SQL Generado: {sql_query}")
            
            results = self.mcp_client.run_query(sql_query)

            if results is None or (isinstance(results, list) and len(results) == 0):
                print("⚠️ No se encontraron registros.")
                return

            import pandas as pd
            df = pd.DataFrame(results)

            # --- EJECUCIÓN BASADA EN FLAGS ---

            # ACCIÓN: Tabla (Si el plan dice show_table)
            if plan.get("show_table"):
                print("\n--- RESULTADOS (TABLA) ---")
                print(df.to_string(index=False))

            # ACCIÓN: Gráfico (Si el plan dice show_chart)
            if plan.get("show_chart"):
                print("\n📊 Generando gráfico...")
                self.generar_grafico(df)

            # ACCIÓN: Exportar (Si el plan dice export_file)
            if plan.get("export_file"):
                print("\n💾 Exportando a CSV...")
                df.to_csv("reporte_ventas.csv", index=False)
                print("✅ Archivo 'reporte_ventas.csv' guardado exitosamente.")

        except Exception as e:
            print(f"Error inesperado en SalesAgent: {e}")

    def generar_grafico(self, df):
        import matplotlib.pyplot as plt
        try:
            plt.figure(figsize=(10, 6))
            
            # Usamos la primera columna para el eje X y la última para el Y
            # En tu caso: X=producto, Y=total_vendido
            columnas = df.columns
            df.plot(kind='bar', x=columnas[0], y=columnas[-1], color='skyblue', legend=False)
            
            plt.title("Análisis de Ventas")
            plt.xlabel(columnas[0].capitalize())
            plt.ylabel(columnas[-1].replace('_', ' ').capitalize())
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # Guardar el archivo
            nombre_archivo = "grafico_ventas.png"
            plt.savefig(nombre_archivo)
            plt.close() # Cerramos la figura para liberar memoria
            print(f"✅ Gráfico guardado exitosamente como '{nombre_archivo}'")
            
        except Exception as e:
            print(f"⚠️ Error al crear el gráfico: {e}")