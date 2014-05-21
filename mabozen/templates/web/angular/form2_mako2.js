"use strict";

// uglifyjs form2_mako.js -b  --comments all 
/**
* form
*/
angular.module("fbpoc.FormCtrl", []).controller("FormCtrl", [ "$scope", "$builder", "$validator", "$log", function($scope, $builder, $validator, $log) {
    var table = "facility";
    var name_map = {};
    var fdict = {
        //       id:"facility",
        name: "facility",
        component: "sampleInput",
        label: "New Name",
        description: "",
        placeholder: "Your name",
        required: true,
        editable: false,
        //     readonly:true,
        default_: "Hello"
    };
    // object list / initial position
    var obj_list = [ fdict, fdict,fdict,fdict,fdict,fdict];
    /*
    init all select
    */
    var init_select = function() {};
    /*
        init
    */
    var init = function() {
        var j = 0;
        $scope.zmodel = [];
        $scope.defaultValue = {};
        // add form objects
        for (j = 0; j < obj_list.length; j++) {
            var obj = obj_list[j];
            name_map[j] = obj.name;
            if ("default_" in obj) {
                $scope.defaultValue[j] = obj.default_;
            }
            $builder.addFormObject("zform", obj);
        }
        //init init_select
        init_select();
    };
    //console.log(name_map);
    //var  track = $builder.addFormObject('form_name', tdict);
    // var  facility_code = $builder.addFormObject('form_name', fdict);
    //$scope.form = $builder.forms["zform"];
    // reset field options
    //$builder.forms["zform"][1].options = [ "", 1, 2, 3, 4 ];
    /*
    default value
    */
    //$scope.defaultValue[1] = 3;
    /*
    submit, save, refresh...
    */
    $scope.submit = function() {
        return $validator.validate($scope, "zform").success(function() {}).error(function() {});
    };
    /*
    initialize controller
    */
    init();
} ]);