new Autocomplete('#autocomplete', {
    search : input => {
        const url = `/shop/get-product/?search=${input}`

        return new Promise(resolve => {
            fetch(url)
                .then(responce=>responce.json())
                .then(data => {
                    console.log("--------------",data.payload)
                    resolve(data.payload)
                })
        })
    },
    renderResult : (result, props) => {
        let group = ''
        if (result.index % 3 === 0) {
            group = `<li class="group"> Group </li>`
        }
        return `
            <li ${props}>
                <div class="wiki-title" >
                    ${result}
                </div>
            </li>
            `
    }
})

