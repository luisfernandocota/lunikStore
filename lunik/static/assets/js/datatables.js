/* ============================================================
 * DataTables
 * Generate advanced tables with sorting, export options using
 * jQuery DataTables plugin
 * For DEMO purposes only. Extract what you need.
 * ============================================================ */
(function($) {

    // Initialize datatable showing a search box at the top right corner
    var initTableWithSearch = function() {
        var table = $('.table-search');

        table.dataTable({
          "bLengthChange": false,
          "bFilter": true,
          "bInfo": false,
          "bAutoWidth": false,
          "paging": true,
          "language": {
        				"url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
        			}
        });

        // search box for table
        $('#search-table').keyup(function() {
            table.fnFilter($(this).val());
        });
    }
    initTableWithSearch();

})(window.jQuery);
