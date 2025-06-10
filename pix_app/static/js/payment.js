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

// Função para baixar o QR Code
function downloadQRCode() {
  const qrImage = document.getElementById('qrCodeImage');
  
  // Extrair a extensão do arquivo da URL
  const imageUrl = qrImage.src;
  let extension = 'png'; // extensão padrão
  
  // Se for data URL (base64), verificar o tipo MIME
  if (imageUrl.startsWith('data:')) {
    const mimeType = imageUrl.split(',')[0].split(':')[1].split(';')[0];
    if (mimeType === 'image/jpeg') extension = 'jpg';
    else if (mimeType === 'image/png') extension = 'png';
    else if (mimeType === 'image/gif') extension = 'gif';
    else if (mimeType === 'image/webp') extension = 'webp';
  } else {
    // Se for URL normal, extrair extensão do caminho
    const urlPath = imageUrl.split('?')[0]; // Remove query parameters
    const match = urlPath.match(/\.([a-zA-Z0-9]+)$/);
    if (match) {
      extension = match[1].toLowerCase();
    }
  }
  
  // Criar o link de download
  const link = document.createElement('a');
  link.download = `qr-code-pix.${extension}`;
  link.href = qrImage.src;
  link.target = '_blank';
  
  // Simular o clique no link para iniciar o download
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  
  // Mostrar notificação de sucesso
  showDownloadSuccess();
}

// Função para mostrar notificação de sucesso do download
function showDownloadSuccess() {
	const successDiv = document.getElementById('downloadSuccess');
	successDiv.style.display = 'block';
	
	setTimeout(() => {
		successDiv.style.display = 'none';
	}, 3000);
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