document.addEventListener('DOMContentLoaded', () => {
    
    // Show bet size next to slider
    let bet_slider = document.querySelector('#bet-slider');
    bet_slider.addEventListener("input", function() {
        let slider_label = document.querySelector('#slider-value');
        slider_label.innerHTML = bet_slider.value;
    })
    
    var socket = io();




    socket.on('connect', () => {
        socket.emit('connected');
    });

    socket.on('disconnect', () => {
        socket.emit('disconnected');
    });


    socket.on('player_joined', (player, seat_num) => {
        console.log(`${player.username} joined seat ${seat_num}`);
    });

    socket.on('global_notification', data => {
        console.log(`global_notif: ${data}`);
    });

    // display incoming messages
    socket.on('message', data => {
        console.log(`message: ${data}`);
        if (data == 'fully_disconnected') {
            window.location.href = '/';
        }
    });


    // Send quit button input to server
    document.querySelector('#quit').onclick = () => {
        socket.emit('disconnected');
    };

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

