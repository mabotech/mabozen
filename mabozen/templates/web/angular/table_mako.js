"use strict";

// uglifyjs table.js -b  --comments all 
/**
 * FacilityListCtrl
 * view of engity list
 * save pagination and filter params in session?
 */
//function FacilityListCtrl($scope, $routeParams, $http,  sessionService, entity, common) {
var module = angular.module("maboss.FacilityTableCtrl", []);

module.controller("FacilityTableCtrl", [ "$scope", "$routeParams", "$http", "sessionService", "dataService", "$log", function($scope, $routeParams, $http, sessionService, dataService, $log) {
    //table name
    $scope.table = "facility";
    //primary key
    $scope.pkey = "facility";
    //configuration for datatables 
    
    //var texts_languageid = {msgid:text}; 
    
    var _t = function(msgid){
        
        return "更新时间";
        
    };
        
    $scope.columns = [ {
        data: "facility",
        title: "Facility Code",
         "render": function ( data, type, row ) {
                    return  '<a href="#/facility.form/'+data +'">'+data+'</a>';
                }
    }, {
        data: "texths",
        title: "Facility"
    }, {
        data: "company",
        orderable: false,
        title: "公司",
        name: "company"
    },{
        data: "modifiedon",
        title: _t('modifiedon')
    },
        

    {
        data: "createdon",
        title: "Created On"
    }, {
        data: "createdby",
        title: "Created By",
        orderable: false,        
    } ];
    /*
     call service
    */
    var fetch = function(data, callback) {
        var cols = [];
        var i;
        for (i = 0; i < data.columns.length; i++) {
            cols.push(data.columns[i].data);
        }
        // construct jsonrpc params
        var params = {
            table: $scope.table,
            pkey: $scope.pkey,
            cols: cols,
            orderby: [ parseInt(data.order[0].column) + 1, data.order[0].dir ].join(" "),
            offset: data.start,
            domain: [ [ [ cols[0], "ilike", data.search.value + "%" ] ] ],
            limit: data.length,
            //hardcode
            languageid: "1033"
        };
        //fetch
        dataService.fetch(params).then(function(result) {
            //$log.debug(JSON.stringify(result));
                $log.debug("fetch success", result);
                result.recordsTotal = result.total,
                result.recordsFiltered= result.count
 
           $log.debug(JSON.stringify(result));
            callback(result);
        }, function(result) {
            $log.error("error", result);
            var rdata = {
                data: []
            };
            callback(rdata);
        });
    };
    /*
    table config
    */
    $("#main_table").dataTable({
        //"processing": true,
        serverSide: true,
        //data:get_data(),
        aaSorting: [ [ 0, "desc" ] ],
        sPaginationType: "bootstrap",
        oLanguage: {
            sSearch: "Search",
            sLengthMenu: "_MENU_"
        },
        ajax: function(data, callback, setting) {
           // $log.debug(JSON.stringify(data));
            fetch(data, callback);
        },
        columns: $scope.columns,
        columnDefs:{
            "render": function ( data, type, row ) {
                    return data +' ('+ row[3]+')';
                },
            }
    });
} ]);