
function alpineData() {
    const messageInput = document.querySelector('input[name="message"]')
    const keyInput = document.querySelector('input[name="message"]')
    const secretInput = document.querySelector('input[name="message"]')

    return {
        socket: null,
        messages: [],
        status: {
            connected: false,
            message: 'Attempting to join',
        },

        inputs: {
            message: '',
            key: '',
            secret: '',
        },

        _cipher: null,
        get cipher() {
            if (this._cipher == null || this._cipher.secret !== this.inputs.key) {
                this._cipher = new StreamCipher(this.inputs.key)
            }

            return this._cipher;
        },

        alpineInit: function () {
            const roomInfo = JSON.parse(document.getElementById('room-info').textContent);
            const roomName = roomInfo['room_name'];
            const alias = roomInfo['alias'];

            const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
            this.socket = new WebSocket(`${protocol}://${window.location.host}/ws/chat/${roomName}/?alias=${alias}`)

            this.socket.onopen = () => {
                this.status = {
                    connected: true,
                    message: '',
                }
            }

            this.socket.onmessage = (e) => {
                this.messages = [
                    ...this.messages,
                    {
                        ...JSON.parse(e.data),
                        secret: null,
                    }
                ]
            }

            this.socket.onerror = () => {
                this.status = {
                    connected: false,
                    message: 'Connection was terminated unexpectedly.'
                }
            }

            messageInput.focus()
        },
        send: function () {
            let message = this.inputs.message;

            if (this.inputs.key && this.inputs.secret) {
                const bitstring = this.cipher.encode(this.inputs.secret)
                message = hide(message, bitstring)
            }

            this.socket.send(JSON.stringify({message}))
        },
        showSecret: function (message) {
            const [original, bitstring] = reveal(message.text)

            if (!bitstring) {
                alert('No secret was found in the message.')
                return;
            }

            const secret = this.cipher.decode(bitstring)
            alert(secret)
        },

        // UTILITY METHODS

        focus: {
            message: messageInput.focus,
            key: keyInput.focus,
            secret: secretInput.focus,
        }
    }
}