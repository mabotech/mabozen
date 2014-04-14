<%
payload = '{"ab":"cd"}'
%>
'use strict';

function My${class_name}($scope, $http) {


    console.log("info");

    $scope.post = function() {

        console.log("post");

        var payload = ${payload};



        $http({
            method: 'POST',
            url: '/v2/si/01',
            data: {"data":"from angular, port 8011", "info":{"version":"0.0.1", "type":1}}
        }).
        success(function(data, status) {
            console.log(data);

        }).
        error(function(data, status) {
            console.log("Error");
        });
    }

};

MyCtrl1.$inject = ['$scope', '$http'];