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

// Função para atualizar o campo quando uma imagem for selecionada
document.getElementById('logo').addEventListener('change', function (e) {
	const file = e.target.files[0];
	const uploadBox = document.getElementById('fileUploadBox');
	const uploadText = document.getElementById('uploadText');
	
	if (file) {
		// Validar tipo de arquivo
		if (!file.type.startsWith('image/')) {
			alert('Por favor, selecione apenas arquivos de imagem.');
			this.value = '';
			return;
		}
		
		// Validar tamanho (5MB máximo)
		if (file.size > 5 * 1024 * 1024) {
			alert('A imagem deve ter no máximo 5MB.');
			this.value = '';
			return;
		}
		
		// Atualizar texto e aparência
		uploadText.textContent = file.name;
		uploadBox.classList.add('has-image');
	} else {
		// Resetar se nenhum arquivo foi selecionado
		uploadText.textContent = 'Selecionar imagem';
		uploadBox.classList.remove('has-image');
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

document.getElementById('submitButton').addEventListener('click', function (e) {
  const logoInput = document.getElementById('logo');

  if (!logoInput.files.length) {
    logoInput.removeAttribute('name');
  } else {
    logoInput.setAttribute('name', 'file');
  }
  //e.preventDefault();
});