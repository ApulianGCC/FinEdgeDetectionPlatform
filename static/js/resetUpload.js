$(document).ready(function () {
    $("#resetBtn").click(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/cancel_upload",
            data: {
                id: $(this).val(), // < note use of 'this' here
                access_token: $("#access_token").val()
            },
            success: function(result) {
                Dropzone.forElement('#myDropzone').removeAllFiles(true)
                $("#getOutlineBtn").addClass("gray-button");
                $("#resetBtn").addClass("gray-button");
            },
            error: function(result) {
                alert('error');
            }
        });
    });
});