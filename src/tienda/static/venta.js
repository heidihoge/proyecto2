

        function notifyError(message) {
            PNotify.prototype.options.delay = 3000;
            new PNotify({
                title: 'Error',
                text: message,
                type: 'error',
                styling: 'bootstrap3'
            });
        }
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
            window.totalForms.val(0);
            
            useAutonumericCurrency('#id_monto_total');
            useAutonumericCurrency('#id_total_iva_10');
            useAutonumericCurrency('#id_total_iva_5');
            useAutonumericCurrency('#id_total_iva');
            useAutonumericCurrency('#id_total_grav_exentas');
            useAutonumericCurrency('#id_total_grav_10');
            useAutonumericCurrency('#id_total_grav_5');
            useAutonumericCurrency('#subtotal-exentas');
            useAutonumericCurrency('#subtotal-iva-5');
            useAutonumericCurrency('#subtotal-iva-10');
            // pago
            useAutonumericCurrency('#monto-restante');
            useAutonumericCurrency('#id_pago-monto');
            useAutonumericCurrency('#id_pago-monto_efectivo');
            useAutonumericCurrency('#id_pago-monto_tarjeta');
            useAutonumericCurrency('#id_pago-monto_cheque');
            useAutonumericCurrency('#id_pago-monto_efectivo_abonado');
            useAutonumericCurrency('#id_pago-monto_efectivo_vuelto');
            setAutonumericCurrency('#monto-restante', 0);
            setAutonumericCurrency('#id_pago-monto', 0);
            setAutonumericCurrency('#id_pago-monto_efectivo', 0);
            setAutonumericCurrency('#id_pago-monto_tarjeta', 0);
            setAutonumericCurrency('#id_pago-monto_cheque', 0);
            setAutonumericCurrency('#id_pago-monto_efectivo_abonado', 0);
            setAutonumericCurrency('#id_pago-monto_efectivo_vuelto', 0);

            $('#pago input').on('change ifChanged keypress', function(){
                logicaPago();
            });

            $('#id_pago-monto').attr('readonly', true);
            $('#id_monto_total').attr('readonly', true);
            $('#id_total_iva_10').attr('readonly', true);
            $('#id_total_iva_5').attr('readonly', true);
            $('#id_total_exentas').attr('readonly', true);
            $('#id_total_iva').attr('readonly', true);
            setMetodoPago('Efectivo');



            $('form input').keydown(function (event) {
                if (event.keyCode === 13) {
                    event.preventDefault();
                    return false;
                }
            });

            $('#id_total_iva_10,#id_total_iva_5').on('change keypress', calcularTotalIva);

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
            calcularTotales();
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
            var detalles = $('#detalles');
            if(cuenta && detalles.find('[cuenta-id=' + cuenta.pk + ']').length > 0) {
                return;
            }
            row.attr('id', 'id_ventadetalle_set-' + parseInt(formIdx));
            row.append(window.rowTemplate.html().replace(/__prefix__/g, formIdx));
            row.find('.numero').append(parseInt(formIdx) + 1);
            detalles.append(row);
            $('#id_ventadetalle_set-' + formIdx + '-cantidad,#id_ventadetalle_set-' + formIdx + '-precio')
                .on('change keypress', function(){
                    calcularTotales();
                });

            useAutonumericCurrency('#id_ventadetalle_set-' + formIdx + '-monto_exento');
            useAutonumericCurrency('#id_ventadetalle_set-' + formIdx + '-monto_5');
            useAutonumericCurrency('#id_ventadetalle_set-' + formIdx + '-monto_10');
            useAutonumericCurrency('#id_ventadetalle_set-' + formIdx + '-precio');

            $(row.find("input[name=ventadetalle_set-" + formIdx + "-monto_exento]")).attr("readonly",true);
            $(row.find("input[name=ventadetalle_set-" + formIdx + "-monto_5]")).attr("readonly",true);
            $(row.find("input[name=ventadetalle_set-" + formIdx + "-monto_10]")).attr("readonly", true);

            if (cuenta) {
                row.attr('cuenta-id', cuenta.pk);
                row.find(".select2").remove();
                // Si producto es texto, entonces se trata de una cuota!!!
                var productoDescripcion = $("<input type='text' name='ventadetalle_set-"  + formIdx + "-producto-descripcion'></input>");
                productoDescripcion.addClass("form-control");
                productoDescripcion.val(cuenta.detalle);
                $(row.find("select")).replaceWith(productoDescripcion);


                setAutonumericCurrency('#id_ventadetalle_set-' + formIdx + '-monto_10', cuenta.monto);
                setAutonumericCurrency("#id_ventadetalle_set-" + formIdx + "-precio", cuenta.monto);
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
                    setAutonumericCurrency('#id_ventadetalle_set-' + formIdx + '-precio', data.precio_venta);
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

                setAutonumericCurrency('#id_ventadetalle_set-' + i + '-monto_5', 0);
                setAutonumericCurrency('#id_ventadetalle_set-' + i + '-monto_10', 0);
                setAutonumericCurrency('#id_ventadetalle_set-' + i + '-monto_exento', 0);
                monto = ($('#id_ventadetalle_set-' + i + '-cantidad').val() * getAutonumericCurrency('#id_ventadetalle_set-' + i + '-precio')) || 0;
                if(iva === '5%') {
                    monto_5 += monto;
                    setAutonumericCurrency('#id_ventadetalle_set-' + i + '-monto_5', monto);
                } else if (iva === '10%') {
                    monto_10 += monto;
                    setAutonumericCurrency('#id_ventadetalle_set-' + i + '-monto_10', monto);
                } else {
                    monto_exento += monto;
                    setAutonumericCurrency('#id_ventadetalle_set-' + i + '-monto_exento', monto);
                }

            }
            setAutonumericCurrency('#id_monto_total', monto_exento + monto_10 + monto_5);
            setAutonumericCurrency('#id_pago-monto', monto_exento + monto_10 + monto_5);
            setAutonumericCurrency('#id_total_grav_10', Math.round(monto_10));
            setAutonumericCurrency('#id_total_grav_5',Math.round(monto_5));
            setAutonumericCurrency('#id_total_grav_exentas', Math.round(monto_exento));
            setAutonumericCurrency('#id_total_iva_10', Math.round(monto_10 / 11));
            setAutonumericCurrency('#id_total_iva_5', Math.round(monto_5 / 21));
            setAutonumericCurrency('#id_total_iva', Math.round(monto_10 / 11) + Math.round(monto_5 / 21));
            setAutonumericCurrency('#subtotal-exentas', monto_exento);
            setAutonumericCurrency('#subtotal-iva-5', monto_5);
            setAutonumericCurrency('#subtotal-iva-10', monto_10);



        }

        function calcularTotalIva() {
            var total = parseInt($('#id_total_iva_10').val()) + parseInt($('#id_total_iva_5').val());
            $('#id_total_iva').val(total);
        }

        function setMetodoPago(metodo) {
            var guardado = $('#guardar_pago');
            guardado.removeAttr("disabled");

            $('#id_pago-metodo_pago').val(metodo);

            $('[name^=pago-]').removeAttr('required');

        }

        function calculaVuelto() {
            var mensaje= $('#vueltonegativo');
            mensaje.hide();
            var monto_total = getAutonumericCurrency('#id_pago-monto_efectivo');
            var abonado = getAutonumericCurrency('#id_pago-monto_efectivo_abonado');

            var vuelto = abonado-monto_total;
            // noinspection JSAnnotator
            if (vuelto < 0   )   {

                setAutonumericCurrency('#id_pago-monto_efectivo_vuelto', 0);

                mensaje.show();

                return {
                    error: true
                }

            }

            setAutonumericCurrency('#id_pago-monto_efectivo_vuelto', vuelto);

            return {
                error: false
            }
        }

        function setErrores(errores, prefix) {
            Object.keys(errores).forEach(function(field){
                var feedback = $('[name=' + prefix + field + ']')
                    .siblings('.feedback-message');
                feedback.html("");
                errores[field].forEach(function(message) {
                    feedback.append($('<p class="text-danger">' + message + '</p>'));
                })
            });
        }

        function guardarVenta() {
            var form = $('form');
            var formData = new FormData(form[0]);
            var pagoModal = $("#pago");
            $('.feedback-message').html('');
            var feedbackDetalles = $('#feedback-detalles');
            feedbackDetalles.html('');
            if(window.totalForms.val() > 0) {
                $.post({
                    url: window.guardarVentaUrl,
                    data: formData,
                    cache: false,
                    contentType: false,
                    processData: false
                })
                .done(function (data) {
                    if(data.success){

                        document.location.href = data.redirect;
                    } else {
                        notifyError("Error al guardar pago, verifique los campos");
                        if(data.clienteErrors) {

                            pagoModal.modal('hide');
                            setErrores(data.clienteErrors, 'cliente-')

                        }
                        for (var i=0; i< data.detalleErrors.length; i++) {
                            if(!$.isEmptyObject(data.detalleErrors[i])) {
                                pagoModal.modal('hide');
                                feedbackDetalles.append($('<p class="text-danger">Verifica que los detalles esten completos' + '.</p>'));
                            }
                        }
                        if(data.pagoErrorsExtra) {
                            setErrores(data.pagoErrorsExtra, 'pago-');
                        }
                    }

                });
            } else {
                pagoModal.modal('hide');
                notifyError("Error al guardar pago, verifique los campos");
                feedbackDetalles.append($('<p class="text-danger">Agrega al menos 1 detalle.</p>'));
            }

        }
        function logicaPago() {

            var error = false;

            function mediosDePago() {
                var efectivo = $('#id_pago-pago_efectivo').prop('checked');
                var tarjeta = $('#id_pago-pago_tarjeta').prop('checked');
                var cheque = $('#id_pago-pago_cheque').prop('checked');
                var cantidad = [tarjeta, efectivo, cheque].filter(function(v){return v}).length;
                return {
                    cantidad: cantidad,
                    efectivo: efectivo,
                    tarjeta: tarjeta,
                    cheque: cheque
                }
            }

            var pagos = mediosDePago();

            var montoTotal = getAutonumericCurrency('#id_pago-monto');

            var montoEfectivoInput = $('#id_pago-monto_efectivo');
            var montoTarjetaInput = $('#id_pago-monto_tarjeta');
            var montoChequeInput = $('#id_pago-monto_cheque');
            var mensajeMedioPago = $('#no-medio-pago');
            var mensajeMayorATotal = $('#mayor-a-total-pago');
            var mensajeMontoCero = $('#monto-cero-pago');
            var botonGuardar = $('#guardar_pago');

            botonGuardar.attr('disabled', true);

            montoEfectivoInput.attr('readonly', true);
            montoTarjetaInput.attr('readonly', true);
            montoChequeInput.attr('readonly', true);
            mensajeMedioPago.hide();
            mensajeMayorATotal.hide();
            mensajeMontoCero.hide();

            setAutonumericCurrency('#monto-restante', 0);

            if (montoTotal === 0) {
                error = true;
                mensajeMontoCero.show();
            }

            if (pagos.cantidad === 0) {
                mensajeMedioPago.show();
                error = true;
            } else if (pagos.cantidad === 1) {
                setAutonumericCurrency('#monto-restante', 0);
                if (pagos.efectivo) {
                    setAutonumericCurrency('#id_pago-monto_efectivo', montoTotal);
                    setAutonumericCurrency('#id_pago-monto_tarjeta', 0);
                    setAutonumericCurrency('#id_pago-monto_cheque', 0);
                }
                else if (pagos.tarjeta) {
                    setAutonumericCurrency('#id_pago-monto_efectivo', 0);
                    setAutonumericCurrency('#id_pago-monto_tarjeta', montoTotal);
                    setAutonumericCurrency('#id_pago-monto_cheque', 0);
                }
                else if (pagos.cheque) {
                    setAutonumericCurrency('#id_pago-monto_efectivo', 0);
                    setAutonumericCurrency('#id_pago-monto_tarjeta', 0);
                    setAutonumericCurrency('#id_pago-monto_cheque', montoTotal);
                }
            } else {
                var montoParcial = 0;
                if(pagos.efectivo) {
                    montoParcial += getAutonumericCurrency('#id_pago-monto_efectivo');
                }
                if(pagos.tarjeta) {
                    montoParcial += getAutonumericCurrency('#id_pago-monto_tarjeta');
                }
                if(pagos.cheque) {
                    montoParcial += getAutonumericCurrency('#id_pago-monto_cheque');
                }

                if (montoTotal < montoParcial) {
                    mensajeMayorATotal.show();
                    error = true;
                } else if (montoTotal > montoParcial) {
                    error = true;
                }
                setAutonumericCurrency('#monto-restante', Math.max(montoTotal - montoParcial, 0));


                montoEfectivoInput.removeAttr('readonly');
                montoTarjetaInput.removeAttr('readonly');
                montoChequeInput.removeAttr('readonly');
            }

            error = error || calculaVuelto().error;


            if(!error) {
                botonGuardar.removeAttr('disabled');
            }

        }
