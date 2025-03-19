document.addEventListener("DOMContentLoaded", function () {
    let form = document.querySelector("form");
    form.addEventListener("submit", function (event) {
        let emailField = document.getElementById("id_author_email");
        if (!emailField.value.includes("@")) {
            event.preventDefault();
            alert("Lütfen geçerli bir e-posta adresi girin.");
        }
    });
});
