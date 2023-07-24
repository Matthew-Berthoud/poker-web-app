document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    // connect event
    // socket.on('connect', () => {
    //     socket.send("I am connected"); // send function goes to 'message' bucket by default
    // });

    socket.on('message', data => {
        const p = document.createElement('p');
        const span_timestamp = document.createElement('span');
        span_timestamp.innerHTML = data.time
        p.innerHTML = data.username + ' ' + data.action + ' ' + span_timestamp.outerHTML;
        document.querySelector('#seats').append(p);
    });

    socket.on('some-event', data => {
        console.log(data);
    });

    // Send user input to server
    document.querySelector('#fold').onclick = () => {
        socket.send({'username': username, 'player_id': player_id, 'action': 'fold'});
    }
});