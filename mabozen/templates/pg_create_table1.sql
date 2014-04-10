-- mabozen: mabotech app generator

{% for table in tables %}
-- Table {{table.table}}
CREATE TABLE {{table.table}}
(
id serial Not NULL,
{% for col_def in table.column_defs %}
{{ col_def }},
{% endfor  %}
-- common columns:
active smallint NOT NULL DEFAULT 1,
modifiedby character varying(40),
modifiedon timestamp without time zone,
createdon timestamp without time zone,
createdby character varying(40),
rowversionstamp integer NOT NULL DEFAULT 1,
CONSTRAINT pk_{{table.table}} PRIMARY KEY (id)
);

{% endfor %}