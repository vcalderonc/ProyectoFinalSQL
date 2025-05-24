// Mostrar/ocultar menú lateral
function toggleMenu() {
    const menu = document.getElementById("side-menu");
    menu.classList.toggle("show");
}

function consultarNomina() {
    const codigo = document.getElementById("codigoEmpleado").value;
    const nombre = document.getElementById("nombreEmpleado").value;

    fetch(`/empleado/info?codigo=${codigo}`)
        .then(r => r.json())
        .then(data => {
            const contenedor = document.getElementById("nomina-empleado");
            contenedor.innerHTML = "";
            contenedor.style.background = "none";
            contenedor.style.boxShadow = "none";
            contenedor.style.padding = "0";

            if (!data || data.length === 0) {
                contenedor.style.display = "block";
                contenedor.style.marginTop = "20px";
                contenedor.innerHTML = "<p style='text-align:center;'>No se encontraron datos para ese código.</p>";
                return;
            }

            const emp = data[0];
            if (emp.nombre_empleado.toLowerCase() !== nombre.toLowerCase()) {
                contenedor.style.display = "block";
                contenedor.style.marginTop = "20px";
                contenedor.innerHTML = "<p style='text-align:center;'>El nombre no coincide con el código ingresado.</p>";
                return;
            }

            const inc_inicio = emp.inc_inicio || 'No aplica';
            const inc_fin = emp.inc_fin || 'No aplica';
            const tipo_incapacidad = emp.tipo_incapacidad || 'No aplica';
            const vac_inicio = emp.vac_inicio || 'No aplica';
            const vac_fin = emp.vac_fin || 'No aplica';

            contenedor.style.display = "block";
            contenedor.innerHTML = `
              <div style="
                max-width: 1000px;
                margin: auto;
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                gap: 20px;
              ">

                <div style="
                  flex: 1 1 30%;
                  min-width: 280px;
                  background: #111;
                  padding: 24px;
                  border-radius: 20px;
                  box-shadow: 0 0 10px rgba(0,0,0,0.3);
                ">
                  <h3 style="color:#008f39 ;">👤 Información General</h3>
                  <p><strong>Código:</strong> ${emp.codigo_empleado}</p>
                  <p><strong>Nombre:</strong> ${emp.nombre_empleado}</p>
                  <p><strong>Dependencia:</strong> ${emp.nombre_dependencia}</p>
                  <p><strong>Cargo:</strong> ${emp.nombre_cargo}</p>
                  <p><strong>Sueldo:</strong> $${emp.sueldo}</p>
                  <p><strong>EPS:</strong> ${emp.nombre_eps}</p>
                  <p><strong>ARL:</strong> ${emp.nombre_arl}</p>
                  <p><strong>Pensión:</strong> ${emp.nombre_pension}</p>
                </div>

                <div style="
                  flex: 1 1 30%;
                  min-width: 280px;
                  background: #111;
                  padding: 24px;
                  border-radius: 20px;
                  box-shadow: 0 0 10px rgba(0,0,0,0.3);
                ">
                  <h3 style="color:#008f39 ;">🏥 Incapacidad</h3>
                  <p><strong>Inicio:</strong> ${emp.inc_inicio || 'No aplica'}</p>
                  <p><strong>Fin:</strong> ${emp.inc_fin || 'No aplica'}</p>
                  <p><strong>Tipo:</strong> ${emp.tipo_incapacidad || 'No aplica'}</p>
                </div>

                <div style="
                  flex: 1 1 30%;
                  min-width: 280px;
                  background: #111;
                  padding: 24px;
                  border-radius: 20px;
                  box-shadow: 0 0 10px rgba(0,0,0,0.3);
                ">
                  <h3 style="color:#008f39 ;">🌴 Vacaciones</h3>
                  <p><strong>Inicio:</strong> ${emp.vac_inicio || 'No aplica'}</p>
                  <p><strong>Fin:</strong> ${emp.vac_fin || 'No aplica'}</p>
                </div>

              </div>

              <div style="text-align:center; margin-top: 30px;">
                <button class="exportar-pdf" onclick="window.open('/empleado/nomina_pdf?codigo=${emp.codigo_empleado}', '_blank')">
                  Exportar PDF
                </button>
              </div>
            `;

            contenedor.scrollIntoView({ behavior: "smooth" });
        });
}