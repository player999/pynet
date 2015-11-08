// instantiate the uploader
Dropzone.autoDiscover = false;

function progress(percent, $element) {
    var progressBarWidth = percent * $element.width() / 100;
    $element.find('div').animate({ width: progressBarWidth }, 500).html(percent + "% ");
}

$(document).ready(function() {
    $('#file-dropzone').dropzone({
        url: "/upload",
        maxFilesize: 100,
        paramName: "uploadfile",
        maxThumbnailFilesize: 5,
        init: function() {
            this.on('success', function(file, json) {
                $("#file-dropzone").hide();
                $(".result").show();

                $("#deep-view-pic").attr("src", json.image);
                $("#car-class").html(json.class);
                progress(json.confidence*100, $('#car-confidence'));
            });
            this.on('addedfile', function(file) {
            });
            this.on('drop', function(file) {
            });
        }
    });
});
