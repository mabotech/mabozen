var pg = require('pg');

require("should");

//or native libpq bindings
//var pg = require('pg').native

describe('mabozen', function() {

    describe('function call', function() {

        it('mtp_find_cf1 should success', function(done) {

            var conString = "postgres://mabotech:mabouser@127.0.0.1:6432/maboss";

            var client = new pg.Client(conString);

            client.connect(function(err) {
                if (err) {
                    return console.error('could not connect to postgres', err);
                }

                var json = {
                    "table": "company",
                    "filter": "seq > 100",
                    "cols": ["id", "seq", "createdby"],
                    "orderby": "2",
                    "offset": "0",
                    "limit": "3"
                }

                var json_str = JSON.stringify(json);

                var sql = "select mtp_find_cf1 as result from mtp_find_cf1('" + json_str + "')";

                client.query(sql, function(err, result) {
                    if (err) {
                        return console.error('error running query', err);
                    }

                    result.rows[0].result.count.should.equal(3);
                    
                    client.end();
                    done();
                });
            });


        });

    });


});
