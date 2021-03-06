// Generated by CoffeeScript 1.7.1
(function() {
    var pg, should;

    pg = require('pg');

    should = require("should");

    describe('mabozen', function() {
        return describe('funcation call', function() {
            return it('find_cf1 should success', function(done) {
                var client, conString;
                conString = "postgres://mabotech:mabouser@127.0.0.1:6432/maboss";
                client = new pg.Client(conString);
                return client.connect(function(err) {
                    var json, json_str, sql;
                    if (err) {
                        console.error('could not connect to postgres', err);
                    }
                    json = {
                        "table": "company",
                        "filter": "seq > 100",
                        "cols": ["id", "seq", "createdon"],
                        "orderby": "2",
                        "offset": "10",
                        "limit": "3"
                    };
                    json_str = JSON.stringify(json);
                    sql = "select mtp_find_cf1 as result from mtp_find_cf1('" + json_str + "')";
                    return client.query(sql, function(err, rtn) {
                        if (err) {
                            console.error('query error', err);
                        }
                        rtn.rows[0].result.count.should.equal(3);
                        console.log(rtn.rows[0].result);
                        client.end();
                        return done();
                    });
                });
            });
        });
    });

}).call(this);
