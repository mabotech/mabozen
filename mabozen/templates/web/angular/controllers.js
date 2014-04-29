"use strict";

/*
  * Company Controllers
  * Copyright
  * License MIT
  */
/*
  * output to console
  * TODO:  as a service? 
  * >uglifyjs  controllers.js -b  --comments all
  */
function elog(msg) {
    console.log(msg);
    //alert(msg);
}

/*
  * CompanyFormCtrl
  * view of entity form
  *  Create or update
  */
function CompanyFormCtrl($scope,  $routeParams,  $location,  $http) {
    elog("form");
    $scope.table = "company";
    
     $scope.company_id =  $routeParams.id;
        
    $scope.currencycode = ["CNY","USD"];
    
       $scope.select2Options = {
      //  allowClear:true
    };
    
    $scope.init = function() {
        elog("init");
        if ($scope.company_id === undefined){
            elog("b");
            //$location.url("/company.list");  
        }else{
            elog($scope.company_id);
            $scope.get();
        }

    };
    // $scope.company -> $scope.t_company || $scope.obj ?
    // entity
    $scope.company = {
        id: null,
        seq: null,
        company: "",
        texths: null,
        currencycode: null,
        codesystemtype: null,
        domainmanagerid: null,
        formattype: null,
        objectclass: null,
        modifiedon:null,
        modifiedby:null,
        createdon:null,
        createdby:null,
        rowversion: null
    };
    /**
        *post
        */
    $scope.post = function() {
        elog("post");
        /*
        var columns = {
                    id:$scope.company.id,
                    company: $scope.company.company,
                    texths: $scope.company.texths,
                    currencycode: $scope.company.currencycode,
                    domainmanagerid:$scope.company.domainmanagerid,
                    objectclass:$scope.company.objectclass,
                    rowversion:$scope.company.rowversion
                };
            */
        
        $scope.validate = function(){
            
            /*
            
                if($scope.company.company.length>4){
                    
                    return;
                    }
                if ($scope.company.texths === null ||  $scope.company.texths == undefined){
                    //alert("text required");
                    return;
                    }
                    */
            
            }
        
        elog($scope.company.texths);
            
        var jsonrpc_params = {
            jsonrpc: "2.0",
            id: "r2",
            method: "call",
            params: {
                method: "mtp_upsert_cf5",
                table: $scope.table,
                //eneity
                columns: $scope.company,
                context: {
                    user: "idea",
                    languageid: "1033"
                }
            }
        };
        elog(jsonrpc_params);
        // call ajax
        $http({
            method: "POST",
            url: "/api/callproc.call",
            data: jsonrpc_params
        }).success(function(data, status) {
            elog(data);
            $scope.data = data;
            if (data.result.returning.length === 0) {
                elog("returning error");
                return 0;
            }
            // fill entity
            $scope.company.id = data.result.returning[0].id;
            $scope.company.seq = data.result.returning[0].seq;
            $scope.company.modifiedon = data.result.returning[0].modifiedon;
            $scope.company.modifiedby = data.result.returning[0].modifiedby;
            $scope.company.createdon = data.result.returning[0].createdon;
            $scope.company.createdby = data.result.returning[0].createdby;
            $scope.company.rowversion = data.result.returning[0].rowversion;
            $scope.status = status;
        }).error(function(data, status) {
            $scope.data = data;
            $scope.status = status;
            // error handling and alert
            elog("Error");
            elog(data);
        });
    };
    // <- end post
    
        $scope.get = function() {
        elog("post");
        /*
        var columns = {
                    id:$scope.company.id,
                    company: $scope.company.company,
                    texths: $scope.company.texths,
                    currencycode: $scope.company.currencycode,
                    domainmanagerid:$scope.company.domainmanagerid,
                    objectclass:$scope.company.objectclass,
                    rowversion:$scope.company.rowversion
                };
            */
            
            
        var jsonrpc_params = {
            jsonrpc: "2.0",
            id: "r2",
            method: "call",
            params: {
                method: "mtp_fetch_one_cf1",
                table: $scope.table,
                //eneity
                id: $scope.company_id,
                cols:Object.keys($scope.company) ,
                 languageid: "1033",
                context: {
                    user: "idea",
                    languageid: "1033"
                }
            }
        };
        elog(jsonrpc_params);
        // call ajax
        $http({
            method: "POST",
            url: "/api/callproc.call",
            data: jsonrpc_params
        }).success(function(data, status) {
            elog(data);
            $scope.data = data;
            if (data.result.returning.length === 0) {
                elog("returning error");
                return 0;
            }
            // fill entity
            
            $scope.company = data.result.returning[0];

            $scope.status = status;
        }).error(function(data, status) {
            $scope.data = data;
            $scope.status = status;
            // error handling and alert
            elog("Error");
            elog(data);
        });
    };
    // <- get end
    $scope.init();
}

// <- End controller
CompanyFormCtrl.$inject = [ "$scope", "$routeParams", "$location",  "$http" ];

/**
 * CompanyListCtrl
 * view of engity list
 */
function CompanyListCtrl($scope, $http) {
    // global
    var DEFAULT_SORT_ICON = "";
    var SORT_UP_ICON = "chevron-up";
    var SORT_DOWN_ICON = "chevron-down";
    var DEFAULT_PAGE_SIZE = 15;
    $scope.limit = DEFAULT_PAGE_SIZE;
    $scope.pagesize = [ 10, 15, 20, 30, 50, 100 ];
    $scope.change_limit = function() {
        $scope.post();
    };
    var success = function() {};
    var error = function() {};
    //$scope.totalItems = 35;
    $scope.currentPage = 1;
    $scope.maxSize = 10;
    // sort 
    //default sort column
    $scope.sort_col_seq = 1;
    // default sort dir
    $scope.sort_dir = "asc";
    $scope.page_changed = function(page) {
        $scope.currentPage = page;
        elog(page);
        $scope.post();
    };
    //$scope.bigTotalItems = 80;
    $scope.bigCurrentPage = 1;
    $scope.init = function() {
        $scope.table = "company";
        $scope.cols = [ "company", "texths", "createdon", "seq", "id" ];
        $scope.sort_icons = {};
        var i;
        for (i = 1; i <= $scope.cols.length; i++) {
            $scope.sort_icons[i] = DEFAULT_SORT_ICON;
        }
        $scope.post();
    };
    // sort
    $scope.sort = function(col_seq) {
        if ($scope.sort_col_seq == col_seq) {
            if ($scope.sort_dir == "asc") {
                $scope.sort_dir = "desc";
                $scope.sort_icons[col_seq] = SORT_DOWN_ICON;
            } else {
                $scope.sort_dir = "asc";
                $scope.sort_icons[col_seq] = SORT_UP_ICON;
            }
        } else {
            $scope.sort_icons[$scope.sort_col_seq] = DEFAULT_SORT_ICON;
            $scope.sort_col_seq = col_seq;
            $scope.sort_dir = "asc";
            $scope.sort_icons[col_seq] = SORT_UP_ICON;
        }
        $scope.post();
    };
    /*
        * construct jsonrpc call in service, if switch to other web service 
        * provider, just modify the service lay
        */
    $scope.post = function() {
        elog("post");
        // construct jsonrpc params
        var jsonrpc_params = {
            jsonrpc: "2.0",
            id: "r1",
            method: "call",
            params: {
                method: "mtp_search_cf3",
                table: $scope.table,
                cols: $scope.cols,
                orderby: [ $scope.sort_col_seq, $scope.sort_dir ].join(" "),
                offset: $scope.limit * ($scope.currentPage - 1),
                limit: $scope.limit,
                languageid: "1033"
            }
        };
        // ajax call, move into service?
        $http({
            method: "POST",
            url: "/api/callproc.call",
            data: jsonrpc_params
        }).success(function(data, status) {
            elog(data);
            elog(status);
            // rows
            $scope.company_list = data.result.rows;
            // pagination data
            $scope.bigTotalItems = data.result.total;
        }).error(function(data, status) {
            elog("Error", data);
            elog(status);
        });
    };
    // <-End post
    // initialize
    $scope.init();
}

// <- End Controller
CompanyListCtrl.$inject = [ "$scope", "$http" ];