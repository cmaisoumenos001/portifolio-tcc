document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("formLogout");

    if (form) {
        form.addEventListener("submit", function (e) {

            const confirmar = confirm("Tem certeza que quer sair?");

            if (!confirmar) {
                e.preventDefault(); 
            }

        });
    }

});
