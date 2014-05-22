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
]).config [
    "$routeProvider"
    ($routeProvider) ->
        $routeProvider.when "/${table_name}.form",
            templateUrl: "app/${table_name}/form.html"
            controller: "${class_name}FormCtrl"

        $routeProvider.when "/${table_name}.form/:id",
            templateUrl: "app/${table_name}/form.html"
            controller: "${class_name}FormCtrl"

        $routeProvider.when "/${table_name}.table",
            templateUrl: "app/${table_name}/table.html"
            controller: "${class_name}TableCtrl"

        $routeProvider.otherwise redirectTo: "/${table_name}.table"
]


centralConfig.config(app)