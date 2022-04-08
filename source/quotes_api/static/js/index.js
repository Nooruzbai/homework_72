async function make_request(url, context) {
    let response = await fetch(url, context);
    console.log(response)
    if (response.ok) {
        console.log('OK')
        return await response.json();
    } else {
        console.log('Not Successful')
        let error = new Error(response.statusText);
        error.response = response;
        error_res = await response.json()
        console.log(error_res.error)
        return error_res;
    }
}

// Getting CSRFToken
let get_csrf_token = async function () {
    let url = "api/get-csrf-token/"
    let request_csrf_token = await make_request(url, {method: "GET"});
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


get_csrf_token();
let csrf_token = getCookie('csrftoken');


// Getting all the quotes
let get_quotes = async function (event) {
    let url = '/get/quotes/';


    if (document.getElementById('container1')) {
        let form = document.getElementById('container1')
        form.hidden = true
    }
    if (document.getElementById('innerDiv')) {
        let reapeted_div = document.getElementById('innerDiv')
        reapeted_div.remove()
    }

    let main_container = document.getElementById('container')
    let inner_div = document.createElement('div')
    inner_div.id = "innerDiv"
    main_container.appendChild(inner_div)
    // let url = event.target.dataset.articlesUrl;
    let data = await make_request(url, {method: "GET"})

    for (let i = 0; i < data.length; i++) {
        let quote_result = quote(data[i].id, data[i].text, data[i].name, data[i].email, data[i].ranking, data[i].status, data[i].data_created)
        inner_div.appendChild(quote_result)

    }


// Hanging event to buttons to see details
    const buttons = document.querySelectorAll('.button_for_detail');
    const delete_buttons = document.querySelectorAll('.delete_buttons')

    buttons.forEach(button => {
        button.addEventListener('click', (e) => quote_details(e))
    });

    delete_buttons.forEach(button => {
        button.addEventListener('click', (e) => delete_quote(e))
    });

    const plus_buttons = document.querySelectorAll('.plus_buttons')
    const minus_buttons = document.querySelectorAll('.minus_buttons')
    console.log(plus_buttons)

    plus_buttons.forEach(button => {
        button.addEventListener('click', (e) => math_button(e))
    });

    minus_buttons.forEach(button => {
        button.addEventListener('click', (e) => math_button(e))
    });

}

// Function to create quote
let create_quote = async function (event) {
    let url = event.target.dataset.quoteUrl


    let main_container = document.getElementById('container1');

    let text = document.getElementById('text').value;
    let name = document.getElementById('name').value;
    let email = document.getElementById('email').value;

    let data = JSON.stringify({"text": text, "name": name, "email": email})
    let request_data = await make_request(url, {
        method: "POST",
        body: data,
        headers: {"Content-type": "application/json", "X-CSRFToken": csrf_token}
    })

    get_quotes()
    console.log(data)
}


// Base function to see one quote
function quote(id, text, name, email, ranking, status) {

    let div_for_quote = document.createElement('div')

    let quote_text = document.createElement("p")
    quote_text.innerText = `${text}`
    let quote_name = document.createElement('p')
    quote_name.innerText = `${name}`
    let quote_email = document.createElement('p')
    quote_email.innerText = `${email}`


    let quote_ranking = document.createElement('p')
    quote_ranking.innerText = `${ranking}`
    quote_ranking.id = id

    let minus_button = document.createElement('button')
    minus_button.className = "minus_buttons"
    minus_button.innerText = "-"
    minus_button.style.color = "red"
    minus_button.dataset.number = id
    minus_button.dataset.sign = "-"

    let plus_button = document.createElement('button')
    plus_button.className = "plus_buttons"
    plus_button.innerText = "+"
    plus_button.style.color = "red"
    plus_button.dataset.number = id
    plus_button.dataset.sign = "+"


    let quote_status = document.createElement('p')
    quote_status.innerText = `${status}`
    let detail_view_button = document.createElement('button')
    detail_view_button.innerText = "Details"
    detail_view_button.className = "button_for_detail"
    detail_view_button.dataset.number = id
    let delete_button = document.createElement("button")
    delete_button.innerText = "Delete"
    delete_button.className = "delete_buttons"
    delete_button.dataset.number = id


    div_for_quote.appendChild(quote_text)
    div_for_quote.appendChild(quote_name)
    div_for_quote.appendChild(quote_email)
    div_for_quote.appendChild(quote_ranking)
    div_for_quote.appendChild(minus_button)
    div_for_quote.appendChild(plus_button)
    div_for_quote.appendChild(quote_status)
    div_for_quote.appendChild(detail_view_button)
    div_for_quote.appendChild(delete_button)
    console.log(div_for_quote)
    return div_for_quote
}

// Function to see a quote_form
let get_quote_form = function (event) {

    if (document.getElementById('innerDiv')) {
        let remove_element = document.getElementById("innerDiv")
        remove_element.remove()
    }

    if (document.getElementById('quote_detail')) {
        let repeated_element = document.getElementById('quote_detail')
        repeated_element.remove()

    }
    let quote_form = document.getElementById('container1')
    quote_form.hidden = false
};


// Function to see quote detail
let quote_details = async function (event) {

    let quote_id = parseInt(event.target.dataset.number)
    let url = `/quotes/${quote_id}/`;
    let data = await make_request(url, {method: "GET"})
    console.log(data)

    if (document.getElementById('innerDiv')) {
        let remove_element = document.getElementById("innerDiv")
        remove_element.remove()
    }

    if (document.getElementById('quote_detail')) {
        let repeated_element = document.getElementById('quote_detail')
        repeated_element.remove()

    }

    let container = document.getElementById('container')
    let quote_detail = document.createElement('div')
    quote_detail.id = 'quote_detail'
    let div_for_quote = quote(data.id, data.text, data.name, data.email, data.ranking, data.status, data.date_created)
    quote_detail.appendChild(div_for_quote)
    container.appendChild(quote_detail)

}

// Function to delete a quote
let delete_quote = async function (event) {

    let quote_id = parseInt(event.target.dataset.number)
    let url = `/quotes/${quote_id}/`;
    let data = await make_request(url, {
        method: "DELETE",
        headers: {"Content-type": "application/json", "X-CSRFToken": csrf_token}
    })

    get_quotes()
}

let math_button = async function (event) {
    let quote_id = parseInt(event.target.dataset.number)
    let url = `quote/ranking/${quote_id}/`
    let sign = event.target.dataset.sign
    console.log(sign)
    let data = JSON.stringify({"sign": sign})
    console.log(event.target.dataset.plus)

    let request_data = await make_request(url, {
        method: "POST",
        body: data,
        headers: {"Content-type": "application/json", "X-CSRFToken": csrf_token}
    })


    let ranking = document.getElementById(`${quote_id}`)
    console.log(request_data)
    ranking.innerText = `${request_data.ranking}`


}


let quotes_form = document.getElementById('add_quote_form')
quotes_form.addEventListener("click", get_quote_form)


let quotes_list = document.getElementById('quotes_list')
quotes_list.addEventListener("click", get_quotes)



