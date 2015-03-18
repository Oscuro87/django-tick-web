$(document).ready(
    function () {
        // Activation des champs étage et bureau quand un bâtiment est sélectionné
        var batimentSelect = $("select#building");
        batimentSelect.change(
            function () {
                var selected = batimentSelect.find(":selected").val();
                var floorField = $("#floor");
                var officeField = $("#office");
                if (selected != "") {
                    floorField.prop("disabled", false);
                    officeField.prop("disabled", false);
                }
                else {
                    floorField.prop("disabled", true);
                    officeField.prop("disabled", true);
                }
            }
        );

        // Chargement des sous-catégories via ajax quand une catégorie est sélectionnée.
        var subCatDiv = $("div#subcategorydiv");
        var catDiv = $("select#category");

        catDiv.change(
            function () {
                selectedValue = catDiv.find(":selected").val();
                if (selectedValue != "empty") {
                    subCatDiv.html("");
                    ajax_fillSubCategories(selectedValue);
                }
                else {
                    subCatDiv.html("{% trans 'Please select a category first.' %}");
                }
            }
        );
    }
);