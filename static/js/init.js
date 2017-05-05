$(document).ready(function () {
    // namespace = '/test';
    namespace = document.location.pathname;
    if (namespace == "/") {
        var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
        console.log(socket);
        console.log("test namespace");
    }
    else {
        var socket = io.connect('http://' + document.domain + ':' + location.port + document.location.pathname);
        console.log(socket);
        console.log("custom namespace");
    }

    socket.on('my response', function (msg) {
        $('#board').val(msg.data);
    });

    $('#room').change(function (event) {
        socket.emit('join', {room: $('#room').val()});
        return false;
    });

    $('#board').change(function (event) {
        socket.emit('my broadcast event', {data: $('#board').val()});
        return false;
    });
});

document.getElementById("copyButton").addEventListener("click", function() {
    copyToClipboard(document.getElementById("board"));
});

function copyToClipboard(elem) {
    // create hidden text element, if it doesn't already exist
    var targetId = "_hiddenCopyText_";
    var isInput = elem.tagName === "INPUT" || elem.tagName === "TEXTAREA";
    var origSelectionStart, origSelectionEnd;
    if (isInput) {
        // can just use the original source element for the selection and copy
        target = elem;
        origSelectionStart = elem.selectionStart;
        origSelectionEnd = elem.selectionEnd;
    } else {
        // must use a temporary form element for the selection and copy
        target = document.getElementById(targetId);
        if (!target) {
            var target = document.createElement("textarea");
            target.style.position = "absolute";
            target.style.left = "-9999px";
            target.style.top = "0";
            target.id = targetId;
            document.body.appendChild(target);
        }
        target.textContent = elem.textContent;
    }
    // select the content
    var currentFocus = document.activeElement;
    target.focus();
    target.setSelectionRange(0, target.value.length);
    
    // copy the selection
    var succeed;
    try {
        succeed = document.execCommand("copy");
    } catch (e) {
        succeed = false;
    }
    // restore original focus
    if (currentFocus && typeof currentFocus.focus === "function") {
        currentFocus.focus();
    }
    
    if (isInput) {
        // restore prior selection
        elem.setSelectionRange(origSelectionStart, origSelectionEnd);
    } else {
        // clear temporary content
        target.textContent = "";
    }
    return succeed;
}

var now = new Date();
var hh = now.getHours();
var mm = now.getMinutes()
var da = now.getDate()
var mo = now.getMonth()
var yyyy = now.getFullYear()
var datetime = hh + '' + mm + '-' + mo + '-' + da + '-' + yyyy;
var container = document.querySelector('textarea');
var anchor = document.getElementById("downloadButton");

anchor.onclick = function() {
    anchor.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(container.value);
    anchor.download = 'clippy-' + datetime + '.txt';
};