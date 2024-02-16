from sql_metadata import Parser

SQL1 = """
    select 
         t1.test1
        ,t1.test2
        ,t2.test3
        ,t3.test4
    from mydb.myschema.mytable_1 t1
        left join mydb.myschema.mytable_2 t2
            on t1.key = t2.key
        inner join mydb.myschema.mytable_3 t3
            on t2.key = t3.key3
    where t3.filter = 'test'            
"""


parsed_query=Parser(SQL1)
print(parsed_query.columns)
print(parsed_query.tables)
print(parsed_query.columns_dict)
print(parsed_query.columns_aliases)