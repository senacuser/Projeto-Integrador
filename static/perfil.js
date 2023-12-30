function saveProfile() {
    const userName = document.getElementById('user-name').value;
    const userEmail = document.getElementById('user-email').value;
    const userLocation = document.getElementById('user-location').value;
    
    // Você pode salvar esses dados onde preferir (localmente, em um banco de dados, etc.)
    // Por enquanto, apenas mostrando os dados no console como exemplo
    console.log('Nome:', userName);
    console.log('Email:', userEmail);
    console.log('Localização:', userLocation);
  }

  document.getElementById('photo-input').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
      document.getElementById('user-photo').src = e.target.result;
    };

    reader.readAsDataURL(file);
  });