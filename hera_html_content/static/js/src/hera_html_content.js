/* Javascript for HeraHtmlContentXBlock. */
function HeraHtmlContentXBlock(runtime, element) {

    var handlerUrl = runtime.handlerUrl(element, 'save_hera_html_content');

    $(element).find('.action-cancel').bind('click', function () {
        runtime.notify('cancel', {});
    });

    $(element).find('.action-save').bind('click', function () {
        $('#html-content').html(tinymce.activeEditor.getContent())
        var data = {
            "csrfmiddlewaretoken": $.cookie('csrftoken'),
            'display-name': $('#display-name').val(),
            'image-url': $('#image-url').val(),
            'iframe-url': $('#iframe-url').val(),
            'html-content': $('#html-content').val()
        };

        runtime.notify('save', { state: 'start' });

        $.post(handlerUrl, JSON.stringify(data)).done(function (response) {
            if (response.result === 'success') {
                runtime.notify('save', { state: 'end' });
            }
            else {
                runtime.notify('error', { msg: response.message });
            }
        });
    });

    tinymce.init({selector:'textarea#html-content'})
}