import os
from supabase import create_client, Client

class SupabaseDB:
    def __init__(self):
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    def execute_select(self, table: str, columns="*", where=None, order_by=None):
        query = self.supabase.table(table).select(columns)

        if where:
            for col, val in where.items():
                query = query.eq(col, val)

        if order_by:
            query = query.order(order_by)

        resp = query.execute()

        if not resp.data:
            return []

        if columns == "*":
            col_names = list(resp.data[0].keys())
        else:
            col_names = [c.strip() for c in columns.split(",")]

        # normaliza para lista de tuplas
        return [tuple(row[col] for col in col_names) for row in resp.data]

    def insert(self, table: str, data: dict):
        resp = self.supabase.table(table).insert(data).execute()
        # retorna id inserido se existir
        if resp.data and "id" in resp.data[0]:
            return resp.data[0]["id"]
        return resp.data

    def update(self, table: str, data: dict, where: dict):
        query = self.supabase.table(table).update(data)
        for col, val in where.items():
            query = query.eq(col, val)
        return query.execute()

    def delete(self, table: str, where: dict):
        query = self.supabase.table(table).delete()
        for col, val in where.items():
            query = query.eq(col, val)
        return query.execute()

    def rpc(self, func_name: str, params: dict):
        """Chama funções SQL personalizadas no Supabase"""
        resp = self.supabase.rpc(func_name, params).execute()
        return resp.data
