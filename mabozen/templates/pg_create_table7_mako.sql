## -- mako template for ddl
-- mabozen: mabotech app generator

%for table in tables:
-- Table ${table["table"]}

-- DROP TABLE ${table["table"]} CASCADE

CREATE TABLE ${table["table"]}
(
%for col_def in table["column_defs"]:
    ${ col_def },
%endfor
    -- common columns:
    referenceid integer,
    active smallint NOT NULL DEFAULT 1,
    modifiedon timestamp,
    modifiedby varchar(20),
    createdon timestamp,
    createdby varchar(20),
    rowversion integer DEFAULT 1,
    CONSTRAINT pk_${table["table"]} PRIMARY KEY (${table["pk_column"]})
);

%endfor