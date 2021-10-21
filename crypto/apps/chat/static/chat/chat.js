
function alpineData() {
    const messageInput = document.querySelector('input[name="message"]')
    const keyInput = document.querySelector('input[name="key"]')
    const secretInput = document.querySelector('input[name="secret"]')

    function isBottom() {
      const { scrollHeight, scrollTop, clientHeight } = document.scrollingElement;
      const distanceFromBottom = scrollHeight - scrollTop - clientHeight;
      return distanceFromBottom < 100; // adjust the number 20 yourself
    }

    function setObserver() {
        const chatNode = document.querySelector('#messages')
        function callback(mutations) {
            if (!isBottom()) {
                return;
            }

            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'instant',
            });
        }

        const observer = new MutationObserver(callback);
        observer.observe(chatNode, { attributes: true, childList: true, subtree: true });
    }

    return {
        socket: null,

        order: [],
        messages: {},

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
                const message = JSON.parse(e.data);

                this.order = [...this.order, message.id,]
                this.messages[message.id] = {
                    ...message,
                    hasSecret: null,
                    secret: '',
                };

                window.scrollTo(0,document.body.scrollHeight);
            }

            this.socket.onerror = () => {
                this.status = {
                    connected: false,
                    message: 'Connection was terminated unexpectedly.'
                }
            }

            messageInput.focus()
            setObserver()
        },
        send: function () {
            let message = this.inputs.message;

            if (this.inputs.key && this.inputs.secret) {
                const bitstring = this.cipher.encode(this.inputs.secret)
                message = hide(message, bitstring)
            }

            this.socket.send(JSON.stringify({message}))
        },
        messageData: function (id) {
            const self = this;
            const message = this.messages[id];

            return {
                message,
                showSecret: function () {
                    const [original, bitstring] = reveal(this.message.text)

                    if (!bitstring) {
                        this.message = {...this.message, hasSecret: false, secret: 'No secret within'};
                        return;
                    }

                    const secret = self.cipher.decode(bitstring)
                    this.message = {...this.message, hasSecret: true, secret}
                },
            }
        },

        // UTILITY METHODS

        focus: {
            message: messageInput.focus,
            key: keyInput.focus,
            secret: secretInput.focus,
        }
    }
}

