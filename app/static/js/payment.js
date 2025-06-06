async function copyPixCode() {
	const pixCode = document.getElementById('pixCode');
	const copySuccess = document.getElementById('copySuccess');
	const copyButton = document.querySelector('.copy-button');
	
	try {
		// Usar API moderna do clipboard
		if (navigator.clipboard && window.isSecureContext) {
			await navigator.clipboard.writeText(pixCode.value);
		} else {
			// Fallback para browsers mais antigos
			pixCode.select();
			document.execCommand('copy');
		}
		
		// Mostrar feedback de sucesso
		copySuccess.style.display = 'block';
		copyButton.innerHTML = '<i class="fas fa-check"></i> Código Copiado!';
		copyButton.style.background = 'var(--success-gradient)';
		
		// Resetar após 3 segundos
		setTimeout(() => {
			copySuccess.style.display = 'none';
			copyButton.innerHTML = '<i class="fas fa-copy"></i> Copiar Código PIX';
			copyButton.style.background = 'var(--primary-gradient)';
		}, 3000);
		
	} catch (error) {
		console.error('Erro ao copiar:', error);
		alert('Erro ao copiar o código. Tente selecionar manualmente.');
	}
}

// Adicionar animação de entrada suave
document.addEventListener('DOMContentLoaded', function () {
	const elements = document.querySelectorAll('.payment-section, .card');
	
	const observer = new IntersectionObserver((entries) => {
		entries.forEach(entry => {
			if (entry.isIntersecting) {
				entry.target.style.opacity = '1';
				entry.target.style.transform = 'translateY(0)';
			}
		});
	});
	
	elements.forEach(el => {
		observer.observe(el);
	});
});