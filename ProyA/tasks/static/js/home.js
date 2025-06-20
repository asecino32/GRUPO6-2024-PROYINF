document.addEventListener('DOMContentLoaded', function() {
    // Formulario de boletines
    const boletinForm = document.getElementById('boletin-form');
    boletinForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const titulo = document.getElementById('titulo').value;
        alert(`Boletín enviado: ${titulo}`);
        // Aquí agregar lógica para enviar el boletín al servidor
    });

    // Formulario de solicitud de fuente
    const fuenteForm = document.getElementById('fuente-form');
    fuenteForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const tema = document.getElementById('tema').value;
        alert(`Solicitud de fuente: ${tema}`);
        // Aquí agregar lógica para solicitar la fuente
    });
});

