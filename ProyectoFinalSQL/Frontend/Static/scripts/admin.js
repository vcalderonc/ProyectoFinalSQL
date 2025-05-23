 // Mostrar/ocultar menú lateral
      function toggleMenu() {
          const menu = document.getElementById("side-menu");
          menu.classList.toggle("show");
      }

      // Abrir y cerrar modal de crear
      function abrirModal() {
          document.getElementById("modalCrearEmpleado").style.display = "flex";
      }

      function cerrarModal() {
          document.getElementById("modalCrearEmpleado").style.display = "none";
      }

      // Abrir y cerrar modal de editar
      function cerrarModalEditar() {
          document.getElementById("modalEditarEmpleado").style.display = "none";
      }

      function editarEmpleado(codigo) {
          fetch(`/empleado/info?codigo=${codigo}`)
              .then(r => r.json())
              .then(data => {
                  const emp = data[0];
                  document.getElementById("editCodigo").value = emp.codigo_empleado;
                  document.getElementById("editNombre").value = emp.nombre_empleado;
                  document.getElementById("editApellido").value = emp.apellido_empleado;
                  document.getElementById("editFecha").value = emp.fecha_ingreso;
                  document.getElementById("editDependencia").value = emp.id_dependencia;
                  document.getElementById("editCargo").value = emp.id_cargo;
                  document.getElementById("editEps").value = emp.id_eps;
                  document.getElementById("editArl").value = emp.id_arl;
                  document.getElementById("editPension").value = emp.id_pension;
                  document.getElementById("editSueldo").value = emp.sueldo;

                  document.getElementById("modalEditarEmpleado").style.display = "flex";
              });
      }

      // Abrir y cerrar modal de novedad
      function abrirModalNovedad() {
          document.getElementById("modalNovedad").style.display = "flex";
      }

      function cerrarModalNovedad() {
          document.getElementById("modalNovedad").style.display = "none";
      }

      // Ocultar modales al hacer clic fuera
      window.onclick = function(event) {
          const modalCrear = document.getElementById("modalCrearEmpleado");
          const modalEditar = document.getElementById("modalEditarEmpleado");
          const modalNovedad = document.getElementById("modalNovedad");

          if (event.target === modalCrear) modalCrear.style.display = "none";
          if (event.target === modalEditar) modalEditar.style.display = "none";
          if (event.target === modalNovedad) modalNovedad.style.display = "none";
      }

      // Mostrar/ocultar secciones de vacaciones e incapacidad
      function toggleSeccion(id) {
          const seccion = document.getElementById(id);
          seccion.style.display = (seccion.style.display === "none" || seccion.style.display === "") ? "block" : "none";
      }

      // Buscar empleado
      function buscarEmpleado() {
      const codigo = document.getElementById("codigoEmpleado").value;
      fetch(`/empleado/info?codigo=${codigo}`)
        .then(r => r.json())
        .then(data => {
          const contenedor = document.getElementById("resultadoEmpleado");
          contenedor.innerHTML = "";

          if (!data || data.length === 0) {
            contenedor.innerHTML = "<p>No se encontraron datos para ese código.</p>";
            return;
          }

          const emp = data[0];
          contenedor.innerHTML = `
            <div style="background-color:#111; padding:20px; border-radius:16px; box-shadow:0 0 10px rgba(255,255,255,0.05);">
              <h3 style="font-size:20px; color:#6a6aff; margin-bottom:20px;">👤 Información del Empleado</h3>
              <div style="display: grid; grid-template-columns: 1fr 2fr; row-gap: 10px;">
                <p><strong>Código:</strong></p><p>${emp.codigo_empleado}</p>
                <p><strong>Nombre:</strong></p><p>${emp.nombre_empleado}</p>
                <p><strong>Cargo:</strong></p><p>${emp.nombre_cargo}</p>
                <p><strong>Dependencia:</strong></p><p>${emp.nombre_dependencia}</p>
                <p><strong>Sueldo:</strong></p><p>$${emp.sueldo}</p>
                <p><strong>EPS:</strong></p><p>${emp.nombre_eps}</p>
                <p><strong>ARL:</strong></p><p>${emp.nombre_arl}</p>
                <p><strong>Pensión:</strong></p><p>${emp.nombre_pension}</p>
              </div>
              <div style="margin-top:20px; display:flex; gap:10px;">
                <button onclick="eliminarEmpleado(${emp.codigo_empleado})" class="button1" style="background-color:#c62828;">Eliminar</button>
                <button onclick="editarEmpleado(${emp.codigo_empleado})" class="button1" style="background-color:#1976d2;">Editar</button>
              </div>
            </div>
          `;
        });
    }

      // Eliminar empleado
      function eliminarEmpleado(codigo) {
          if (confirm("¿Estás seguro de que deseas eliminar este empleado?")) {
              fetch(`/empleado/eliminar?codigo=${codigo}`, {
                      method: "DELETE"
                  })
                  .then(r => r.json())
                  .then(data => {
                      alert(data.mensaje || "Empleado eliminado");
                      document.getElementById("resultadoEmpleado").innerHTML = "";
                  });
          }
      }
      // scripts/Inicioscript.js

// MENÚ DESPLEGABLE
function toggleMenu() {
  const menu = document.getElementById("side-menu");
  menu.style.display = (menu.style.display === "block") ? "none" : "block";
}

// Ocultar menú al hacer clic fuera de él
window.addEventListener("click", function (e) {
  const menu = document.getElementById("side-menu");
  const icon = document.querySelector(".menu-icon");
  if (!menu.contains(e.target) && !icon.contains(e.target)) {
    menu.style.display = "none";
  }
});
