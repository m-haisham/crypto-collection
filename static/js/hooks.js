function useInnerHTML(id) {
    let element = document.getElementById(id);

    return [
        () => element?.innerHTML,
        (html) => {
            if (element != null) element.innerHTML = html
        },
    ]
}

function useHidden(id) {
    let element = document.getElementById(id);
    console.log({id, element})

    return [
        () => element == null || element.getAttribute('hidden') != null,
        (hide) => {
            if (element == null) return;

            if (hide) {
                element.setAttribute('hidden', '')
            } else {
                element.removeAttribute('hidden')
            }
        }
    ]
}

function useAttribute(selector, attribute) {
    let elements = document.querySelectorAll(selector)

    return [
        () => elements.map(element => element.getAttribute(attribute)),
        (value) => elements.forEach(element => element.setAttribute(attribute, value)),
        () => elements.forEach(element => element.removeAttribute(attribute)),
    ]
}