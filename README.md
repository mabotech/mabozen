mabozen
=======

mabotech web app generator.

generate code from json model to pg ddl, pg function, javascript and html, etc.

schema defination

    [
    {"table":"company",
    "properties":[
    	{"name":"company", "column":"company", "type":"varchar(10)", "required":true, "isUnique":true},
    	{"name":"text", "column":"texths",  "type":"hstore"}
    	]
    },
    ...
    ]

output

    -- Table company
    CREATE TABLE company
    (
    company varchar(10) NOT NULL,
    texths hstore,
    -- common columns:
    active smallint NOT NULL DEFAULT 1,
    lastupdatedby character varying(40),
    lastupdateon timestamp without time zone,
    createdon timestamp without time zone,
    createdby character varying(40),
    rowversionstamp integer NOT NULL DEFAULT 1,
    CONSTRAINT pk_company PRIMARY KEY (id)
    );

roadmap
-------
- generate json model from db schema.
- js version?
- support Oracle, SQL Server?