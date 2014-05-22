"use strict"

# uglifyjs table.js -b  --comments all 
###
${class_name}TableCtrl
table view of entity
save pagination and filter params in session?
###

#function FacilityListCtrl($scope, $routeParams, $http,  sessionService, entity, common) {
module = angular.module("maboss.${class_name}TableCtrl", [])

module.controller "${class_name}TableCtrl", [
    "$scope"
    "$routeParams"
    "$log"
    "contextService"
    "dataService"
    "translationService"
    "helpers"
    ($scope, $routeParams, $log, contextService, dataService, translationService, helpers) ->
        
        #table name
        $scope.table = "${table_name}"
        
        #primary key
        $scope.pkey = "${pkey}"
        
        #configuration for datatables 
        
        #var texts_languageid = {msgid:text}; 
        _t = translationService.translate
        
        
        init ->
            $log.debug("init")
        
        ###
        init table columns
        ###
        
        $scope.columns = [
%for attr in attrs:        
            {
                data: "${attr["column"]}"
                title: _t("${attr["column"]}")
                orderable: true
                show: true
    %if pkey == attr["column"]:
                render: (data, type, row) ->
                    "<a href=\"#/facility.form/" + data + "\">" + data + "</a>"
    %endif
    
            }
%endfor            
            {
                data: "modifiedon"
                title: _t("modifiedon")
                show: false
            }
            {
                data: "createdon"
                title: _t("createdon")
                show: false
            }
            {
                data: "createdby"
                title: _t("createdby")
                orderable: false
                show: false
            }
        ]
        
        ###
        # call service
        ###    
        fetch = (data, callback) ->
            cols = []
            i = undefined
            i = 0
            while i < data.columns.length
                cols.push data.columns[i].data
                i++
            
            # construct jsonrpc params
            params =
                table: $scope.table
                pkey: $scope.pkey
                cols: cols
                orderby: [
                    parseInt(data.order[0].column) + 1
                    data.order[0].dir
                ].join(" ")
                offset: data.start
                domain: [[[
                    cols[0]
                    "ilike"
                    data.search.value + "%"
                ]]]
                limit: data.length
                
                #hardcode
                languageid: "1033"

            
            #fetch
            dataService.fetch(params).then ((result) ->
                
                #$log.debug(JSON.stringify(result));
                $log.debug "fetch success", result
                result.recordsTotal = result.total
                result.recordsFiltered = result.count

                $log.debug JSON.stringify(result)
                callback result
                return
            ), (result) ->
                $log.error "error", result
                rdata = data: []
                callback rdata
                return

            return

        
        ###
        #    table config
        ###   
        $("#main_table").dataTable
            
            #"processing": true,
            serverSide: true
            
            #data:get_data(),
            aaSorting: [[
                0
                "desc"
            ]]
            sPaginationType: "bootstrap"
            oLanguage:
                sSearch: "Search"
                sLengthMenu: "_MENU_"

            ajax: (data, callback, setting) ->
                
                # $log.debug(JSON.stringify(data));
                fetch data, callback
                return

            columns: $scope.columns
            columnDefs:
                render: (data, type, row) ->
                    data + " (" + row[3] + ")"
        
        ###
        delete
        ###
        $scope.delete = ->
            params = {
                table:$scope.table
                ids:[]
                }
                
            if params.ids.length > 0
                dataService.delete(params)
        
        
        ###
        init
        ###
        init()
]
