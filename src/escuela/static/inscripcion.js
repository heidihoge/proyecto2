// #comentario: elemento wizard
var wizard = null;

// #comentario: Cantidad de alumnos.
var alumnosCount = 0;

// #comentario: Template del alumno
var formTemplateAlumno = null;

// #comentario: Formulario del titular
var formTitular = null;

function notifyError(message) {
    PNotify.prototype.options.delay = 3000;
    new PNotify({
        title: 'Error',
        text: message,
        type: 'error',
        styling: 'bootstrap3'
    });
}

function verificarAlumnos() {
    var form = $('form');
    var feedback = $('#alumno-feedback');

    function clean() {
        feedback.html('');
        feedback.removeClass('alert alert-danger');
    }

    var formData = new FormData(form[0]);
    $.post({
        url: window.verificarAlumnosUrl,
        data: formData,
        cache: false,
        contentType: false,
        processData: false
    })
        .done(function (data) {
            if (data.filter(function(d){ return d.valid === false }).length === 0) {
                clean();
                wizard.smartWizard('setError', {stepnum: 2, iserror: false});
            } else {
                clean();
                var errDesc = '';
                feedback.append($('<h5>Corrige los siguientes errores:</h5>'));

                for (var i = 0; i<data.length; i++) {
                    if(data[i].valid) {
                        continue;
                    }
                    var lista = $('<ul></ul>');
                    var listaElemento;

                    for (campo in data[i].errors) {

                        if (data[i].errors.hasOwnProperty(campo)) {
                            listaElemento = $('<li></li>');
                            errDesc = data[i].errors[campo];
                            listaElemento.text(campo + ": " + errDesc);
                            lista.append(listaElemento)
                        }
                    }
                    feedback.append($('<strong>#' + (i+1) + ':</strong>'));
                    feedback.append(lista);
                }


                feedback.addClass('text-danger');
                feedback.addClass('alert alert-danger');
                feedback.addClass('has-error');

                wizard.smartWizard('setError', {stepnum: 2, iserror: true});
                notifyError("Complete los campos obligatorios.");
            }
        });
}
function verificarInscripcion() {
    var form = $('form');
    var feedback = $('#inscripcion-feedback');

    function clean() {
        feedback.html('');
        feedback.removeClass('alert alert-danger');
    }

    var formData = new FormData(form[0]);
    $.post({
        url: window.verificarInscripcionUrl,
        data: formData,
        cache: false,
        contentType: false,
        processData: false
    })
        .done(function (data) {
            if (data.filter(function(d){ return d.valid === false }).length === 0) {
                clean();
                wizard.smartWizard('setError', {stepnum: 3, iserror: false});
            } else {
                clean();
                var errDesc = '';
                feedback.append($('<h5>Corrige los siguientes errores:</h5>'));

                for (var i = 0; i<data.length; i++) {
                    if(data[i].valid) {
                        continue;
                    }
                    var lista = $('<ul></ul>');
                    var listaElemento;

                    for (campo in data[i].errors) {

                        if (data[i].errors.hasOwnProperty(campo)) {
                            listaElemento = $('<li></li>');
                            errDesc = data[i].errors[campo];
                            listaElemento.text(campo + ": " + errDesc);
                            lista.append(listaElemento)
                        }
                    }
                    feedback.append($('<strong>#' + (i+1) + ':</strong>'));
                    feedback.append(lista);
                }


                feedback.addClass('text-danger');
                feedback.addClass('alert alert-danger');
                feedback.addClass('has-error');

                wizard.smartWizard('setError', {stepnum: 3, iserror: true});
                notifyError("Complete los campos obligatorios.");
            }

            var error_cupos = data.filter(function(d){ return d.error_cupos !== null && d.error_cupos !== undefined; });
            console.log(error_cupos);
            if (error_cupos.length > 0) {
                new PNotify({
                    title: 'Atención',
                    text: "<p>Alumnos inscriptos en grupos con cupos llenos:</p><ul>" +
                        error_cupos.map(function(alumno){
                            return "<li>Alumno " + alumno.alumno + "</li>"
                        }) + "</ul>",
                    styling: 'bootstrap3',
                    hide: false
                });
            }
        });
}

function verificarTitular() {
    var titularForm = $('form');
    var feedback = $('#titular-feedback');

    function clean() {
        $('#titular-feedback').html('');
        feedback.removeClass('alert alert-danger');
    }

    var formData = new FormData(titularForm[0]);
    $.post({
        url: window.verificarTitularUrl,
        data: formData,
        cache: false,
        contentType: false,
        processData: false
    })
        .done(function (data) {
            if (data.valid) {
                clean();
                wizard.smartWizard('setError', {stepnum: 1, iserror: false});
            } else {
                clean();
                var errDesc = '';
                var lista = $('<ul></ul>');
                var listaElemento;
                for (campo in data.errors) {

                    if (data.errors.hasOwnProperty(campo)) {
                        listaElemento = $('<li></li>');
                        errDesc = data.errors[campo];
                        listaElemento.text(campo + ": " + errDesc);
                        lista.append(listaElemento)
                    }
                }
                feedback.append($('<h5>Corrige los siguientes errores:</h5>'));
                feedback.append(lista);
                feedback.addClass('text-danger');
                feedback.addClass('alert alert-danger');
                feedback.addClass('has-error');

                wizard.smartWizard('setError', {stepnum: 1, iserror: true});
                notifyError("Complete los campos obligatorios.");
            }
        });

}

// #comentario: Carga los datos obtenidos a partir del autocompletado (persona)
function cargar(form, datos, prefix) {

    if (!prefix) {
        prefix = '';
    }

    form.find('[name=' + prefix + 'sexo]').iCheck('uncheck');
    form.trigger("reset");
    for (var campo in datos.fields) {
        if (datos.fields.hasOwnProperty(campo)) {
            form.find('[name=' + prefix + campo + '][type!=file][type!=radio]').val(datos.fields[campo]);
            if (campo === 'sexo') {
                form.find('[name=' + prefix + 'sexo][value=' + datos.fields[campo] + ']').iCheck('check');
            }
            if (campo === 'estado') {
                form.find('[name=' + prefix + 'estado][value=' + datos.fields[campo] + ']').iCheck('check');
            }
        }
    }
    form.find('[name=' + prefix + 'cedula]').val(datos.id);

}

// #comentario logica cuando se selecciona siguiente
window.wizardOnLeaveStep = function (element, context) {

    switch (context.fromStep) {
        case 1: // Titular
            verificarTitular();
            break;
        case 2: // Alumnos
            verificarAlumnos();
            if(context.toStep === 3) {
                generarInscripcion();
            }
            break;
        case 3: // Grupos
            verificarInscripcion();
            if(context.toStep === 4) {
                generarResumen();
            }
            break;
    }

    return true;
};



// Generar Resumen
function generarResumen() {
    var resumentitular = $('#resumen-titular');
    resumentitular.html("");
    // resumentitular.addClass('text-center');

    formTitular.find('input[type=text],select[name$=cedula]')
        .each(function () {
            var elemento = $(this);
            var value = elemento.val();
            var label = formTitular.find('label[for=' + elemento.attr('id') + ']').text();
            resumentitular.append($('<p> ' + label + ': ' + value + '</p>'));
        }
        );
    var resumenalumno = $('#resumen-alumno');
    resumenalumno.html("");
    var formularioAlumno = $('#formulario-alumno');
    for (var i = 1; i<= alumnosCount; i++){
        var panelalumno = formularioAlumno.find('#panel-alumno-' + i);
        resumenalumno.append($("<strong>Alumno " + i+"</strong>").css( "background-color", "rgba(26, 187, 156, 0.27)" ));
        //todos los inputs que no sean ocultos
        panelalumno.find('input[type=text],select[name$=cedula]')
            .each(function () {
                var elemento = $(this);
                var i;
                // resumenalumno.addClass('text-center');
                var value = elemento.val();
                // alumno-1-nombre
                var label = panelalumno.find('label[for=' + elemento.attr('id') + ']').text();
                resumenalumno.append($('<p> ' + label + ': ' + value + '</p>'));
            });
        var formularioInscripcion = $('#formulario-inscripcion');
        var grupoAlumno = formularioInscripcion.find('#grupo-alumno-' + i);

        grupoAlumno.find('input[type=text]')
            .each(function () {
                var elemento = $(this);
                var i;
                // resumenalumno.addClass('text-center');
                var value = elemento.val();
                // alumno-1-nombre
                var label = grupoAlumno.find('label[for=' + elemento.attr('id') + ']').text();
                resumenalumno.append($('<p> ' + label + ': ' + value + '</p>'));


            });
        grupoAlumno.find('select')
            .each(function () {
                var elemento = $(this);
                var i;
                // resumenalumno.addClass('text-center');
                var value = elemento.find('option:selected').text();
                // alumno-1-nombre
                var label = grupoAlumno.find('label[for=' + elemento.attr('id') + ']').text();
                resumenalumno.append($('<p> ' + label + ': ' + value + '</p>'));


            });

    }
}



function generarInscripcion() {
    var fieldAlumnoPrefix = 'alumno-';
    var idPanelAlumnoPrefix = "#panel-alumno-";
    var idGrupoAlumnoPrefix = "grupo-alumno-";
    var formularioIncripcion = $('#formulario-inscripcion');
    var templateFormularioInscripcion = $('#formulario-template-incripcion');

    // limpia el contenido del formulario
    formularioIncripcion.html("");

    var inscripcion, fieldset, cedula, nombre, apellido, panelAlumno;
    // El id del contenedor alumno empieza de 1.
    for (var i=1; i <= alumnosCount; i++) {
        panelAlumno = $(idPanelAlumnoPrefix + i);
        cedula = panelAlumno.find('[name=' + fieldAlumnoPrefix + i + '-cedula]').val();
        nombre = panelAlumno.find('[name=' + fieldAlumnoPrefix + i + '-nombre]').val();
        apellido = panelAlumno.find('[name=' + fieldAlumnoPrefix + i + '-apellido]').val();

        fieldset = $('<fieldset id="' + idGrupoAlumnoPrefix + i +'"><legend>' + cedula + " (" + nombre + " " + apellido + ")" + '</legend></fieldset>');

        inscripcion = $(templateFormularioInscripcion.clone().html());
        inscripcion.find('.select2').remove();
        inscripcion.find('[name=grupo]').trigger('autocompleteLightInitialize');
        var alumnoHiddent = $('<input type="hidden" name="alumno" />');
        inscripcion.append(alumnoHiddent);
        inscripcion.find('[name=alumno]').val(cedula);

        configurarCalendario(inscripcion.find('[name^=fecha]'));

        var inputs = inscripcion.find('[name]');
        for (var j = 0; j <= inputs.length; j++) {
            var input = $(inputs[j]);
            input.attr('name', fieldAlumnoPrefix  + i + '-inscripcion-' + input.attr('name'));
        }
        fieldset.append(inscripcion);
        formularioIncripcion.append(fieldset);
    }
}

// #comentario: Se ejecuta cuando se presiona el boton Guardar.
window.wizardOnFinish = function (element, context) {
    if (context.fromStep === 4) {
        var form = $('form');
        var formData = new FormData(form[0]);
        $.post({
            url: window.guardarInscripcion,
            data: formData,
            cache: false,
            contentType: false,
            processData: false
        })
            .done(function (data) {
                if(data.errores.length > 0) {
                    // manejar
                    notifyError("Error al guardar, verifique todos los pasos (" + data.errores.join(",") + ")")
                    for(var i = 0; i<data.errores.length; i++) {
                        wizard.smartWizard('setError', {stepnum: data.errores[i], iserror: true});
                    }
                } else {
                    document.location.href = "/";
                }
            });

    }
};


// #comentario: reduce la cantidad de alumnos.
function quitarAlumno() {
    if (alumnosCount > 1) {
        $('#panel-alumno-' + alumnosCount).remove();
        alumnosCount--;
        $('[name=alumnosCount]').val(alumnosCount);
    }
}


// #comentario: incrementa la cantidad de alumnos.
function alumnoExtra() {
    alumnosCount++;
    $('[name=alumnosCount]').val(alumnosCount);
    var bindId = "-alumno-" + alumnosCount;
    var fieldPrefix = 'alumno-' + alumnosCount + '-';
    var panel = $('<div></div>'); //crea elemento
    panel.attr('id', 'panel-alumno-' + alumnosCount);
    panel.addClass('panel');
    var tab = $('<a></a>');
    if (alumnosCount > 1) {
        tab.addClass('collapsed');
    }
    tab.addClass('panel-heading');
    tab.attr('role', 'tab');
    tab.attr('id', 'heading-' + alumnosCount);
    tab.attr('data-toggle', 'collapse');
    tab.attr('data-parent', '#accordion');
    tab.attr('href', '#collapse-' + alumnosCount);
    tab.attr('aria-expanded', false);
    tab.attr('aria-controls', 'collapse-' + alumnosCount);
    var titulo = $('<h4></h4>');
    titulo.addClass('panel-title');
    var numero = $('<span></span>');
    numero.text("#" + alumnosCount + " ");
    titulo.append(numero);
    var apellido = $('<span></span>');
    apellido.attr('data-bind', 'apellido' + bindId);
    titulo.append(apellido);

    var nombre = $('<span></span>');
    nombre.attr('data-bind', 'nombre' + bindId);
    titulo.append(nombre);

    tab.append(titulo);

    var tabContent = $('<div></div>');
    tabContent.addClass('panel-collapse');
    tabContent.addClass('collapse');
    if (alumnosCount === 1) {
        tabContent.addClass('in');
    }
    tabContent.attr('id', 'collapse-' + alumnosCount);
    tabContent.attr('role', 'tabpanel');
    tabContent.attr('aria-labelledby', 'heading-' + alumnosCount);
    tabContent.attr('aria-expanded', false);


    var tabContentPanel = $('<div></div>');
    tabContentPanel.addClass('panel-body');
    if (formTemplateAlumno === null) {
        formTemplateAlumno = $('#formulario-template-alumno');
    }
    var alumnoForm = $(formTemplateAlumno.clone().html());
    alumnoForm.addClass('text-left');
    alumnoForm.find('input[name=apellido]').attr('data-bind', 'apellido' + bindId);
    alumnoForm.find('input[name=nombre]').attr('data-bind', 'nombre' + bindId);
    tabContentPanel.append(alumnoForm);
    tabContent.append(tabContentPanel);
    panel.append(tab);
    panel.append(tabContent);
    $('#formulario-alumno').find('#accordion').append(panel);

    // Arregla select de alumno por cedula.
    alumnoForm.find('.select2').remove();
    alumnoForm.find('[name=cedula]').trigger('autocompleteLightInitialize');
    configurarCalendario(alumnoForm.find('[name^=fecha]'));
    configurarICheck(alumnoForm.find('[name=sexo]'));
    configurarICheck(alumnoForm.find('[name=estado]'));

    var inputs = alumnoForm.find('[name]');
    for (var j = 0; j <= inputs.length; j++) {
        var input = $(inputs[j]);
        input.attr('name', fieldPrefix + input.attr('name'));
    }

    alumnoForm.on('select2:select', function (event) {
        nombre.text("");
        apellido.text("");
        cargar(alumnoForm, event.params.data, fieldPrefix);
        var fields = event.params.data.fields;
        if (fields) {
            var hasNombre = false;
            if (fields.hasOwnProperty('nombre')) {
                nombre.text(fields['nombre']);
                hasNombre = true;
            }
            if (fields.hasOwnProperty('apellido')) {
                apellido.text(fields['apellido'] + (hasNombre ? ', ' : ''));
            }
        }
    });

    bind();
}

function configurarICheck(element) {
    element.parents('ul').attr('style', 'list-style-type: none;padding:0');
    element.iCheck({
        checkboxClass: 'icheckbox_flat-green',
        radioClass: 'iradio_flat-green'
    });
}

function configurarCalendario(element) {
    var config = {
        singleDatePicker: true,
        showDropdowns: true,
        locale: {
            format: 'DD/MM/YYYY',
            daysOfWeek: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'],
            monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Deciembre'],

        }
    };

    element.daterangepicker(config);
    element.inputmask();
}

$(document).ready(function () {
    // #comentario: Agrega el primer alumno. (siempre minimo: 1)
    alumnoExtra();

    wizard = $('#wizard');
    if (formTitular === null) {
        formTitular = $('#formulario-titular');
        configurarCalendario(formTitular.find('[name=fecha_nacimiento]'));
        configurarICheck(formTitular.find('[name=sexo]'));
        configurarICheck(formTitular.find('[name=estado]'));
    }

    formTitular.on('select2:select', function (event) {
        cargar(formTitular, event.params.data);
    });

});

// #comentario: Esto es para que el nombre y apellido del alumno se vea en la cabecera del accordion (paso 2)
var bind = function () {
    var elements = document.querySelectorAll('[data-bind]'), scope = {};

    elements.forEach(function (element) {
        if (element.type === 'text') {
            var propToBind = element.getAttribute("data-bind");

            addScopeProp(propToBind);

            element.onkeyup = function () {
                scope[propToBind] = element.value;
            };

        }
    });

    function addScopeProp(prop) {
        if (!scope.hasOwnProperty(prop)) {
            var value;

            Object.defineProperty(scope, prop, {
                set: function (newValue) {
                    elements.forEach(function (element) {
                        if (element.getAttribute('data-bind') === prop) {
                            if (element.type === 'text') {
                                element.value = newValue;
                            } else {
                                element.innerHTML = newValue;
                                if (prop.substring(0, 8) === 'apellido' && newValue.length > 0) {
                                    element.innerHTML += ", ";
                                }
                            }
                        }
                    })
                },
                get: function () {
                    return value;
                },
                enumerable: true
            });
        }
    }

};





// Borrar esto despues...
// setTimeout(function(){
//     wizard.smartWizard('goToStep', 3);
// }, 500);