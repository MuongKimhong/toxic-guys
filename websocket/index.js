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
    console.log("Websocket evelopment server started")
});
