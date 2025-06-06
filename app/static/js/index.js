document.getElementById('tipo').addEventListener('change', function () {
	const tipo = this.value;
	const locationField = document.getElementById('locationField');
	const locationInput = document.getElementById('location');
	const keyField = document.getElementById('keyField');
	const keyInput = document.getElementById('chave');
	const staticFields = document.getElementById('staticFields');
	const tipoRow = document.getElementById('tipoRow');
	
	if (tipo === 'dinamico') {
		// Exibe location, esconde chave
		locationField.classList.remove('hidden');
		locationField.style.display = '';
		locationInput.setAttribute('required', 'required');
		
		keyField.style.display = 'none';
		keyInput.removeAttribute('required');
		
		staticFields.style.display = 'none';
		
		// Insere locationField na linha, se necessário
		if (!tipoRow.contains(locationField)) {
			tipoRow.appendChild(locationField);
		}
		
	} else {
		// Exibe chave, esconde location
		locationField.classList.add('hidden');
		locationInput.removeAttribute('required');
		
		keyField.style.display = '';
		keyInput.setAttribute('required', 'required');
		
		staticFields.style.display = '';
	}
});


// Aplica máscaras dinâmicas no campo chave e fixa no campo CEP
document.addEventListener('DOMContentLoaded', function () {
	var tipoSelect = document.getElementById('tipo');
	var chaveInput = document.getElementById('chave');
	var maskRef = null;
	
	function aplicarMascara(tipo) {
		if (maskRef) {
			maskRef.destroy();
			maskRef = null;
		}
		chaveInput.type = 'text';
		chaveInput.value = '';
		chaveInput.removeAttribute('pattern');
		
		if (tipo === 'celular') {
			maskRef = IMask(chaveInput, {mask: '(00) 00000-0000'});
		} else if (tipo === 'cpf') {
			maskRef = IMask(chaveInput, {mask: '000.000.000-00'});
		} else if (tipo === 'cnpj') {
			maskRef = IMask(chaveInput, {mask: '00.000.000/0000-00'});
		} else if (tipo === 'email') {
			chaveInput.type = 'email';
			chaveInput.setAttribute('pattern', '[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,}$');
		}
		// Para outros tipos, sem máscara
	}
	
	tipoSelect.addEventListener('change', function () {
		aplicarMascara(this.value);
	});
	
	// Máscara fixa para o campo CEP
	var cepInput = document.getElementById('zipcode');
	if (cepInput) {
		IMask(cepInput, {mask: '00000-000'});
	}
});