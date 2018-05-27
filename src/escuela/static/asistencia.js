$(document).ready(function () {
    Vue.directive('datepicker', {
        bind: function (el, binding, vnode) {
            var key = binding.expression; // dentro de data, key es el nombre de la variable
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
                console.log(picker.startDate.format("DD/MM/YYYY"));
                window.vm[key] = picker.startDate.format("DD/MM/YYYY");
            });
            $(el).inputmask();
        },
        update: function (val) {

        }
    });

    Vue.directive('icheck', {
        bind: function (el, binding, vnode) {
            var key = binding.expression;
            console.log(arguments);
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
        update: function(el){
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
                // vm.alumnos.push({
                //     nombre: "Julio Reyes (4145624)",
                //     grupo: "Natacion 101 - Prof Heidi - 08:00 - 09:00 - Lunes, Martes, Miercoles",
                //     asistencia: false
                // },
                // {
                //     nombre: "Heidi  (4145624)",
                //     grupo: "Natacion 101 - Prof Heidi - 08:00 - 09:00 - Lunes, Martes, Miercoles",
                //     asistencia: true
                // });
                $.ajax('/escuela/asistencias?fecha=' + vm.dia)
                    .then(function (data) {
                        vm.alumnos = data;
                        console.log(vm)
                    });

            }
        },
        computed: {}
    });

    $('.select2').remove();
    $('[name=grupo]').trigger('autocompleteLightInitialize')
        .on('select2:select', function(e) {
            window.vm["grupo"] = e.params.data.id;
        }).on('select2:unselect', function(e) {
            window.vm["grupo"] = null;
        });

});

