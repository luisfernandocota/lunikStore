   $('.listbox').bootstrapDualListbox({
    infoText: 'Total de módulos {0}',
    infoTextFiltered: '<span class="badge bg-warning-400">Encontrados</span> {0} de {1} módulos',
    infoTextEmpty: 'No hay módulos',
    filterPlaceHolder: 'Buscar',
    filterTextClear: 'Mostrar todo'
  });

  /* USER ROLE SELECTED */
  $("#wizard").on("change", "#id_role", function () {
    var _value = $(this).val();
    if(_value != ""){
        $.ajax({
          url: $("input[name=usertype_select]").data("url"),
          data: {'role':_value},
          type: 'get',
          dataType: 'json',
          success: function (data) {
            $("input[name=usertype_select]").val(data.is_group);
          }
        });
      }else{
        $("input[name=usertype_select]").val("");
      }
    });
