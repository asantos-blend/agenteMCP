from mcp_host.sql_mpc import SQLMCP

class MCPSQLClient:
    def __init__(self, db_path: str):
        self.mcp = SQLMCP(db_path)

    def run_query(self, sql: str):
        return self.mcp.execute(sql)
