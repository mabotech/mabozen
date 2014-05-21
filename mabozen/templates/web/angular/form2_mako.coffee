"use strict"

# uglifyjs form2_mako.js -b  --comments all
###
# ${class_name} form
###
angular.module("fbpoc.${class_name}FormCtrl", []).controller "${class_name}FormCtrl", [
  "$scope"
  "$builder"
  "$validator"
  "dataService"
  "$log"
  ($scope, $builder, $validator, dataService, $log) ->
  
    table = "${table_name}"
    
    $scope.system = {
        modifiedon:null
        modifiedby:null
        createdon:null
        createdby:null
        rowversion: null
    
    }
    name_pos = {}
    
%for attr in attrs:
<%
#foreign table

if 'pk' in attr:
    pkey = attr['column']

if 'ref' in attr:
    type = 'select4'
else:
    type = 'sampleInput'

#default
if 'default' in attr:
    default = 'default_:"select4""'
else:
    default = '#default'

# required
if 'required' in attr:
    required = str(attr['required']).lower()
else:
    required = 'false'
    
%>
    # ${table_name}.${attr["column"]}
    o_${attr["column"]} =
      name: "${attr["column"]}"
      component: "${type}"
      label: "${attr["column"]}"
      description: ""
      placeholder: "${attr["column"]}"
      required: ${required}
      editable: false
      #readonly:false,
      ${default}
      
%endfor
    
    # object list / initial position
    obj_list = [
%for attr in attrs:      
      o_${attr["column"]}
%endfor
    ]
    
    #
    #    init all select
    #
    init_select = ->

    
    #
    #        init
    #
    init = ->
      j = 0
      $scope.zmodel = []
      $scope.defaultValue = {}
      
      # add form objects
      j = 0
      while j < obj_list.length
        obj = obj_list[j]
        name_pos[ obj.name] = j
        $scope.defaultValue[j] = obj.default_  if "default_" of obj
        $builder.addFormObject "zform", obj
        j++
        
      $scope.zform = $builder.forms["zform"]
      
      #init init_select
      init_select()
      return

    
    #console.log(name_map);
    #var  track = $builder.addFormObject('form_name', tdict);
    # var  facility_code = $builder.addFormObject('form_name', fdict);
    #$scope.form = $builder.forms["zform"];
    # reset field options
    #$builder.forms["zform"][1].options = [ "", 1, 2, 3, 4 ];
    #
    #    default value
    #
    
    #$scope.defaultValue[1] = 3;
    #
    #    submit, save, refresh...
    #
    $scope.submit = ->
        #$validator.validate($scope, "zform").success(->
        #zmodel
        
        fields = {}
        
        if $scope.system.rowversion
            # for update
            fields.rowversion = $scope.system.rowversion
        
        context = {
            languageid:1033
            user:'idea'
        }
        
        for item in $scope.zmodel
            if item.value.length == 0
                fields[item.name] = null
            else
                fields[item.name] = item.value
        
        params = 
            table:'${table_name}'
            pkey:'${pkey}'
            columns:fields
            #hardcode
            context: context


        $log.debug(fields)        
        $log.debug(params)
        
        #call service
        dataService.save(params).then(
            (data)->
                
                $scope.system = data.returning[0]
                
                #pkey must be the first field of the form
                pos = name_pos['${pkey}']
                $builder.forms["zform"][pos].readonly = true
                
                $log.debug(data)
            ,
            (reason) ->
                $log.debug("error", reason)
        
        )
        

        
        #).error ->
        #show message

    
    #
    #    initialize controller
    #
    init()
]
