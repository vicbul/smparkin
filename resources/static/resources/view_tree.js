$(document).ready(function(){
    $("<div id=resources_tree></div>").appendTo("p.paginator");
    $("#resources_tree").load("http://localhost:8000/graph/resources.models.CSE/116/ .tree");
});