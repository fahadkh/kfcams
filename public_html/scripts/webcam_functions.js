// Variables
var ws = undefined; // websocket instance
var logs = [];
var logsLimit = 3;
var b = document.getElementById('btnWS');
var blinkstr = " ";

// Initialize the WebSocket
function initWebSocket() {
    var ipName = window.location.hostname;      //manually input wifi chip IP address to test
    if (ws) {
        ws.onclose(); // close the websocket if open.
    }
    ws = new WebSocket('ws://' + ipName + '/socket');

    ws.onopen = function () { // when handshake is complete:
        log('WebSocket open to aws server ' + ipName);
        //*** Change the text of the button to read "Stop Webcam" ***//
        document.getElementById("btnWS").innerHTML = 'Stop Webcam';
        //*** Change the title attribute of the button to display "Click to stop webcam" ***//
        document.getElementById("btnWS").title = 'Click to stop webcam';
        
        //*** Enable the button" ***//
        document.getElementById("btnWS").disabled = false;
        
        //Blink recording
        blinkstr = "Recording";
        document.getElementById("recordblink").innerHTML = blinkstr.blink();
        
    };

    ws.onclose = function () { // when socket is closed:
        log('WebSocket connection to ' + ipName + ' has been closed!');
        //*** Change the text of the button to read "Start Webcam" ***//
        document.getElementById("btnWS").innerHTML = 'Start Webcam';
        
        //*** Change the title attribute of the button to display "Click to start webcam" ***//
        
        document.getElementById("btnWS").title = 'Click to start webcam';
        
        //*** Enable the button" ***//
        document.getElementById("btnWS").disabled = false;
        
        //Turn off recording blink
        document.getElementById("recordblink").innerHTML = "";
		
        ws = undefined;
    };

    ws.onmessage = function (event) { // when client receives a WebSocket message:
        //*** Display a new timestamp ***//
        var time = new Date().getTime();
        var date = new Date(time);
        document.getElementById("timestamp").innerHTML = date.toString();
        
        //*** Set the source of the image to the image on the WiFi chip ***//
        document.getElementById("pic").src = "/images/img.png?time=" + new Date().getTime();
        
        //Blink recording
        blinkstr = "Recording";
        document.getElementById("recordblink").innerHTML = blinkstr.blink();
        
    };
	
	ws.onerror = function () { // when an error occurs
		ws.onclose();
		log('Websocket error');
		
	}
}

// Set up event listeners
//*** When the button is clicked, disable it, and depending on whether a Websocket is open or not, either run "initWebSocket()" or "ws.close()" ***//

function buttonHit() {
    document.getElementById("btnWS").disabled = true;
    if (ws) {
        ws.onclose(); // close the websocket if open.
    } else {
        initWebSocket();
    }
}

document.getElementById("btnWS").addEventListener("click", buttonHit);      //use buttonHit function


// Other functions
function log(txt) {
    logs.push({
        'content': txt,
        'type': 'log'
    });
    showLog(logs, 'log', logsLimit);
}

function showLog(logArray, logId, logLimit) {
    var logContent = '';
    var logLength = logArray.length;
    var iStart = logLength - logLimit - 1;
    if (iStart < 0) {
        iStart = 0;
    }
    for (var index = iStart; index < logLength; ++index) {
        logItem = logArray[index];
        logContent += '<span class="' + logItem.type + '">' + logItem.content + '</span><br/>\n'
    }
    document.getElementById(logId).innerHTML = logContent;
}

// Define initialization function
function init() {
    initWebSocket();
}

// Open Websocket as soon as page loads

//test code for blink
/*function blinkthat() {
    blinkstr = "Recording";
        document.getElementById("recordblink").innerHTML = blinkstr.blink();
}
window.addEventListener("load", blinkthat);*/  
window.addEventListener("load", init, false);
