function toggleSidebar() {
    var sidebar = document.querySelector('.sidebar');
    if (sidebar.style.width === '0px' || sidebar.style.width === '') {
      sidebar.style.width = '200px';
    } else {
      sidebar.style.width = '0px';
    }
  }

  function resizeSidebar() {
    var sidebar = document.querySelector('.sidebar');
    if (window.innerWidth < 600) {
      sidebar.style.width = '0px';
    } else {
      sidebar.style.width = '200px';
    }
  }
  
  window.addEventListener('resize', resizeSidebar);
  
  // Ejecuta la función al cargar la página
  window.addEventListener('load', resizeSidebar);
  