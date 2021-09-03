$(document).ready(function () {
        var url = window.location;
    // Will only work if string in href matches with location
        $('ul.ul-navbar a[href="' + url + '"]').parent().addClass('active');
        $('ul.ul-navbar a[href="' + url + '"]').addClass('active');

    // Will also work for relative and absolute hrefs
        $('ul.ul-navbar a').filter(function () {
            return this.href == url;
        }).addClass('active').parent().addClass('active').parent().parent().addClass('active');
    });