document.querySelectorAll('form[data-partial]')
    .forEach((form) => form.addEventListener('submit', (e) => {
        e.preventDefault();
        const data = new FormData(e.target);

        const [getInnerHTML, setInnerHTML] = useInnerHTML(e.target.dataset.partial);
        const [isErrorHidden, setErrorHidden] = useHidden(e.target.dataset.partialError)
        const [isWaitingHidden, setWaitingHidden] = useHidden(e.target.dataset.partialWaiting)

        setErrorHidden(true)
        setWaitingHidden(false)
        if (!isWaitingHidden()) setInnerHTML('')

        let xhr = new XMLHttpRequest();
        xhr.open(
            e.target.getAttribute('method'),
            e.target.getAttribute('action'),
        )
        xhr.onabort = function (event) {
            setInnerHTML('')
            setErrorHidden(false)
            setWaitingHidden(true)
        }

        xhr.onload = function (event) {
            switch (event.target.status) {
                case 200:
                    setInnerHTML(event.target.responseText)
                    setWaitingHidden(true)
                    setErrorHidden(true)
                    break
                default:
                    xhr.onabort(event)
                    break;
            }

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

document.querySelectorAll('input.custom-file-input')
    .forEach((form) => form.addEventListener('change', (e) => {
        const fileName = e.target.files[0].name;
        const id = e.target.getAttribute('id')

        document.querySelector(`label[for="${id}"]`).innerText = fileName
    }))