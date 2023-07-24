document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    // connect event
    socket.on('connect', () => {
        socket.send("I am connected"); // send function goes to 'message' bucket by default
    });

    socket.on('message', data => {
        console.log(`Message recieved: ${data}`)
    });

    socket.on('some-event', data => {
        console.log(data);
    });


    document.querySelectorAll('.inputs').onclick = () => {
        if 
        socket.send("fold")
    }
});