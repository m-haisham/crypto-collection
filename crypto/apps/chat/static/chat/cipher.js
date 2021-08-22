/**
 * Function that converts a string into its binary representation
 *
 * @author https://github.com/mensch272
 */
function stringToBinary(string) {
    let output = "";
    let binary;
    for (let i = 0; i < string.length; i++) {
        binary = string.charCodeAt(i).toString(2);
        output += "00000000".slice(binary.length % 8) + binary;
    }

    return output;
}

/**
 * Function that converts a binart string into string
 *
 * @author https://github.com/mensch272
 */
function binaryToString(binary) {
    const cleanBinary = binary
        .replace(/\s+/g, "")
        .match(/.{1,8}/g)
        .join(" ");

    var newBinary = cleanBinary.split(" ");
    var binaryCode = [];

    for (let i = 0; i < newBinary.length; i++) {
        binaryCode.push(String.fromCharCode(parseInt(newBinary[i], 2)));
    }

    return binaryCode.join("");
}

/**
 * Function that converts a 32-bit integer into string
 */
function int32ToBinary(nMask) {
    // nMask must be between -2147483648 and 2147483647
    for (
        var nFlag = 0, nShifted = nMask, sMask = "";
        nFlag < 32;
        nFlag++, sMask += String(nShifted >>> 31), nShifted <<= 1
    );

    return sMask;
}

/**
 * Function that creates a binary keystream from the seed
 *
 * uses the pseudo-random number generator [seedrandom]
 * @link https://github.com/davidbau/seedrandom
 *
 * @param {string} seed
 * @param {number} length minimum length of the keystream
 * @author https://github.com/mensch272
 * @returns bitstream
 */
function createKeystream(seed, length = 512) {
    const rng = new Math.seedrandom(seed);
    let stream = "";

    while (stream.length < length) {
        stream += int32ToBinary(rng.int32());
    }

    return stream;
}

class StreamCipher {
    constructor(secret) {
        this.secret = secret;
        this.keystream = createKeystream(secret, 1024);
    }

    /**
     * Private function that runs xor operation against the input and keystream
     *
     * @author https://github.com/mensch272
     */
    _xor(bitstring) {
        const output = [];
        for (let i = 0; i < bitstring.length; i++) {
            output.push(bitstring[i] ^ this.keystream[i]);
        }

        return output.join("");
    }

    /**
     * Public function that encodes the given plaintext into binary
     * by applying xor operation again the keystream
     *
     * @author https://github.com/mensch272
     */
    encode(plaintext) {
        const binary = stringToBinary(plaintext);
        return this._xor(binary);
    }

    /**
     * Public function that converts the encoded binary into string
     * by applying xor operation again the keystream
     *
     * @author https://github.com/mensch272
     */
    decode(binary) {
        const decoded = this._xor(binary);
        return binaryToString(decoded);
    }
}

// source: https://blog.bitsrc.io/how-to-hide-secrets-in-strings-modern-text-hiding-in-javascript-613a9faa5787
const characters = {
    "00": "\u200C",
    "01": "\u200D",
    10: "\u2060",
    11: "\u2062",
};
const invisible = Object.entries(characters).reduce(
    (acc, [key, val]) => ({ ...acc, [key]: val, [val]: key }),
    {}
);

/**
 * Function that hides the bitstring inside the unconcealed message.
 *
 * This function returns new message with the bitstring hidden within it.
 *
 * @author https://github.com/mensch272
 */
function hide(str, bitstring) {
    const output = [];
    for (let i = 0; i < bitstring.length; i += 2) {
        output.push(invisible[bitstring.substring(i, i + 2)]);
    }

    const hidden = output.join("");

    if (str.includes(" ")) {
        return str.replace(/ /, " " + hidden);
    } else {
        return str.substring(0, 1) + hidden + str.substring(1);
    }
}

/**
 * Function that isolates the hidden characters and converts them to their bitstring representation.
 *
 * This function return the original unconcealed message without the secret and the hidden bitstring
 *
 * @author https://github.com/mensch272
 */
function reveal(str) {
    const parts = str.includes(" ") ? str.split(" ")[1] : str.substring(1);

    const hidden = [];
    const output = [];
    for (let i = 0; i < parts.length; i++) {
        const char = parts[i];
        const bits = invisible[char];

        if (bits == null) {
            break;
        }

        output.push(bits);
        hidden.push(char);
    }

    return [str.replace(hidden.join(""), ""), output.join("")];
}
