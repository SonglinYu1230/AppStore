var loadingView;

function showLoadingWithMessage() {
    loadingView = bootbox.dialog({
        message: '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Loading...</div>'
    })
}

function hideLoadingView() {
    loadingView.modal('hide');
}