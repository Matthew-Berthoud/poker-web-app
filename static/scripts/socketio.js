document.addEventListener('DOMContentLoaded', () => {
    
    // Show bet size next to slider
    let bet_slider = document.querySelector('#bet-slider');
    bet_slider.addEventListener("input", function() {
        let slider_label = document.querySelector('#slider-value');
        slider_label.innerHTML = bet_slider.value;
    })
    

    var socket = io();

    // connect event: Player 
    socket.on('connect', () => {
        socket.send("I am connected"); // send function goes to 'message' bucket by default
    });

    socket.on('global_notification', data => {
        console.log(`sent via global_notification event from server to this client: ${data}`);
    });

    // display incoming messages
    socket.on('message', data => {
        console.log(`sent via message event from server to this client: ${data}`);
        // const p = document.createElement('p');
        // const span_timestamp = document.createElement('span');
        // span_timestamp.innerHTML = data.time_stamp
        // p.innerHTML = data.username + ' ' + data.action + ' ' + span_timestamp.outerHTML;
        // document.querySelector('#seats').append(p);
    });

    // Send action button input to server
    document.querySelector('#fold').onclick = () => {
        socket.emit('action_button', action='fold', slider=bet_slider.value, player=client);
    };
    document.querySelector('#check-or-call').onclick = () => {
        socket.emit('action_button', action='checkcall', slider=bet_slider.value, player=client);
    };
    document.querySelector('#bet-or-raise').onclick = () => {
        socket.emit('action_button', action='betraise', slider=bet_slider.value, player=client);
    };
});

