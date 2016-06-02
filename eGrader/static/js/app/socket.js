import io from 'socket.io-client'


class SocketManager {
    constructor() {
        this.namespace = '/grader/soc';
        if (location.port) {
            this.rootUrl = location.protocol + '//' + document.domain + ':' + location.port + this.namespace;
        } else {
            this.rootUrl = location.protocol + '//' + document.domain + this.namespace;
        }
        this.connect();
    }
    
    connect() {
        let self = this;
        this.socket = io.connect(this.rootUrl);

        this.socket.on('connection', function(msg) {
            self.sessionId = msg['session_id'];
            console.log(self.sessionId)
        })
    }

    getSocket() {
        return this.socket
    }
    
    getSessionId() {
        return this.sessionId
    }
}

export default SocketManager;
