"use strict";

/**
 * ${class_name}ListCtrl
 * view of engity list
 */
function ${class_name}ListCtrl($scope, $http) {
    // global
    var DEFAULT_SORT_ICON = "";
    var SORT_UP_ICON = "chevron-up";
    var SORT_DOWN_ICON = "chevron-down"; 
    
    var DEFAULT_PAGE_SIZE = 15;
    $scope.limit = DEFAULT_PAGE_SIZE;
    $scope.pagesize = [5, 10, 15, 20, 30, 50, 100 ];
    $scope.change_limit = function() {
        $scope.post();
    };
    
     $scope.isCollapsed = true;
    
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
        
    /**
        * alert
        */
    $scope.alert=function(msg){
        //console.log(msg);
    }
        
    $scope.check= function(id){
            //if(not in){
            $scope.ids.push(id);
            //}else{
            //remove
            //}
    };
        
    $scope.page_changed = function(page) {
        $scope.currentPage = page;
        elog(page);
        $scope.post();
    };
    //$scope.bigTotalItems = 80;
    $scope.bigCurrentPage = 1;
    $scope.init = function() {
        $scope.table = "${table_name}";
        $scope.cols = [ "company", "texths", "createdon", "createdby", "seq",  "id" ];
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
        $scope.jsonrpc_params = {
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
                domain:[[["active","=","1"], ["seq",">","10"]]], // or[ and[ filter[], ], ]
                languageid: "1033"
            }
        };
        // ajax call, move into service?
        $scope.url = "/api/callproc.call" ;
        $http({
            method: "POST",
            url: $scope.url,
            data: $scope.jsonrpc_params
        }).success(function(data, status) {
            $scope.params =  JSON.stringify($scope.jsonrpc_params, null, 4);
            $scope.data = JSON.stringify(data, null, 4);
            $scope.status = status;
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
    $scope.ids = [];
    
    $scope.delete = function(){
        
        elog("delete");
        // construct jsonrpc params
        
        if ($scope.ids.length == 0){
            elog("no id");
            return;
            
            }
        
        $scope.jsonrpc_params = {
            jsonrpc: "2.0",
            id: "r1",
            method: "call",
            params: {
                method: "mtp_delete_cf2",
                table: $scope.table,
                ids: $scope.ids,
                user: "system"
            }
        };
        // ajax call, move into service?
        $scope.url = "/api/callproc.call" ;
        $http({
            method: "POST",
            url: $scope.url,
            data: $scope.jsonrpc_params
        }).success(function(data, status) {
            $scope.params =  JSON.stringify($scope.jsonrpc_params, null, 4);
            $scope.data = JSON.stringify(data, null, 4);
            $scope.status = status;
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
    }
    // <- End delete
    
    // initialize
    $scope.init();
}

// <- End Controller
${class_name}ListCtrl.$inject = [ "$scope", "$http" ];