"use strict"

###
# Declare app level module which depends on filters, and services
###

# 'ui.select2',
# 'maboss.filters',
# 'maboss.services',
# 'maboss.directives',
# 'myApp.controllers'
app = angular.module("maboss", [
    "ngRoute"
    "ui.bootstrap"
    "ui.validate"
    
    #form builder
    "builder"
    "builder.components"
    "validator.rules"
    
    #mabo services
    "service.jsonrpc"
    "service.contextService"
    "service.dataService"
    "service.translationService"
    "service.helpers"
    
    #controllers    
    "maboss.${class_name}FormCtrl"
    "maboss.${class_name}TableCtrl"
  
]).config [
    "$routeProvider"
    ($routeProvider) ->
        $routeProvider.when "/${table_name}.form",
            templateUrl: "/common/views/form.html"
            controller: "${class_name}FormCtrl"

        $routeProvider.when "/${table_name}.form/:id",
            templateUrl: "/common/views/form.html"
            controller: "${class_name}FormCtrl"

        $routeProvider.when "/${table_name}.table",
            templateUrl: "/common/views/table.html"
            controller: "${class_name}TableCtrl"

        $routeProvider.otherwise redirectTo: "/${table_name}.table"
]


centralConfig(app)