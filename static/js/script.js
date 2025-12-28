/* Toggle sidebar */
const sidebarToggle = document.querySelector("#sidebar-toggle");
sidebarToggle.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("collapsed");
});

/* Loading Spinner */
const spinnerWrapperEl = document.querySelector('.spinner-wrapper');
window.addEventListener('load', () => {
    spinnerWrapperEl.style.opacity = '0';
    setTimeout(() => {
        spinnerWrapperEl.style.display = 'none';
    }, 200);
});

/* DataTable */
$(document).ready(function () {
    $('#myTable').DataTable();
});
