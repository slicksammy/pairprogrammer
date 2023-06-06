document.addEventListener('DOMContentLoaded', function() {
  var markdownContainer = document.getElementById('markdown-container');
  if (markdownContainer) {
    var readmeContent = markdownContainer.innerText;
    markdownContainer.innerHTML = window.marked.parse(readmeContent);
  }
});
