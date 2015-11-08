// instantiate the uploader
Dropzone.autoDiscover = false;

$('#file-dropzone').dropzone({
    url: "/upload",
    maxFilesize: 100,
    paramName: "uploadfile",
    maxThumbnailFilesize: 5,
    init: function() {
        this.on('success', function(file, json) {
        });
        this.on('addedfile', function(file) {
        });
        this.on('drop', function(file) {
        });
    }
});

$(document).ready(function() {});
