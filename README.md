mabozen
=======

mabotech web app generator, model driven.

generate code from json model to pg ddl, pg function, javascript and html, etc.

Domain-Driven in future.

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
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
	seq serial,
    company varchar(10) NOT NULL,
    texths hstore,
    -- common columns:
    active smallint NOT NULL DEFAULT 1,
    modifiedby character varying(40),
    modifiedon timestamp without time zone,
    createdon timestamp without time zone,
    createdby character varying(40),
    rowversion integer NOT NULL DEFAULT 1,
    CONSTRAINT pk_company PRIMARY KEY (id)
    );

roadmap
-------
- generate json model from db schema.
- js version?
- support Oracle, SQL Server?