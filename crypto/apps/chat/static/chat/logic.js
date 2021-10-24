let _cipher = null;

function cipher(key) {
    if (_cipher == null || _cipher.secret !== key) {
        _cipher = new StreamCipher(key)
    }

    return _cipher;
}

function alpineHideData() {

    return {
        content: {
            message: '',
            key: '',
            secret: '',
        },

        result: null,
        error: null,

        submit: function () {
            if (this.content.message.length === 0) {
                this.error = "Message must not be empty.";
            } else if (this.content.key.length === 0) {
                this.error = "Key must not be empty.";
            } else if (this.content.secret.length === 0) {
                this.error = "Secret message must not be empty.";
            } else {
                this.error = null;
            }

            if (this.error != null) return;

            const bitstring = cipher(this.content.key).encode(this.content.secret);
            this.result = hide(this.content.message, bitstring)
        },

        clip: function (text) {
            navigator.clipboard.writeText(text)
        }
    }
}

function alpineShowData() {

    return {
        encoded: '',
        key: '',

        result: null,
        error: null,

        submit: function () {
            if (this.encoded.length === 0) {
                this.error = 'Encoded message must not be empty';
            } else if (this.key.length === 0) {
                this.error = 'Key must not be empty.'
            } else {
                this.error = null;
            }

            if (this.error != null) return;

            const [original, bitstring] = reveal(this.encoded)
            if (!bitstring) {
                this.error = 'Could not find any secret messages';
                return;
            }

            const decoded = cipher(this.key).decode(bitstring);
            this.result = {original, decoded}
        },

        intoClip: function () {
            if (this.result == null) {
                return;
            }

            navigator.clipboard.writeText(this.result.decoded)
        },
    }
}