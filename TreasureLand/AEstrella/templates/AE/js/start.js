function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  function cargarListaGrafos() {
    fetch('/listar-grafos/')
      .then(res => res.json())
      .then(data => {
        const select = document.getElementById('grafo-select');
        select.innerHTML = '<option value="">Cargar grafo guardado</option>';
        data.forEach(g => {
          const opt = document.createElement('option');
          opt.value = g.id;
          opt.textContent = g.nombre;
          select.appendChild(opt);
        });
      });
  }

  document.addEventListener('DOMContentLoaded', cargarListaGrafos);
  const csrftoken = getCookie('csrftoken');