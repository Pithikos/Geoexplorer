/*
 * A thin layer for using websocket
 * */

function msg(str) {
   msgs.innerHTML += str + "\n";
   msgs.scrollTop = msgs.scrollHeight;
}

function connect() {
   var uri = 'ws://127.0.0.1:9017';
   ws = new Websock()
   ws.open(uri);
   ws.on('open', function () {
       msg("Connected to application: " + uri);
   });
   ws.on('message', function () {
       recv(ws.rQshiftStr());
   });
   ws.on('close', function () {
       disconnect();
       msg("Connection with application closed");
       msg("Restart the application and refresh this page");
   });
   $D('sendButton').disabled = false;
}


function disconnect() {
   if (ws) { ws.close(); }
   ws = null;
   $D('sendButton').disabled = true;
}

// -----------------------------------------------------------------------------

// Incoming messages
function recv(str) {
   pcs=str.split(':'); 
   action=pcs[0]
   object=pcs[1]
   
   if (action=="draw" && object=="marker"){
      coords=pcs[2].split(',')
      addMarker(coords[0], coords[1]);
   }
   
   if (action=="draw" && object=="box"){
      coords=pcs[2].split(',')
      addBox(coords[0], coords[1], coords[2], coords[3]);
   }
   
}

// Send a message to application
function send() {
   msg("Sending: " + $D('sendText').value);
   ws.send_string($D('sendText').value);
};
