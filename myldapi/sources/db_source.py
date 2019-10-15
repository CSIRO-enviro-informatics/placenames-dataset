import requests, psycopg2
from lxml import etree
from functools import lru_cache
from .source import Source



class DBSource(Source):    
    def __init__(self, conn_str, from_query, id_prop,  attr_map):
        self.conn_str = conn_str
        self.from_query = from_query
        self.attr_map = attr_map
        self.id_prop = id_prop

    @lru_cache(maxsize=1)
    def get_count(self):
        with DBHelpers.get_connection(self.conn_str) as conn, DBHelpers.get_cursor(conn) as cur:
            q = f"SELECT COUNT({self.id_prop}) FROM {self.from_query}"
            cur.execute(q)
            return cur.fetchone()[0]

    def get_ids(self, startindex, take_count):
        with DBHelpers.get_connection(self.conn_str) as conn, DBHelpers.get_cursor(conn) as cur:
            q = f"""SELECT {self.id_prop} 
                  FROM {self.from_query} 
                  ORDER BY {self.id_prop} 
                  LIMIT {take_count} 
                  OFFSET {startindex}"""
            cur.execute(q)
            return map(lambda x: x[0], cur.fetchall())

    def get_many_object_details(self, id_list):        
        obj_attr_list = []

        col_list = [am.col_name for am in self.attr_map if hasattr(am, 'col_name')]
        col_list.insert(0, self.id_prop)
        with DBHelpers.get_connection(self.conn_str) as conn, DBHelpers.get_cursor(conn) as cur:
            q = f"""SELECT {", ".join(col_list)} 
                  FROM {self.from_query} 
                  WHERE {self.id_prop} IN ({", ".join([str(psycopg2.extensions.adapt(x)) for x in id_list])}) 
                  """
            cur.execute(q)

            id_attributes = []
            # Might want record to be a dict for easy lookup
            # See http://initd.org/psycopg/docs/extras.html#module-psycopg2.extras
            for record in cur:
                id = record[0]                
                attr_pairings = []
                for i, am in enumerate(self.attr_map, start=1):
                    val = record[i]
                    value = am.create_value(val) if val else None
                    attr_pairings.append((am, value))

                obj_attr_list.append((id, attr_pairings))

        return obj_attr_list

    
class DBHelpers:
    @staticmethod
    def get_connection(conn_str):
        return psycopg2.connect(conn_str)

    @staticmethod
    def get_cursor(con):
        return con.cursor()
