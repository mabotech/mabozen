'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
  'ngRoute',
  'ui.bootstrap', // 'ui.select2'
  
  'myApp.filters',
  'myApp.services',
  'myApp.directives',
 // 'myApp.controllers'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/company.form', {templateUrl: 'views/company/form.html', controller: 'CompanyFormCtrl'});
  $routeProvider.when('/company.list', {templateUrl: 'views/company/list.html', controller: 'CompanyListCtrl'});
  $routeProvider.otherwise({redirectTo: '/company.list'});
}]);
