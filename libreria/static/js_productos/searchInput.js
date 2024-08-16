// Obtener el elemento de entrada de búsqueda
var searchInput = document.getElementById("searchInput");

// Obtener la tabla
var table = document.getElementById("myTable");

// Añadir un evento de escucha al elemento de entrada de búsqueda
searchInput.addEventListener("keyup", function() {
  var filter = searchInput.value.toLowerCase(); // Obtener el valor de búsqueda y convertirlo a minúsculas
  var rows = table.getElementsByTagName("tr"); // Obtener todas las filas de la tabla

  // Recorrer todas las filas y mostrar u ocultar aquellas que coincidan con la búsqueda
  for (var i = 0; i < rows.length; i++) {
    var name = rows[i].getElementsByTagName("td")[0]; // Obtener el valor de la celda "Nombre"
    if (name) {
      var text = name.innerText.toLowerCase(); // Obtener el texto de la celda y convertirlo a minúsculas
      if (text.includes(filter)) {
        rows[i].style.display = ""; // Mostrar la fila si coincide con la búsqueda
      } else {
        rows[i].style.display = "none"; // Ocultar la fila si no coincide con la búsqueda
      }
    }
  }
});
