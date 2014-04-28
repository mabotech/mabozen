"use strict";

/*
  * Company Controllers
  * Copyright
  * License MIT
  */
/*
  * output to console
  */
function log(msg) {
    console.log(msg);
}

/*
  * CompanyFormCtrl
  */
function CompanyFormCtrl($scope, $http) {
    log("info");
    $scope.company = "Mabotech";
    $scope.texths = "Company Name";
    $scope.post = function() {
        log("post");
        $http({
            method: "POST",
            url: "/api/callproc.call",
            data: {
                data: "from angular, port 8011",
                info: {
                    version: "0.0.1",
                    type: 1
                }
            }
        }).success(function(data, status) {
            $scope.data = data;
            $scope.status = status;
            log(data);
        }).error(function(data, status) {
            $scope.data = data;
            $scope.status = status;
            log("Error");
        });
    };
}

// <- End controller
CompanyFormCtrl.$inject = [ "$scope", "$http" ];

/**
 * CompanyListCtrl
 */
function CompanyListCtrl($scope, $http) {
    // global
    var DEFAULT_SORT_ICON = "";
    var SORT_UP_ICON = "chevron-up";
    var SORT_DOWN_ICON = "chevron-down";
    var DEFAULT_PAGE_SIZE = 15;
    $scope.limit = DEFAULT_PAGE_SIZE;
    $scope.pagesize = [10, 15, 20, 30, 50, 100 ];
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
        log(page);
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
        log("post");
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
            log(data);
            log(status);
            // rows
            $scope.company_list = data.result.rows;
            // pagination data
            $scope.bigTotalItems = data.result.total;
        }).error(function(data, status) {
            log("Error", data);
            log(status);
        });
    };
    // <-End post
    // initialize
    $scope.init();
}

// <- End Controller
CompanyListCtrl.$inject = [ "$scope", "$http" ];