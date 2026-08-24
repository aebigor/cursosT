// Validación simple en el cliente antes de enviar el formulario
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".query-form");
    if (!form) return;

    form.addEventListener("submit", (e) => {
        const tipo = form.querySelector("#tipo_documento").value;
        const numero = form.querySelector("#numero_documento").value.trim();

        if (!tipo || !numero) {
            e.preventDefault();
            alert("Debe seleccionar el tipo e ingresar el número de documento.");
        }
    });
});
