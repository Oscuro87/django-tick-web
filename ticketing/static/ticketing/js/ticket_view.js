var historyTable = $("#history_table");

var commentTitleSpan = $("#comment-title");
var commentDivContent = $("#comment-div #content");

var historyTitleSpan = $("#history-title-span");
var historyDivContent = $("#history-div #content");

$(document).ready(
    function () {
        // History datatable (see plugin)
        options = {
            "bFilter": false,
            "bLengthChange": false,
            "bInfo": false,
            "bAutoWidth": false,
            "iDisplayLength": 4,
            "sDom": "tp"
        };
        historyTable.dataTable(options);

        // Expand / collapse
        historyDivContent.hide();
        historyTitleSpan.click(function () {
                historyDivContent.toggle();
            }
        );

        commentTitleSpan.click(function()
        {
            commentDivContent.toggle();
        });
    }
);
