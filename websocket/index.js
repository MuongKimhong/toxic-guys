const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();
const server = require("http").createServer(app);
const socketIO = require("socket.io")(server, {
    cors: {
        origin: "http://localhost:8080",
        methods: ["GET", "POST"]
    }
});

const devPort = 3000;
const webSocketServerDomain = "http://localhost:3000";

// enable cors for all origins
app.use(cors("*"))

// tell server to accept json format
app.use(express.json())

// listening to the port
server.listen(devPort, () => {
    console.log("Websocket development server started")
});

// use socket.emit so that client emitter can receive 
// use socket.broadcast so that other clients beside emiiter can receive


socketIO.on("connection", (socket) => {

    // listen to friend request
    socket.on("send-connection-request", (userToBeConnectedId) => {
        socket.broadcast.emit("connection-request", userToBeConnectedId);
    })

    socket.on("connection-accepted", (requestSenderId) => {
        socket.broadcast.emit("accepted", requestSenderId);
    })

    socket.on("send-message", (message) => {
        socket.broadcast.emit("new-message", message);
    })

    socket.on("group_invitation", (invitedUserIds) => {
        socket.broadcast.emit("group-invitation-sent", invitedUserIds);
    })
})