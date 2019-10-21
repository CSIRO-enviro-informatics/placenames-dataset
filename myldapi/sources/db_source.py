import requests, psycopg2, psycopg2.extras, itertools
from lxml import etree
from functools import lru_cache
from .source import Source
from ..attr_mapping import AttributeMappingValue


class DBSource(Source):    
    def __init__(self, conn_str, from_query, id_prop,  attr_map):
        self.conn_str = conn_str
        self.from_query = from_query
        self.attr_map = attr_map
        self.id_prop = id_prop

    @lru_cache(maxsize=1)
    def get_count(self):
        with DBHelpers.get_connection(self.conn_str) as conn, DBHelpers.get_cursor(conn) as cur:            
            first_table = self.from_query.split(" ")[0]
            q = f"SELECT COUNT({self.id_prop}) FROM {first_table}"
            cur.execute(q)
            return cur.fetchone()[0]

    def get_ids(self, startindex, take_count):
        with DBHelpers.get_connection(self.conn_str) as conn, DBHelpers.get_cursor(conn) as cur:
            first_table = self.from_query.split(" ")[0]
            q = f"""SELECT {self.id_prop} 
                  FROM {first_table} 
                  ORDER BY {self.id_prop} 
                  LIMIT {take_count} 
                  OFFSET {startindex}"""
            cur.execute(q)
            return map(lambda x: x[0], cur.fetchall())

    @staticmethod
    def get_col_names(am_list):
        col_list = [] 
        for am in am_list:
            if am.child_attrs:
                child_cols = DBSource.get_col_names(am.child_attrs)
                for col in child_cols:
                    col_list.append(col)
            if hasattr(am, 'col_name'):
                if isinstance(am.col_name, list):
                    for col in am.col_name:
                        col_list.append(col)
                else:
                    col_list.append(am.col_name)

        return col_list

    def get_many_object_details(self, id_list):        
        #col_name could be a list or tuple
        obj_attr_list = []

        col_list = DBSource.get_col_names(self.attr_map)
        col_list.insert(0, self.id_prop)
        col_list = list(dict.fromkeys(col_list)) #remove duplicates

        with DBHelpers.get_connection(self.conn_str) as conn, DBHelpers.get_cursor(conn) as cur:
            q = f"""SELECT {", ".join(col_list)} 
                  FROM {self.from_query} 
                  WHERE {self.id_prop} IN ({", ".join([str(psycopg2.extensions.adapt(x)) for x in id_list])}) 
                  ORDER BY {self.id_prop}
                  """
            cur.execute(q)

            id_attributes = []
            row_id = None
            record_buffer = []

            for record in cur:
                id = record[DBHelpers.col_key(self.id_prop)]                
                if not row_id:
                    row_id = id
                if row_id != id:
                    row_id = id
                    am_vals = self.process_rows(record_buffer, self.attr_map)
                    obj_attr_list.append((id, am_vals))
                    record_buffer = []                    
                record_buffer.append(record)

            if record_buffer:
                am_vals = self.process_rows(record_buffer, self.attr_map)
                obj_attr_list.append((id, am_vals))

        return obj_attr_list

    def process_rows(self, records, am_list):
        attr_pairings = []
        for i, am in enumerate(am_list):
            if am.child_attrs:
                id_col_key = DBHelpers.col_key(am.col_name)
                sorted_records = sorted(records, key=lambda rec: rec[id_col_key])
                child_vals = []
                for id, grouped_records in itertools.groupby(sorted_records, lambda x: x[id_col_key]):
                    am_vals = self.process_rows(list(grouped_records), am.child_attrs)
                    child_vals.append(am_vals)
                                    
                attr_pairings.append((am, child_vals)) 
            else:
                #At this stage, all records should be duplicates (same row data) for the remaining am_list attributes
                record = records[0]   
                if hasattr(am, "col_name"):
                    cols = am.col_name if isinstance(am.col_name, list) else [am.col_name]
                    vals = [record[DBHelpers.col_key(c)] for c in cols]
                    val = vals if len(vals) > 1 else vals[0]
                    value = am.create_value(val) if val else None                    
                else:
                    value = am.create_value(None)
                attr_pairings.append((am, value))

        return attr_pairings

class DBHelpers:
    @staticmethod
    def get_connection(conn_str):
        return psycopg2.connect(conn_str)

    @staticmethod
    def get_cursor(con):
        return con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
    @staticmethod
    def col_key(prop):
        return prop.split(" as ")[-1].split('.')[-1]