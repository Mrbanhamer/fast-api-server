// Use the absolute path starting with /front_end/
fetch('/front_end/header.html') 
  .then(response => {
    if (!response.ok) {
      // This will tell you if it's a 404 (Not Found)
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.text();
  })
  .then(data => {
    const placeholder = document.getElementById('header-placeholder');
    if (placeholder) {
      placeholder.innerHTML = data;
    } else {
      console.error("Could not find element with ID 'header-placeholder'");
    }
  })
  .catch(error => console.error('Error loading header:', error));