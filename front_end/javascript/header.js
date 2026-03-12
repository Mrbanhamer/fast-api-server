fetch('header.html') // Added a forward slash to start from the root
  .then(response => response.text())
  .then(data => {
    document.getElementById('header-placeholder').innerHTML = data;
  })
  .catch(error => console.error('Error:', error));