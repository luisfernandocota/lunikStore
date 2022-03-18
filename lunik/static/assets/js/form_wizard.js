/* ============================================================
 * Form Wizard
 * Multistep form wizard using Bootstrap Wizard Plugin
 * For DEMO purposes only. Extract what you need.
 * ============================================================ */
(function($) {

    'use strict';

    function steps(index){
        var form = $('#wizard');
        var user_type = $("input[name=usertype_select]").val();
        if(index == 1){
            if(user_type == "true"){
                $("#box-permissions-group").show();
                $("#box-permissions-items").hide();
            }else{
                $("#box-permissions-group").hide();
                $("#box-permissions-items").show();
            }
        }else if(index == 2){
            if(user_type == "true"){
                $("#box-permissions-actions").hide();
                $("#box-group-actions").show();
            }else{
                $("#box-permissions-actions").show();
                $("#box-group-actions").hide();

                $("#modules_actions").empty();
                $("select[name=modules_group] option:selected").each(function () {
                    $("#modules_actions").append("<optgroup label='"+$(this).text()+"'>"+
                                                "<option value='"+$(this).val()+"|A' selected>Agregar</option>"+
                                                "<option value='"+$(this).val()+"|E' selected>Modificar</option>"+
                                                "<option value='"+$(this).val()+"|D' selected>Eliminar</option>"+
                                                "</optgroup>");
                });
                $('.multiselect').multiselect("destroy");
                $('.multiselect').multiselect({
                    includeSelectAllOption: true,
                    selectAllText: 'Seleccionar todos',
                    allSelectedText: 'Módulos seleccionados',
                    nonSelectedText: 'No hay módulos seleccionados'
                });
            }
        }else if(index == 4){
          form.submit();
        }
         return true;
    }

    $(document).ready(function() {
        $('#rootwizard').bootstrapWizard({
            onTabShow: function(tab, navigation, index) {
                var $total = navigation.find('li').length;
                var $current = index + 1;

                // If it's the last tab then hide the last button and show the finish instead
                if ($current >= $total) {
                    $('#rootwizard').find('.pager .next').hide();
                    $('#rootwizard').find('.pager .finish').show().removeClass('disabled hidden');
                } else {
                    $('#rootwizard').find('.pager .next').show();
                    $('#rootwizard').find('.pager .finish').hide();
                }

                var li = navigation.find('li a.active').parent();

                var btnNext = $('#rootwizard').find('.pager .next').find('button');
                var btnPrev = $('#rootwizard').find('.pager .previous').find('button');

                // remove fontAwesome icon classes
                function removeIcons(btn) {
                    btn.removeClass(function(index, css) {
                        return (css.match(/(^|\s)fa-\S+/g) || []).join(' ');
                    });
                }

                if ($current > 1 && $current < $total) {

                    var nextIcon = li.next().find('.fa');
                    var nextIconClass = nextIcon.attr('class').match(/fa-[\w-]*/).join();

                    removeIcons(btnNext);
                    btnNext.addClass(nextIconClass + ' btn-animated from-left fa');

                    var prevIcon = li.prev().find('.fa');
                    var prevIconClass = prevIcon.attr('class').match(/fa-[\w-]*/).join();

                    removeIcons(btnPrev);
                    btnPrev.addClass(prevIconClass + ' btn-animated from-left fa');
                } else if ($current == 1) {
                    // remove classes needed for button animations from previous button
                    btnPrev.removeClass('btn-animated from-left fa');
                    removeIcons(btnPrev);
                } else {
                    // remove classes needed for button animations from next button
                    btnNext.removeClass('btn-animated from-left fa');
                    removeIcons(btnNext);
                }

                steps(index);
            },
            onNext: function(tab, navigation, index) {
              steps(index);
            },
            onPrevious: function(tab, navigation, index) {
              steps(index);
            },
            onInit: function() {
                $('#rootwizard ul').removeClass('nav-pills');
            }
        });
        $('.remove-item').click(function() {
            $(this).parents('tr').fadeOut(function() {
                $(this).remove();
            });
        });

    });

})(window.jQuery);
