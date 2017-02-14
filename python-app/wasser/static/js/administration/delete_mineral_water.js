//arguments ro delete a single mineral water usinf it own url.
var deleteMineralWaterUrl = null;

function setMineralWaterId(delete_url, key) {
    $('#deleteDialog').modal('show');
    var btnCancel = $("[name='btnCancel']");
    btnCancel.attr("id", "btnCancel-" + key);
    var btnCancel = $("[name='btnConfirm']");
    btnCancel.attr("id", "btnConfirm-" + key);

    deleteMineralWaterUrl = delete_url;
}

function deleteMineralWaterWithId() {
    window.location.href = deleteMineralWaterUrl;
}