/*
 * A thin layer for using websocket
 * */

function msg(str) {
   msgs.innerHTML += str + "\n";
   msgs.scrollTop = msgs.scrollHeight;
}

function connect() {
   var uri = $D('target').value;
   ws = new Websock()
   msg("connecting to: " + uri);
   ws.open(uri);
   ws.on('open', function () {
       msg("Connected");
   });
   ws.on('message', function () {
       msg("Received: " + ws.rQshiftStr());
   });
   ws.on('close', function () {
       disconnect();
       msg("Disconnected");
   });

   $D('connectButton').value = "Disconnect";
   $D('connectButton').onclick = disconnect;
   $D('sendButton').disabled = false;
}

function disconnect() {
   if (ws) { ws.close(); }
   ws = null;

   $D('connectButton').value = "Connect";
   $D('connectButton').onclick = connect;
   $D('sendButton').disabled = true;
}

function send() {
   msg("Sending: " + $D('sendText').value);
   ws.send_string($D('sendText').value);
};
