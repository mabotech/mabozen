Mabozen
=======

Mabotech Web Application generator, **Model-Driven**.

generate code from json model to pg ddl, pg function, javascript and html, etc.

Domain-Driven in future.


- Executable Schema
- Declarative Behavior




Features
========

- Extract db schema from PostgreSQL and save to JSON file.
- Generate DDL from JSON model.
- Generate HTML and JS (AngularJS Controllers).
- Tools for PostgreSQL Scripts(SQL files) execution and PG functions backup.


Example
=======

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

Roadmap
-------
- CLI
- NodeJS version to generate code?
- Support Oracle, SQL Server schema to json?


License
=======

MIT

