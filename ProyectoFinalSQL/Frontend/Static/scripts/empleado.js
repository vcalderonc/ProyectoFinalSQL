// static/scripts/empleado.js

function buscarEmpleado() {
  const codigo = document.getElementById("codigoEmpleado").value.trim();
  const contenedor = document.getElementById("resultadoEmpleado");
  contenedor.innerHTML = "";

  if (!codigo) {
    contenedor.innerHTML = "<p>Por favor ingresa un código válido.</p>";
    return;
  }

  fetch(`/empleado/info?codigo=${codigo}`)
    .then(res => res.json())
    .then(data => {
     if (data.length === 0) {
  showErrorModal("No se encontró ningún empleado con ese código.");
  return;
}


      const emp = data[0];
      contenedor.innerHTML = `
        <div class="empleado-card">
          <h2>👨‍💼 ${emp.nombre_empleado}</h2>
          <p><strong>Código:</strong> ${emp.codigo_empleado}</p>
          <p><strong>Cargo:</strong> ${emp.nombre_cargo}</p>
          <p><strong>Dependencia:</strong> ${emp.nombre_dependencia}</p>
          <p><strong>Sueldo:</strong> $${emp.sueldo}</p>
          <p><strong>EPS:</strong> ${emp.nombre_eps}</p>
          <p><strong>ARL:</strong> ${emp.nombre_arl}</p>
          <p><strong>Pensión:</strong> ${emp.nombre_pension}</p>
          <hr>
          <p><strong>Días trabajados:</strong> ${emp.dias_trabajados}</p>
          <p><strong>Bonificación:</strong> $${emp.bonificacion}</p>
          <p><strong>Transporte:</strong> $${emp.transporte}</p>
          <hr>
          <p><strong>Vacaciones:</strong> ${emp.vac_inicio || "-"} a ${emp.vac_fin || "-"}</p>
          <p><strong>Incapacidad:</strong> ${emp.inc_inicio || "-"} a ${emp.inc_fin || "-"} (${emp.tipo_incapacidad || "-"})</p>
          <div class="boton-pdf-container">
            <button class="boton-pdf" onclick="descargarPDF('${emp.codigo_empleado}')">
              📄 Descargar PDF
            </button>
          </div>
        </div>
      `;
    })
    .catch(error => {
      console.error("Error al buscar empleado:", error);
      contenedor.innerHTML = "<p>Ocurrió un error al consultar la información.</p>";
    });
}

function descargarPDF(codigo) {
  window.open(`/empleado/nomina_pdf?codigo=${codigo}`, '_blank');
}
function showErrorModal(message) {
  const modal = document.getElementById("errorModal");
  const messageContainer = document.getElementById("errorMessage");
  messageContainer.textContent = message;
  modal.style.display = "flex";
}

function closeErrorModal() {
  document.getElementById("errorModal").style.display = "none";
}

// Cierra si se hace clic fuera del modal
window.addEventListener("click", function (event) {
  const modal = document.getElementById("errorModal");
  if (event.target === modal) {
    modal.style.display = "none";
  }
});
