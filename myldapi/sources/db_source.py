import requests, psycopg2, psycopg2.extras
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
        #col_name could be a list or tuple
        obj_attr_list = []

        col_list = [] 
        for am in self.attr_map:
            if hasattr(am, 'col_name'):
                if isinstance(am.col_name, list):
                    for col in am.col_name:
                        col_list.append(col)
                else:
                    col_list.append(am.col_name)

        col_list.insert(0, self.id_prop)
        col_list = list(dict.fromkeys(col_list)) #remove duplicates

        with DBHelpers.get_connection(self.conn_str) as conn, DBHelpers.get_cursor(conn) as cur:
            q = f"""SELECT {", ".join(col_list)} 
                  FROM {self.from_query} 
                  WHERE {self.id_prop} IN ({", ".join([str(psycopg2.extensions.adapt(x)) for x in id_list])}) 
                  """
            cur.execute(q)

            id_attributes = []
            for record in cur:
                id = record[DBHelpers.col_key(self.id_prop)]                
                attr_pairings = []
                for i, am in enumerate(self.attr_map, start=1):
                    cols = am.col_name if isinstance(am.col_name, list) else [am.col_name]
                    vals = [record[DBHelpers.col_key(c)] for c in cols]
                    val = vals if len(vals) > 1 else vals[0]
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
        return con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
    @staticmethod
    def col_key(prop):
        return prop.split('.')[-1]