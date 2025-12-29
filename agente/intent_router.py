class IntentRouter:
    def classify(self, user_input: str) -> dict:
        text = user_input.lower()
        
        plan = {
            "show_table": True,  
            "show_chart": False,
            "export_file": False,
            "chart_type": "bar"
        }

        if any(word in text for word in ["gráfico", "grafica", "visualiza", "top"]):
            plan["show_chart"] = True
            
        if any(word in text for word in ["guarda", "csv", "excel", "descargar", "archivo"]):
            plan["export_file"] = True

        return plan
