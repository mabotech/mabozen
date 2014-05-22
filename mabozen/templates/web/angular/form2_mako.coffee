"use strict"

# uglifyjs form2_mako.js -b  --comments all
###
# ${class_name} form
###
angular.module("fbpoc.${class_name}FormCtrl", []).controller "${class_name}FormCtrl", [
  "$scope"
  "$routeParams"
  "$log"
  "$builder"
  "$validator"
  "contextService"
  "dataService"
  "translationService"
  "helpers"
  ($scope, $routeParams, $log, $builder, $validator, contextService, dataService, translationService, helpers) ->
  
    $scope.table = "${table_name}"
    $scope.pkey = '${pkey}'
    
    _t = translationService.translate
    
    $scope.system = {
        modifiedon:null
        modifiedby:null
        createdon:null
        createdby:null
        rowversion: null
    
    }
    name_pos = {}
<%
refs = []
%>
%for attr in attrs:
<%
#foreign table

if 'ref' in attr:
    type = 'select4'
    refs.append(attr)
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
      label: _t("${attr["column"]}")
      description: ""
      placeholder: _t("${attr["column"]}_ph")
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
    
    init_edit = ->
        id = $routeParams
        
        if id
            $scope.get()

    #
    #        init
    #
    init = ->
    
      context = contextService.get()
    
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
      
      init_edit()
      
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
    
    ###
    #get options for select
    get_kv = (field) ->
    
        dataService.getkv(params).then(
            (data) ->
                $log.debug(data)
            ,
            (result) ->
                $log.debug("error", data)
        
        )
    
    # initial all select field
    init_select = ->
        
        select_fields = []
        
        for field in select_fields
            
            get_kv(field)
    ###        
            
    get_kv = (table, column) ->
        return [table, column]
    
    #
    #    init all select
    #
    init_select = ->
%for ref in refs:
        get_kv("${ref["ref"]["table"]}", "${ref["ref"]["column"]}")
    
%endfor
        return            
    
    #set value for $scope.system
    ###
    set_sysdata = (data) ->
        
        cols = ["modifiedon","modifiedby","createdon","createdby","rowversion"]
        
        for col in cols
            $scope.system[col] = data[col]
    ###
    # get data for edit
    $scope.get = ->
    
    
        dataService.get(params).then(
            (data) ->
                $log.debug(data)
                $scope.defaultValue[0] = "abc"
            ,
            (result) ->
                $log.debug("error", result)        
        
        
        )
        
        return
        
    # refresh data from db
    $scope.refresh = ->
        
        $scope.get()
    
    #
    # submit, save, refresh...
    #
    $scope.save = ->
        #$validator.validate($scope, "zform").success(->
        #zmodel
        
        #$scope.zmodel[0].value = "abc"
        #$scope.defaultValue[0] = "abc";
        
        fields = {}
        
        if $scope.system.rowversion
            # for update
            fields.rowversion = $scope.system.rowversion
        
        #hardcode
        context = contextService.get()
        ###
        {
            languageid:1033
            user:'idea'
        }
        ###
        for item in $scope.zmodel
            if item.value.length == 0
                fields[item.name] = null
            else
                fields[item.name] = item.value
        
        params = 
            table: $scope.table
            pkey: $scope.pkey
            columns:fields
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
        
        return
        
        #).error ->
        #show message   
    #
    #    initialize controller
    #
    init()
]
