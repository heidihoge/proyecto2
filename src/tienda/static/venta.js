        function configurarICheck(element) {
            element.parents('ul').attr('style', 'list-style-type: none;padding:0; display: flex');
            element.parents('label').attr('style', 'padding: 6px;margin:0');
            element.iCheck({
                checkboxClass: 'icheckbox_flat-green',
                radioClass: 'iradio_flat-green'
            });
        }
        $(document).ready(function () {
            window.rowTemplate = $('#row-template');
            configurarICheck($('[name=tipo_pago]'));
            configurarICheck($('[name=metodo_pago]'));
            window.totalForms = $('#id_ventadetalle_set-TOTAL_FORMS');


            $('#id_pago-monto').attr('readonly', true);
            $('#id_monto_total').attr('readonly', true);
            $('#id_total_iva_10').attr('readonly', true);
            $('#id_total_iva_5').attr('readonly', true);
            $('#id_total_exentas').attr('readonly', true);
            $('#id_total_iva').attr('readonly', true);
            $('#id_monto').attr('readonly', true);
            setMetodoPago('Efectivo');



            $('form input').keydown(function (event) {
                if (event.keyCode === 13) {
                    event.preventDefault();
                    return false;
                }
            });

            $('#id_total_iva_10,#id_total_iva_5').on('change', calcularTotalIva);

            $('select[name=talonario_factura]').on('select2:select', function (event) {
                cargarBloqueFactura(event.params.data.fields);
            });

            $('select[name=cliente]').on('select2:select', function (event) {
                if (!event.params.data.fields) {
                    cargarCliente({
                        "ruc_cliente": event.params.data.id
                    });
                } else {
                    cargarCliente(event.params.data.fields);
                }
            });
            var buscacuenta = $('#id_busca_cuenta');
            buscacuenta.siblings('.select2').remove();
            buscacuenta.trigger('autocompleteLightInitialize');
            buscacuenta.on('select2:select', function (event) {
                    var data = event.params.data;
                    agregaDetalle({
                        "monto": data.fields.monto,
                        "detalle": data.text,
                        "pk": data.pk
                    });
                    calcularTotales();
                    if(data) {
                        $('#cuenta').modal('hide');
                    }
                });

        });

        function cargarCliente(datos) {


            var nombreRazon = $('input[name=cliente-nombre_razon]');
            var direccion = $('input[name=cliente-direccion]');
            var telefono = $('input[name=cliente-telefono]');
            var rucCliente = $('input[name=cliente-ruc_cliente]');

            nombreRazon.val('');
            direccion.val('');
            telefono.val('');
            rucCliente.val('');

            if(datos !== undefined) {
                console.log(datos);
                nombreRazon.val(datos.nombre_razon);
                direccion.val(datos.direccion);
                telefono.val(datos.telefono);
                rucCliente.val(datos.ruc_cliente);
            }
        }

        function cargarBloqueFactura(datos) {
            function cambiar(elemento) {

                return function (texto, cssClass){
                    var el = elemento.find("."+cssClass);
                    el.removeClass('blokk');
                    el.html(texto);
                }
            }

            var cambiarTexto = cambiar($('#bloque-factura'));

            cambiarTexto(datos.nombre, 'bloque-factura-nombre');
            cambiarTexto(datos.actividad_economica, 'bloque-factura-actividad-economica');
            cambiarTexto(datos.direccion, 'bloque-factura-direccion');
            cambiarTexto(datos.telefono, 'bloque-factura-telefono');
            cambiarTexto(datos.numero_timbrado, 'bloque-factura-numero-timbrado');
            cambiarTexto(datos.vigencia_desde, 'bloque-factura-vigencia-desde');
            cambiarTexto(datos.vigencia_hasta, 'bloque-factura-vigencia-hasta');
            cambiarTexto(datos.ruc, 'bloque-factura-ruc');
            cambiarTexto(datos.punto_emision, 'bloque-factura-punto-emision');
            cambiarTexto(datos.nro_factura, 'bloque-factura-nro-factura');

            $('input[name=nro_factura]').val(datos.punto_emision + '-' + datos.nro_factura);
            $('input[name=nro_factura_punto_emision]').val(datos.punto_emision);
            $('input[name=nro_factura_numero]').val(parseInt(datos.nro_factura));

        }

        function agregaDetalle(cuenta){
            var formIdx = window.totalForms.val();
            var row = $('<tr></tr>');
            row.attr('id', 'id_ventadetalle_set-' + parseInt(formIdx));
            row.append(window.rowTemplate.html().replace(/__prefix__/g, formIdx));
            console.log(formIdx);
            row.find('.numero').append(parseInt(formIdx) + 1);
            $('#detalles').append(row);
            $('.cantidad input[type=number],.precio input[type=number]').on('change', function(){
                calcularTotales();
            });

            $(row.find("input[name=ventadetalle_set-" + formIdx + "-monto_exento]")).attr("readonly",true);
            $(row.find("input[name=ventadetalle_set-" + formIdx + "-monto_5]")).attr("readonly",true);
            $(row.find("input[name=ventadetalle_set-" + formIdx + "-monto_10]")).attr("readonly", true);

            if (cuenta) {

                row.find(".select2").remove();
                // Si producto es texto, entonces se trata de una cuota!!!
                var productoDescripcion = $("<input type='text' name='ventadetalle_set-"  + formIdx + "-producto-descripcion'></input>");
                productoDescripcion.addClass("form-control");
                productoDescripcion.val(cuenta.detalle);
                $(row.find("select")).replaceWith(productoDescripcion);


                $(row.find("input[name=ventadetalle_set-" + formIdx + "-monto_10]")).val(cuenta.monto);
                $(row.find("input[name=ventadetalle_set-" + formIdx + "-precio]")).val(cuenta.monto);
                $(row.find("input#detalle-" + formIdx + "-producto-iva")).val("10%");

                var cuentainput = $("<input type='hidden' name='ventadetalle_set-"  + formIdx + "-cuenta'></input>");
                cuentainput.val(cuenta.pk);
                $(row).append(cuentainput);

                var productoId = $("<input type='hidden' name='ventadetalle_set-"  + formIdx + "-producto'></input>");
                productoId.val($('#cuenta_id').val());
                $(row).append(productoId);

            }
            else {

                // al elegir producto, carga el precio y el tipo de impuesto (5, 10, exenta)
                $('select[name=ventadetalle_set-' + formIdx + '-producto]').on('select2:select', function (event) {
                    var data = event.params.data.fields;
                    $('input[name=ventadetalle_set-' + formIdx + '-precio]').val(data.precio_venta);
                    $('#detalle-' + formIdx + '-producto-iva').val(data.iva);
                    calcularTotales();
                });

            }

            window.totalForms.val(parseInt(formIdx) + 1);
        }
        function eliminaDetalle(){
            var formIdx = window.totalForms.val();
            $('#id_ventadetalle_set-' + (parseInt(formIdx)-1)).remove();
            window.totalForms.val(Math.max(parseInt(formIdx) - 1, 0));
            calcularTotales();
        }

        function calcularTotales() {
            console.log("calculando");
            var formIdx = parseInt(window.totalForms.val());
            var suma = 0;
            var monto_exento = 0, monto_5 = 0, monto_10 = 0, iva, monto;
            for(var i = 0; i < formIdx ; i ++ ) {
                iva = $('#detalle-' + i + '-producto-iva').val();
                monto = ($('#id_ventadetalle_set-' + i + '-cantidad').val() * $('#id_ventadetalle_set-' + i + '-precio').val());
                if(iva === '5%') {
                    monto_5 += monto;
                    $('input[name=ventadetalle_set-' + i + '-monto_5]').val(monto);
                } else if (iva === '10%') {
                    monto_10 += monto;
                    $('input[name=ventadetalle_set-' + i + '-monto_10]').val(monto);
                } else {
                    monto_exento += monto;
                    $('input[name=ventadetalle_set-' + i + '-monto_exento]').val(monto);
                }

            }
            $('#id_monto_total').val(monto_exento + monto_10 + monto_5);
            $('#id_pago-monto').val(monto_exento + monto_10 + monto_5);
            $('#id_total_exentas').val(monto_exento);
            $('#id_total_iva_10').val(Math.round(monto_10 / 11));
            $('#id_total_iva_5').val(Math.round(monto_5 / 21));
            $('#id_total_iva').val(Math.round(monto_10 / 11) + Math.round(monto_5 / 21));
            $('#subtotal-exentas').text(monto_exento);
            $('#subtotal-iva-5').text(monto_5);
            $('#subtotal-iva-10').text(monto_10);
            $('#id_monto').val(monto_exento + monto_10 + monto_5);



        }

        function calcularTotalIva() {
            var total = parseInt($('#id_total_iva_10').val()) + parseInt($('#id_total_iva_5').val());
            $('#id_total_iva').val(total);
        }

        function setMetodoPago(metodo) {
            $('#id_pago-metodo_pago').val(metodo);

            $('[name^=pago-]').removeAttr('required');

        }
        function calculaVuelto() {
            var mensaje= $('#vueltonegativo');
            mensaje.hide();
            var guardado = $('#guardar_pago');
            guardado.removeAttr("disabled");
            var monto_total= $('#id_monto_total').val();
            var abonado = $('#abonado').val() ;

            var vuelto = abonado-monto_total;
            // noinspection JSAnnotator
            if (vuelto < 0   )   {

                mensaje.show();
                guardado.prop("disabled",true);

            }

            $('#vuelto').val(vuelto) ;


        }

        function guardarVenta() {
            var form = $('form');
            var formData = new FormData(form[0]);
            $.post({
                url: window.guardarVentaUrl,
                data: formData,
                cache: false,
                contentType: false,
                processData: false
            })
            .done(function (data) {
                if(data.success){
                    document.location.href = "/";
                }

            });
        }
