
function mascarachave(tipo) {

    $("#chave").val('');
    $("#location").val('');
    $("#chave").inputmask('remove');
    $("#chave").attr('placeholder', '');
    $("#labelchave").html('Chave Pix (obrigatória)');
    $("#divchave").show();
    $("#estatico").show();
    $("#divlocation").hide();
    $("#chave").attr('required', 'required');
    $("#location").removeAttr('required');

    if (tipo == 'nenhuma') {
        $("#chave").attr('placeholder', 'Selecione o tipo de chave');
        $("#chave").attr('disabled', 'disabled');
    } else {
        $("#chave").removeAttr('disabled');
        switch(tipo) {
            case 'aleatoria':
                $("#chave").attr('placeholder', '________-____-____-____-____________');
                $("#chave").inputmask({ regex: "[0-fA-F]{8}-[0-fA-F]{4}-[0-fA-F]{4}-[0-fA-F]{4}-[0-fA-F]{12}" });
                break;
            case 'email':
                $("#chave").attr('placeholder', '_@_._');
                $("#chave").inputmask("email");
                break;
            case 'celular':
                $("#chave").attr('placeholder', '(__) ____-____');
                $("#chave").inputmask({ mask: ['(99) 9999-9999', '(99) 99999-9999' ], inputmode: "numeric" });
                break;
            case 'cpf':
                $("#chave").attr('placeholder', '___.___.___-__');
                $("#chave").inputmask('999.999.999-99', { inputmode: "numeric" });
                break;
            case 'cnpj':
                $("#chave").attr('placeholder', '__.___.___/____-__');
                $("#chave").inputmask({ mask: '99.999.999/9999-99', inputmode: "numeric" });
                break;
            case 'dinamico':
                $("#divlocation").show();
                $("#divchave").hide();
                $("#estatico").hide();
                $("#chave").removeAttr('required');
                $("#location").attr('required', 'required');
                break;
        }
    }
}

function aviso() {
    if (this.value != "") {
        $("#aviso"+this.name).show();
    } else {
        $("#aviso"+this.name).hide();
    }
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

$(function () {
    $("#valor").inputmask("currency", { prefix: "R$ ", radixPoint: "," });
    $("#nome").inputmask({ regex: "[^\.\/\\\|\$~@#!%&]{0,25}" });
    $("#txid").inputmask({ regex: "[a-zA-Z0-9]{0,25}" });

    mascarachave($("#tipo").val());

    $("#tipo").on("change", function () {
        mascarachave($(this).val());
    });

    $("#nome").on("keyup", aviso);
    $("#txid").on("keyup", aviso);
    $("#nome").keyup();
    $("#txid").keyup();

    if (getCookie('tipo') != "") {
        setTimeout(function() {
            $("#tipo").val(getCookie('tipo'));
            mascarachave($("#tipo").val());
        }, 100);

        switch(getCookie('tipo')) {
            case 'dinamico':
                if (getCookie('location') != "") {
                    setTimeout(function() {
                        $("#location").val(getCookie('location'));
                    }, 200);
                }
                break;
            case 'nenhuma':
                break;
            default:
                if (getCookie('chave') != "") {
                    setTimeout(function() {
                        $("#chave").removeAttr('disabled');
                        $("#chave").val(getCookie('chave'));
                    }, 200);
                }
                break;
        }        
    }

    $("#tipo").focus();
});