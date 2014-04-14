<%
ctrls = []
%>
'use strict';

// Declare app level module which depends on filters, and services
angular.module('myApp', [
  'ngRoute',
  //'myApp.filters',
  //'myApp.services',
  //'myApp.directives',
  // 'myApp.controllers'
]).
config(['$routeProvider', function($routeProvider) {
%for ctrl in ctrls:
  $routeProvider.when('/view_${ctrl}', {templateUrl: '${ctrl}.html', controller: 'Crtl${class_name}'});
%endfor  
  ## $routeProvider.when('/view2', {templateUrl: 'view.html', controller: 'Ctrl'});
  $routeProvider.otherwise({redirectTo: '/view1'});
}]);