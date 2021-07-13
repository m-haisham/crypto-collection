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

    return [
        () => element != null && element.getAttribute('hidden') != null,
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

document.querySelectorAll('form[data-partial]')
    .forEach((form) => form.addEventListener('submit', (e) => {
        e.preventDefault();
        const data = new FormData(e.target);

        // remove any previous
        const [getInnerHTML, setInnerHTML] = useInnerHTML(e.target.dataset.partial);
        const [isWaitingHidden, setWaitingHidden] = useHidden(form.getAttribute('data-partial-waiting'))

        setInnerHTML('')
        setWaitingHidden(false)

        let xhr = new XMLHttpRequest();
        xhr.open(
            e.target.getAttribute('method'),
            e.target.getAttribute('action'),
        )
        xhr.onload = function (event) {
            let html
            switch (event.target.status) {
                case 200:
                    html = event.target.responseText
                    break
                default:
                    html = e.target.dataset.onerror
                        ?? '<div class="text-danger">Uh oh. Something went wrong.</div>'
                    break;
            }

            setInnerHTML(html)
            setWaitingHidden(true)
        }
        xhr.onabort = function (event) {
            setInnerHTML('<i class="fas fa-exclamation-circle"></i>')
            setWaitingHidden(true)
        }

        xhr.send(data)
    }
));

document.querySelectorAll('input[pattern][data-block-pattern]')
    .forEach((form) => {
        let patternValue = form.getAttribute('pattern')
        if (patternValue == null) return;

        let pattern = new RegExp(`(?!${patternValue}).`, 'g')
        form.addEventListener('input', (e) => {
                e.preventDefault();
                e.target.value = e.target.value.replace(pattern, '')
            }
        );
    });