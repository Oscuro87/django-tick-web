var commentTitleSpan = $("#comment-title");
var commentDivContent = $("#comment-div #content");

var historyTitleSpan = $("#history-title-span");
var historyDivContent = $("#history-div #content");

$(document).ready(
    function () {
        // History datatable (voir plugin)
        options = {
            "bFilter": false,
            "bLengthChange": false,
            "bInfo": false,
            "bAutoWidth": false,
            "iDisplayLength": 4,
            "sDom": "tp"
        };
        $("#history_table").dataTable(options);

        // Expand / collapse
        historyDivContent.hide();
        historyTitleSpan.click(function () {
                historyDivContent.slideToggle();
            }
        );

        commentDivContent.hide();
        commentTitleSpan.click(function()
        {
            commentDivContent.slideToggle();
        });
    }
);
