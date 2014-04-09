pg = require('pg')

should = require("should")

describe('mabozen', () ->

    describe('funcation call', () ->


        it('find_cf1 should success', (done) ->
        
            conString = "postgres://mabotech:mabouser@127.0.0.1:6432/maboss"
            client = new pg.Client(conString)

            client.connect( (err)->

                if err
                    console.error('could not connect to postgres', err)

                json = {
                    "table": "company",
                    "filter": "seq > 100",
                    "cols": ["id", "seq", "createdon"],
                    "orderby": "2",
                    "offset": "10",
                    "limit": "3"
                }
                
                json_str = JSON.stringify(json)
                
                sql = "select mtp_find_cf1 as result from mtp_find_cf1('#{json_str}')"
                
                #sql = "select now()"
                
                #console.log(sql)
                
                client.query(sql,  (err, rtn) ->
                        
                    if err
                        console.error('query error', err)

                    rtn.rows[0].result.count.should.equal(3)
                    console.log(rtn.rows[0].result)
                    
                    client.end()
                    done()
                )
            )
        )
    )
)