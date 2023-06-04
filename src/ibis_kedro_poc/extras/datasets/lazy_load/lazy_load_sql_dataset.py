from typing import Optional, List
from sqlalchemy import create_engine, MetaData, Table, Column, String, Date, Float, select
from collections import namedtuple
import pandas as pd

# TODO: condition where `value` is another column
Condition = namedtuple('condition', ['column', 'operator', 'value'])


def build_query(table, columns=None, conditions:Optional[List[Condition]]=None):
    """
    Take a SQLAlchemy table object and build a query from it.
    Optionally, select columns to load and different conditions to filter on.

    :param table: SQLAlchemy table object
    :param columns: list of columns to load
    :param conditions: list of Condition objects
    """

    sql_comparison_to_magic_method_map = {
        '=': '__eq__',
        '!=': '__ne__',
        '>': '__gt__',
        '>=': '__ge__',
        '<': '__lt__',
        '<=': '__le__',
    }

    if columns is None:
        columns = [table]
    else:
        columns = [table.c[col] for col in columns]
    
    query = select(*columns)

    if conditions is not None:
        for condition in conditions:
            
            comparison_attribute_name = condition.operator
            tried_map = False
            comparison_attribute = None
            # Hacky way to either get the magic method using the comparison operator
            # or the magic method directly
            while not comparison_attribute:
                try:
                    comparison_attribute = getattr(table.c[condition.column], comparison_attribute_name)
                except AttributeError as er:
                    if not tried_map:
                        comparison_attribute_name = sql_comparison_to_magic_method_map[comparison_attribute_name]
                        tried_map = True
                    else:
                        er
            
            query = query.where(comparison_attribute(condition.value))

    return query


class LazyLoadSQLQueryDataset():
    def __init__(self, table_name, connection_string, load_method=pd.read_sql):
        """
        Save table and connection information for later loading.

        :param table_name: name of the table to load
        :param connection_string: SQLAlchemy connection string
        :param load_method: function to use to load the data (for pandas and spark compatibility)
        """
        self.table_name = table_name
        self.connection_string = connection_string
        self.load_method = load_method
    
    def load(self):
        """
        Initialize the SQLAlchemy engine and table objects without actually loading the data.
        Returns itself, a callable object that can be used to load the data. This is the method which would be called
        on node start.
        """
        engine = create_engine(self.connection_string)
        metadata = MetaData()
        table = Table(self.table_name, metadata, autoload_with=engine)
        self.engine = engine
        self.table = table
        return self
    
    def __call__(self, columns=None, conditions=None):
        """
        Build a query from the table and load the data using the specified load method.
        """
        query = build_query(self.table, columns, conditions)
        return self.load_method(query, self.engine)