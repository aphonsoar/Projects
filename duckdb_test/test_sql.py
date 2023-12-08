# https://www.linkedin.com/posts/khuyen-tran-1401_python-duckdb-pandsa-activity-7138206922733731840-qRSf?utm_source=share&utm_medium=member_desktop
# https://khuyentran1401.github.io/Efficient_Python_tricks_and_tools_for_data_scientists/Chapter5/SQL.html?highlight=duckdb#efficient-sql-operations-with-duckdb-on-pandas-dataframes
# DuckDB, Polars and Pandas performance comparison: https://github.com/prrao87/duckdb-study
import pandas as pd
import duckdb

#%%
mydf = pd.DataFrame({'a':[1,2,3]})
duckdb.query("select sum(a) from mydf").to_df()

#%%
dir = 'C:\\Aphonso_C\\duckdb_test\\'

branch = pd.read_csv(dir+'branch.csv', keep_default_na=False)
city = pd.read_csv(dir+'city.csv', keep_default_na=False)
department = pd.read_csv(dir+'department.csv', keep_default_na=False)
employee = pd.read_csv(dir+'employee.csv', keep_default_na=False)

#%%
#### '%%timeit
sql_test1 = duckdb.query("""
select 
     case 
    	when t1.city_name in ('London', 'Cambridge', 'Bristol') then '1'
        when t1.city_name in ('Manchester', 'Derby') then '2'
        when t1.city_name = 'Lisburn' then '3'
        when t1.city_name in ('Edinburgh', 'Dundee') then '4'
        when t1.city_name in ('Cardiff', 'Newport') then '5'
        else 'Check'
      end as Group_City
    ,round(avg(t3.salary_value),2) as average_salary
    ,group_concat(distinct city_name) as city_names
from city t1
	INNER join branch t2
		on t1.id_city = t2.id_city
	INNER join employee t3
		on t2.id_branch = t3.id_branch
GROUP by 1
order by 2, 1
""").df()

#%%
#### %%timeit
sql_test2 = duckdb.query("""
with 

city1 as
(
	select * 
  	from city
  	where country = 'England'
)

,branch1 as 
( 
    select * 
    from branch b
        left join city1 c
            on b.id_city = b.id_city
)

select * from branch1
""").df()
