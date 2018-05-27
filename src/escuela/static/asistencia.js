$(document).ready(function () {

    $.ajaxSetup({
        headers: {'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')}
    });

    Vue.directive('datepicker', {
        bind: function (el, binding, vnode) {
            var key = binding.expression; // dentro de data, key es el nombre de la variable
            setTimeout(function() {
                $(el).daterangepicker({
                    singleDatePicker: true,
                    showDropdowns: true,
                    locale: {
                        format: 'DD/MM/YYYY',
                        daysOfWeek: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'],
                        monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Deciembre'],

                    }
                });
                $(el).on('apply.daterangepicker', function (e, picker) {
                    window.vm[key] = picker.startDate.format("DD/MM/YYYY");
                });
                $(el).inputmask();
            });

        }
    });

    Vue.directive('icheck', {
        bind: function (el, binding, vnode) {
            var key = binding.expression;
            setTimeout(function() {
                $(el).iCheck({
                    checkboxClass: 'icheckbox_flat-green',
                    radioClass: 'iradio_flat-green'
                }).on('ifChecked', function(){
                    el.dispatchEvent(new Event("change"));
                }).on('ifUnchecked', function(){
                    el.dispatchEvent(new Event("change"));
                });

                if (binding.value) {
                    el.dispatchEvent(new Event("ifChecked"));
                }

            });
        },
        update: function(el, binding, vnode) {
            setTimeout(function(){
                $(el).iCheck('update');
            })
        }
    });

    window.vm = new Vue({
        delimiters: ["[[", "]]"],
        el: "#app",
        data: {
            dia: null,
            grupo: null,
            alumnos: []
        },
        created: function () {
            this.cargarAlumnos();
        },
        methods: {
            cargarAlumnos: function () {
                var vm = this;
                vm.dia = moment().format("DD/MM/YYYY");
                this.actualizarLista(vm.dia, vm.grupo);

            },
            actualizarLista: function (dia, grupo) {
                var vm = this;
                $.ajax('/escuela/asistencias?fecha=' + dia + '&grupo=' + (grupo?grupo:''))
                    .then(function (data) {
                        vm.alumnos = data.alumnos;
                    });
            },
            actualizarAsistencia: function () {
                var vm = this;

                $.ajax('/escuela/asistencia/update', {
                    data: JSON.stringify(vm.alumnos.map(function(alumno) {
                        return {
                            "alumno_id": alumno.id,
                            "grupo_id": alumno.grupo.id,
                            "fecha": vm.dia,
                            "asistencia_id": alumno.asistencia_id,
                            "asistencia_presente": alumno.asistencia_presente,
                            "asistencia_comentario": alumno.asistencia_comentario
                        }
                    })),
                    contentType: 'application/json',
                    type: 'POST'
                }).done(function () {
                    PNotify.prototype.options.delay = 3000;
                    new PNotify({
                                  title: 'Éxito',
                                  text: 'Guardado correctamente.',
                                  type: 'success',
                                  styling: 'bootstrap3'
                              });
                    vm.actualizarLista(vm.dia, vm.grupo);
                }).fail(function () {
                    PNotify.prototype.options.delay = 3000;
                    new PNotify({
                                  title: 'Error',
                                  text: 'Ocurrio un error al guardar.',
                                  type: 'error',
                                  styling: 'bootstrap3'
                              });
                    vm.actualizarLista(vm.dia, vm.grupo);
                })
            }
        },
        watch: {
            dia: function (val) {
                var vm = this;
                this.actualizarLista(val, vm.grupo);
            },
            grupo: function (val) {
                var vm = this;
                this.actualizarLista(vm.dia, val);
            }
        }
    });

    $('.select2').remove();
    $('[name=grupo]').trigger('autocompleteLightInitialize')
        .on('select2:select', function(e) {
            window.vm["grupo"] = e.params.data.id;
        }).on('select2:unselect', function(e) {
            window.vm["grupo"] = null;
        });

});

