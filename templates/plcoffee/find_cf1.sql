-- Function: find_cf1(json)

-- DROP FUNCTION find_cf1(json);

CREATE OR REPLACE FUNCTION find_cf1(i_json json)
  RETURNS json AS
$BODY$

#init
msg = ""
v_cols = "*"

#input
v_table = i_json.table

v_filter = i_json.filter

v_orderby = i_json.orderby

v_offset = i_json.offset

v_limit = i_json.limit

if i_json.cols
	v_cols = i_json.cols.join(",")

if not v_filter
	v_filter = "true"

if not v_orderby
	v_orderby = "1"	

if not v_offset
	v_offset = 0

if not v_limit
	v_limit = 25

v_sql = "select count(1) as total from #{v_table} where #{v_filter}"

try
	total = plv8.execute( v_sql )[0]["total"]
catch err
	plv8.elog(DEBUG, v_sql)
	msg = "#{err}"
	total = 0
	
if total== 0
	
	return {"error":msg}

v_sql = "select #{v_cols} 
	from #{v_table} 
	where #{v_filter}  
	order by #{v_orderby} 
	offset #{v_offset} limit #{v_limit}"

try
	rtn = plv8.execute(v_sql)
catch err
	plv8.elog(DEBUG, v_sql)
	msg = "#{err}"
	
if msg != ""
	return {"error":msg}

count = rtn.length

return {"total":total, "count":count,  "result":rtn}

$BODY$
  LANGUAGE plcoffee VOLATILE
  COST 100;
