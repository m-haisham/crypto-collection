document.querySelectorAll('form[data-partial]')
    .forEach((form) => form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = new FormData(e.target);

        const [getInnerHTML, setInnerHTML] = useInnerHTML(e.target.dataset.partial);
        const [isErrorHidden, setErrorHidden] = useHidden(e.target.dataset.partialError)
        const [isWaitingHidden, setWaitingHidden] = useHidden(e.target.dataset.partialWaiting)

        setErrorHidden(true)
        setWaitingHidden(false)
        if (!isWaitingHidden()) setInnerHTML('')

        const abort = () => {
            setInnerHTML('')
            setErrorHidden(false)
            setWaitingHidden(true)
        }

        try {
            const response = await fetch(
                e.target.getAttribute('action'),
                {
                    method: e.target.getAttribute('method'),
                    body: data,
                },
            );

            switch (response.status) {
                case 200:
                    setInnerHTML(await response.text())
                    setWaitingHidden(true)
                    setErrorHidden(true)
                    break
                default:
                    abort()
                    break;
            }
        } catch (e) {
            abort()
        }
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
