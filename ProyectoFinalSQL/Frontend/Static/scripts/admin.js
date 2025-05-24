// ----------------------------
// FUNCIONES PARA MODALES
// ----------------------------
function toggleMenu() {
    const menu = document.getElementById("side-menu");
    menu.classList.toggle("show");
}

function abrirModal() {
    document.getElementById("modalCrearEmpleado").style.display = "flex";
}

function cerrarModal() {
    document.getElementById("modalCrearEmpleado").style.display = "none";
}

function abrirModalNovedad() {
    document.getElementById("modalNovedad").style.display = "flex";
}

function cerrarModalNovedad() {
    document.getElementById("modalNovedad").style.display = "none";
}

function cerrarModalEditar() {
    document.getElementById("modalEditarEmpleado").style.display = "none";
}

// Ocultar modal si se hace clic fuera
window.onclick = function(event) {
    const modales = ["modalCrearEmpleado", "modalEditarEmpleado", "modalNovedad"];
    modales.forEach(id => {
        const modal = document.getElementById(id);
        if (event.target === modal) modal.style.display = "none";
    });
}

function toggleSeccion(id) {
    const seccion = document.getElementById(id);
    seccion.style.display = (seccion.style.display === "none" || seccion.style.display === "") ? "block" : "none";
}

// ----------------------------
// CONSULTAR Y GESTIONAR EMPLEADOS
// ----------------------------
function buscarEmpleado() {
    const codigo = document.getElementById("codigoEmpleado").value;
    fetch(`/empleado/info?codigo=${codigo}`)
        .then(r => r.json())
        .then(data => {
            const contenedor = document.getElementById("resultadoEmpleado");
            contenedor.innerHTML = "";

            if (!data || data.length === 0) {
                contenedor.innerHTML = "<p style='text-align:center;'>No se encontraron datos para ese código.</p>";
                return;
            }

            const emp = data[0];
            const div = document.createElement("div");
            div.style.backgroundColor = "#111";
            div.style.padding = "20px";
            div.style.borderRadius = "16px";
            div.style.boxShadow = "0 0 10px rgba(255,255,255,0.05)";
            div.style.marginBottom = "20px";
            div.style.position = "relative";
            div.style.boxSizing = "border-box";
            div.style.width = "100%";
            div.style.flex = "0 0 auto";
            div.style.animation = "fadeIn 0.3s ease-in-out";

            div.innerHTML = `
                <span onclick="cerrarConAnimacion(this)" style="
                position:absolute; top:10px; right:14px;
                font-size:20px; color:#aaa; cursor:pointer; font-weight:bold;">&times;</span>
                <h3 style="font-size:20px; color:#6a6aff; margin-bottom:20px;">👤 Información del Empleado</h3>

                <div style="display: grid; grid-template-columns: 1fr 2fr; row-gap: 10px; margin-bottom: 16px;">
                <p><strong>Código:</strong></p><p>${emp.codigo_empleado}</p>
                <p><strong>Nombre:</strong></p><p>${emp.nombre_empleado}</p>
                <p><strong>Cargo:</strong></p><p>${emp.nombre_cargo}</p>
                <p><strong>Dependencia:</strong></p><p>${emp.nombre_dependencia}</p>
                <p><strong>Sueldo:</strong></p><p>$${emp.sueldo}</p>
                <p><strong>Fecha ingreso:</strong></p><p>${emp.fecha_ingreso}</p>
                <p><strong>EPS:</strong></p><p>${emp.nombre_eps}</p>
                <p><strong>ARL:</strong></p><p>${emp.nombre_arl}</p>
                <p><strong>Pensión:</strong></p><p>${emp.nombre_pension}</p>
                </div>

                <div style="background:#1d1d1d; padding:14px; border-radius:12px; margin-bottom:12px;">
                <h4 style="color:#4caf50; margin-bottom:10px;">🌴 Vacaciones</h4>
                <p><strong>Inicio:</strong> ${emp.vac_inicio || 'No aplica'}</p>
                <p><strong>Fin:</strong> ${emp.vac_fin || 'No aplica'}</p>
                </div>

                <div style="background:#1d1d1d; padding:14px; border-radius:12px;">
                <h4 style="color:#ff9800; margin-bottom:10px;">🏥 Incapacidad</h4>
                <p><strong>Inicio:</strong> ${emp.inc_inicio || 'No aplica'}</p>
                <p><strong>Fin:</strong> ${emp.inc_fin || 'No aplica'}</p>
                <p><strong>Tipo:</strong> ${emp.tipo_incapacidad || 'No aplica'}</p>
                </div>

                <div style="margin-top:20px; display:flex; gap:10px;">
                <button onclick="eliminarEmpleado(${emp.codigo_empleado})" class="button1" style="background-color:#c62828;">Eliminar</button>
                <button onclick="editarEmpleado(${emp.codigo_empleado})" class="button1" style="background-color:#1976d2;">Editar</button>
                </div>
            `;

            contenedor.appendChild(crearTarjetaEmpleado(emp));

        });
}



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

// ----------------------------
// FILTROS AVANZADOS
// ----------------------------
function filtrarAvanzado() {
    const sueldo = document.getElementById("filtroSueldo").value;
    const cargo = document.getElementById("filtroCargo").value;
    const desde = document.getElementById("filtroDesde").value;
    const hasta = document.getElementById("filtroHasta").value;
    const vac = document.getElementById("checkVacaciones").checked ? "1" : "0";
    const inc = document.getElementById("checkIncapacidad").checked ? "1" : "0";

    const params = new URLSearchParams();
    if (sueldo) params.append("sueldo", sueldo);
    if (cargo) params.append("cargo", cargo);
    if (desde && hasta) {
        params.append("desde", desde);
        params.append("hasta", hasta);
    }
    if (vac === "1") params.append("vac", "1");
    if (inc === "1") params.append("inc", "1");


    fetch(`/admin/filtro/avanzado?${params.toString()}`)
        .then(r => r.json())
        .then(data => {
            const contenedor = document.getElementById("resultadoEmpleado");
            contenedor.innerHTML = "";

            if (!data || data.length === 0) {
                contenedor.innerHTML = "<p style='text-align:center;'>No se encontraron empleados con esos criterios.</p>";
                return;
            }
            if (desde && hasta) {
                params.append("desde", desde);
                params.append("hasta", hasta);
            }


            data.forEach(emp => {
                const div = document.createElement("div");
                div.style.backgroundColor = "#111";
                div.style.padding = "20px";
                div.style.borderRadius = "16px";
                div.style.boxShadow = "0 0 10px rgba(255,255,255,0.05)";
                div.style.marginBottom = "20px";
                div.style.position = "relative";
                div.style.boxSizing = "border-box";
                div.style.width = "100%";
                div.style.flex = "0 0 auto";
                div.style.animation = "fadeIn 0.3s ease-in-out";

                div.innerHTML = `
                    <span class="close-btn" onclick="cerrarConAnimacion(this)">&times;</span>
                    <h3 style="font-size:20px; color:#6a6aff; margin-bottom:16px;">👤 Información del Empleado</h3>

                    <div style="display: grid; grid-template-columns: 1fr 2fr; row-gap: 8px; margin-bottom: 16px;">
                        <p><strong>Código:</strong></p><p>${emp.codigo_empleado}</p>
                        <p><strong>Nombre:</strong></p><p>${emp.nombre_empleado}</p>
                        <p><strong>Cargo:</strong></p><p>${emp.nombre_cargo}</p>
                        <p><strong>Dependencia:</strong></p><p>${emp.nombre_dependencia}</p>
                        <p><strong>Sueldo:</strong></p><p>$${emp.sueldo}</p>
                        <p><strong>Fecha ingreso:</strong></p><p>${emp.fecha_ingreso}</p>
                        <p><strong>EPS:</strong></p><p>${emp.nombre_eps}</p>
                        <p><strong>ARL:</strong></p><p>${emp.nombre_arl}</p>
                        <p><strong>Pensión:</strong></p><p>${emp.nombre_pension}</p>
                    </div>

                    <div style="background:#1d1d1d; padding:14px; border-radius:12px; margin-bottom:12px;">
                        <h4 style="color:#4caf50; margin-bottom:10px;">🌴 Vacaciones</h4>
                        <p><strong>Inicio:</strong> ${emp.vac_inicio || 'No aplica'}</p>
                        <p><strong>Fin:</strong> ${emp.vac_fin || 'No aplica'}</p>
                    </div>

                    <div style="background:#1d1d1d; padding:14px; border-radius:12px;">
                        <h4 style="color:#ff9800; margin-bottom:10px;">🏥 Incapacidad</h4>
                        <p><strong>Inicio:</strong> ${emp.inc_inicio || 'No aplica'}</p>
                        <p><strong>Fin:</strong> ${emp.inc_fin || 'No aplica'}</p>
                        <p><strong>Tipo:</strong> ${emp.tipo_incapacidad || 'No aplica'}</p>
                    </div>

                    <div style="margin-top:20px; display:flex; gap:10px;">
                        <button onclick="eliminarEmpleado(${emp.codigo_empleado})" class="button1" style="background-color:#c62828;">Eliminar</button>
                        <button onclick="editarEmpleado(${emp.codigo_empleado})" class="button1" style="background-color:#1976d2;">Editar</button>
                    </div>
                `;
                contenedor.appendChild(crearTarjetaEmpleado(emp));


            });
        });
}


function limpiarFiltros() {
    document.getElementById("filtroCargo").value = "";
    document.getElementById("filtroSueldo").value = "";
    document.getElementById("filtroDesde").value = "";
    document.getElementById("filtroHasta").value = "";
    document.getElementById("checkVacaciones").checked = false;
    document.getElementById("checkIncapacidad").checked = false;
    document.getElementById("resultadoEmpleado").innerHTML = "";
}

function cerrarConAnimacion(btn) {
    const tarjeta = btn.parentElement;
    tarjeta.style.animation = "fadeOutSlide 0.3s ease forwards";
    setTimeout(() => tarjeta.remove(), 300); // Espera a que termine la animación
}

function mostrarTodosLosEmpleados() {
    fetch("/empleados")
        .then(r => r.json())
        .then(data => {
            const contenedor = document.getElementById("resultadoEmpleado");
            contenedor.innerHTML = "";

            if (!data || data.length === 0) {
                contenedor.innerHTML = "<p style='text-align:center;'>No hay empleados registrados.</p>";
                return;
            }

            data.forEach(emp => {
                const div = document.createElement("div");
                div.style.backgroundColor = "#111";
                div.style.padding = "20px";
                div.style.borderRadius = "16px";
                div.style.boxShadow = "0 0 10px rgba(255,255,255,0.05)";
                div.style.marginBottom = "20px";
                div.style.position = "relative";
                div.style.boxSizing = "border-box";
                div.style.width = "100%";
                div.style.flex = "0 0 auto";
                div.style.animation = "fadeIn 0.3s ease-in-out";


                div.innerHTML = `
                    <span class="close-btn" onclick="cerrarConAnimacion(this)">&times;</span>
                    <h3 style="font-size:20px; color:#6a6aff; margin-bottom:20px;">👤 ${emp.nombre_empleado}</h3>
                    <div style="display: grid; grid-template-columns: 1fr 2fr; row-gap: 10px;">
                        <p><strong>Código:</strong></p><p>${emp.codigo_empleado}</p>
                        <p><strong>Cargo:</strong></p><p>${emp.nombre_cargo}</p>
                        <p><strong>Dependencia:</strong></p><p>${emp.nombre_dependencia}</p>
                        <p><strong>Sueldo:</strong></p><p>$${emp.sueldo}</p>
                        <p><strong>Fecha ingreso:</strong></p><p>${emp.fecha_ingreso}</p>
                        <p><strong>EPS:</strong></p><p>${emp.nombre_eps}</p>
                        <p><strong>ARL:</strong></p><p>${emp.nombre_arl}</p>
                        <p><strong>Pensión:</strong></p><p>${emp.nombre_pension}</p>
                    </div>
                    <div style="margin-top:20px; display:flex; gap:10px;">
                        <button onclick="editarEmpleado(${emp.codigo_empleado})" class="button1" style="background-color:#1976d2;">Editar</button>
                        <button onclick="eliminarEmpleado(${emp.codigo_empleado})" class="button1" style="background-color:#c62828;">Eliminar</button>
                    </div>
                `;
                contenedor.appendChild(crearTarjetaEmpleado(emp));

            });
        });
}

function ocultarResultados() {
    const contenedor = document.getElementById("resultadoEmpleado");
    const tarjetas = contenedor.querySelectorAll("div");

    tarjetas.forEach(div => {
        div.style.animation = "fadeOut 0.3s ease-in-out";
        setTimeout(() => div.remove(), 280);
    });
}

function crearTarjetaEmpleado(emp) {
    const div = document.createElement("div");
    div.style.backgroundColor = "#111";
    div.style.padding = "20px";
    div.style.borderRadius = "16px";
    div.style.boxShadow = "0 0 10px rgba(255,255,255,0.05)";
    div.style.marginBottom = "20px";
    div.style.position = "relative";
    div.style.width = "100%";
    div.style.flex = "0 0 auto";
    div.style.animation = "fadeIn 0.3s ease-in-out";

    div.innerHTML = `
        <span onclick="cerrarConAnimacion(this)" style="
            position:absolute; top:10px; right:14px;
            font-size:20px; color:#aaa; cursor:pointer; font-weight:bold;">&times;</span>

        <h3 style="font-size:20px; color:#6a6aff; margin-bottom:20px;">👤 ${emp.nombre_empleado}</h3>

        <div style="display: grid; grid-template-columns: 1fr 2fr; row-gap: 10px; margin-bottom: 16px;">
            <p><strong>Código:</strong></p><p>${emp.codigo_empleado}</p>
            <p><strong>Cargo:</strong></p><p>${emp.nombre_cargo}</p>
            <p><strong>Dependencia:</strong></p><p>${emp.nombre_dependencia}</p>
            <p><strong>Sueldo:</strong></p><p>$${emp.sueldo}</p>
            <p><strong>Fecha ingreso:</strong></p><p>${emp.fecha_ingreso}</p>
            <p><strong>EPS:</strong></p><p>${emp.nombre_eps}</p>
            <p><strong>ARL:</strong></p><p>${emp.nombre_arl}</p>
            <p><strong>Pensión:</strong></p><p>${emp.nombre_pension}</p>
        </div>

        <div style="background:#1d1d1d; padding:14px; border-radius:12px; margin-bottom:12px;">
            <h4 style="color:#4caf50; margin-bottom:10px;">🌴 Vacaciones</h4>
            <p><strong>Inicio:</strong> ${emp.vac_inicio || 'No aplica'}</p>
            <p><strong>Fin:</strong> ${emp.vac_fin || 'No aplica'}</p>
        </div>

        <div style="background:#1d1d1d; padding:14px; border-radius:12px;">
            <h4 style="color:#ff9800; margin-bottom:10px;">🏥 Incapacidad</h4>
            <p><strong>Inicio:</strong> ${emp.inc_inicio || 'No aplica'}</p>
            <p><strong>Fin:</strong> ${emp.inc_fin || 'No aplica'}</p>
            <p><strong>Tipo:</strong> ${emp.tipo_incapacidad || 'No aplica'}</p>
        </div>

        <div style="margin-top:20px; display:flex; gap:10px;">
            <button onclick="editarEmpleado(${emp.codigo_empleado})" class="button1" style="background-color:#1976d2;">Editar</button>
            <button onclick="eliminarEmpleado(${emp.codigo_empleado})" class="button1" style="background-color:#c62828;">Eliminar</button>
        </div>
    `;
    return div;
}