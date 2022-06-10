// functions to fetch accordingly form html and display inside the form container

const formContainer = document.querySelector('#form-container');

document.querySelector('#update-user-details').addEventListener('click', handleButtonClick);

document.querySelectorAll('.update-address').forEach(button => {
    button.addEventListener('click', handleButtonClick);
});

async function handleButtonClick(e) {
    e.preventDefault();
    const url = e.target.getAttribute('data-url');
    let formHtml = await fetch(url).then(res => res.text());
    formContainer.innerHTML = formHtml;
    formContainer.scrollIntoView({ behavior: 'smooth' });
}