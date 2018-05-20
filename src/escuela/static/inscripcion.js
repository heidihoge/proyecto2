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

function verificarTitular() {
    var titularForm = $('#formulario-titular').find('form');

    function clean() {
        titularForm.find('.feedback-message').text('');
        titularForm.find('.text-danger').removeClass('text-danger');
        titularForm.find('.has-error').removeClass('has-error');
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
                for (campo in data.errors) {
                    if (data.errors.hasOwnProperty(campo)) {
                        errDesc = data.errors[campo];
                        titularForm.find('[name=' + campo + ']')
                            .siblings('.feedback-message')
                            .addClass('text-danger')
                            .text(errDesc)
                            .parent()
                            .parent()
                            .addClass('has-error');
                    }
                }

                wizard.smartWizard('setError', {stepnum: 1, iserror: true});
                notifyError("Complete los campos obligatorios.");
            }
        });

}

// #comentario: Carga los datos obtenidos a partir del autocompletado (persona)
function cargar(form, datos) {

    form.find('[name=sexo]').iCheck('uncheck');
    form.trigger("reset");
    for (var campo in datos.fields) {
        if (datos.fields.hasOwnProperty(campo)) {
            form.find('[name=' + campo + '][type!=file]').val(datos.fields[campo]);
            if (campo === 'sexo') {
                form.find('[name=sexo][value=' + datos.fields[campo] + ']').iCheck('check');
            }
        }
    }
    form.find('[name=cedula]').val(datos.id);

}

// #comentario logica cuando se selecciona siguiente
window.wizardOnLeaveStep = function (element, context) {

    switch (context.fromStep) {
        case 1: // Titular
            verificarTitular();
            break;
        case 2: // Alumno
            //verificarAlumno();
            break;
        case 3: // Inscribir
            //verificarInscripcion();
            break;
    }

    return true;
};

// #comentario: Se ejecuta cuando se presiona el boton Guardar.
window.wizardOnFinish = function (element, context) {
    if (context.fromStep === 4) {
        alert("Factura generada!");
    }
};


// #comentario: reduce la cantidad de alumnos.
function quitarAlumno() {
    if (alumnosCount > 1) {
        $('#panel-alumno-' + alumnosCount).remove();
        alumnosCount--;
    }
}


// #comentario: incrementa la cantidad de alumnos.
function alumnoExtra() {
    alumnosCount++;
    var bindId = "-alumno-" + alumnosCount;
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
        formTemplateAlumno = $('#formulario-template-alumno').find('form');
    }
    var alumnoForm = formTemplateAlumno.clone();
    alumnoForm.addClass('text-left');
    alumnoForm.find('input[name=apellido]').attr('data-bind', 'apellido' + bindId);
    alumnoForm.find('input[name=nombre]').attr('data-bind', 'nombre' + bindId);
    tabContentPanel.append(alumnoForm);
    tabContent.append(tabContentPanel);
    panel.append(tab);
    panel.append(tabContent);
    $('#formulario-alumno').find('#accordion').append(panel);
    alumnoForm.find('.select2').remove();
    alumnoForm.find('[name=cedula]').trigger('autocompleteLightInitialize');
    configurarCalendario(alumnoForm.find('[name^=fecha]'));
    configurarICheck(alumnoForm.find('[name=sexo]'));
    alumnoForm.on('select2:select', function (event) {
        nombre.text("");
        apellido.text("");
        cargar(alumnoForm, event.params.data);
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
        formTitular = $('#formulario-titular').find('form');
        configurarCalendario(formTitular.find('[name=fecha_nacimiento]'));
        configurarICheck(formTitular.find('[name=sexo]'));
    }

    formTitular.on('select2:select', function (event) {
        cargar(formTitular, event.params.data);
    });

    $('#calendario').fullCalendar({
        locale: 'es',
        themeSystem: 'jquery-ui',
        schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
        defaultView: 'agendaDay',
        groupByResource: true,
        events: [{
            title: 'test',
            start: new Date()
        }],
        resources: [
          { id: 'a', title: 'Lunes' },
          { id: 'b', title: 'Martes' },
          { id: 'c', title: 'Miércoles' },
          { id: 'd', title: 'Jueves' },
          { id: 'e', title: 'Viernes' }
        ]
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
setTimeout(function(){
    wizard.smartWizard('goToStep', 3);
}, 500);