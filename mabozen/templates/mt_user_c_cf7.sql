-- Function: mt_user_c_cf7(json)

-- DROP FUNCTION mt_user_c_cf7(json);

CREATE OR REPLACE FUNCTION mt_user_c_cf7(i_json json)
  RETURNS json AS
$BODY$

sql_insert = "
	 insert into mabotech.user 
	 (id, name, active, modifiedon, modifiedby, createdon, createdby)
	 values(DEFAULT, $1, 1, now(), $2, now(), $2)  
	 returning id,lastupdateon, rowversion
	"

#plan = plv8.prepare(sql_insert, ['character varying','character varying'])
	
try	
	rtn = plv8.execute(sql_insert, [i_json.name, i_json.user]) 
	return rtn[0];
catch error
	plv8.elog(LOG, sql_insert)
	return {"error_msg":"#{error}"}
#finally
#plan.free()
	
$BODY$
  LANGUAGE plcoffee VOLATILE
  COST 100;
ALTER FUNCTION mt_user_c_cf7(json)
  OWNER TO postgres;
