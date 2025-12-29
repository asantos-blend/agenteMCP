from agente.sales_agent import SalesAgent

def main():
    # 1. Inicializa el agente (esto ejecutará el __init__ con el LLM y el SQLAgent)
    try:
        agent = SalesAgent()
    except Exception as e:
        print(f"Error al inicializar el agente: {e}")
        return

    print("🚀 Agente de Ventas listo (escribe 'salir' para terminar)\n")

    while True:
        user_input = input("Usuario: ")
        
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("Hasta luego!")
            break
        
        if not user_input.strip():
            continue

        try:
            # 2. El método run se encarga de TODO: SQL, Router, Tabla y Gráficos
            # No necesitas hacer prints manuales de SQL aquí si ya los hace agent.run()
            agent.run(user_input)
            
        except Exception as e:
            print(f"Error procesando la solicitud: {e}")

if __name__ == "__main__":
    main()