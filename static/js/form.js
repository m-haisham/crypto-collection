document.querySelectorAll('form[data-partial]')
    .forEach((form) => form.addEventListener('submit', (e) => {
        e.preventDefault();
        const data = new FormData(e.target);

        let xhr = new XMLHttpRequest();
        xhr.open(
            e.target.getAttribute('method'),
            e.target.getAttribute('action'),
        )
        xhr.onload = function (event) {
            let container = document.getElementById(e.target.dataset.partial)
            if (event.target.status === 200) {
                container.innerHTML = event.target.responseText
            } else {
                container.innerHTML = e.target.dataset.onerror
                    ?? '<div class="text-danger">Uh oh. Something went wrong.</div>'
            }

        }
        xhr.onabort = function (event) {
            let container = document.getElementById(e.target.dataset.partial)
            container.innerHTML = '<i class="fas fa-exclamation-circle"></i>'
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