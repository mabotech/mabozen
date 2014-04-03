-- mabozen: mabotech app generator

{% for table in tables %}
-- Table {{table.table}}
CREATE TABLE {{table.table}}
(
{% for col_def in table.column_defs %}
{{ col_def }},
{% endfor  %}
-- common columns:
active smallint NOT NULL DEFAULT 1,
lastupdatedby character varying(40),
lastupdateon timestamp without time zone,
createdon timestamp without time zone,
createdby character varying(40),
rowversionstamp integer NOT NULL DEFAULT 1,
CONSTRAINT pk_{{table.table}} PRIMARY KEY (id)
);

{% endfor %}