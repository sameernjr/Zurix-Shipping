// Add this to your main.js file
document.addEventListener('DOMContentLoaded', function () {
    const menuIcon = document.querySelector('.menu-icon');
    const navList = document.querySelector('.navdiv ul');

    menuIcon.addEventListener('click', function () {
        menuIcon.classList.toggle('active');
        navList.classList.toggle('active');
    });

    // Close menu when clicking a link
    const navLinks = document.querySelectorAll('.navdiv ul li a, .nav-btn a');
    navLinks.forEach(link => {
        link.addEventListener('click', function () {
            menuIcon.classList.remove('active');
            navList.classList.remove('active');
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function (event) {
        const isClickInsideMenu = navList.contains(event.target);
        const isClickOnMenuIcon = menuIcon.contains(event.target);

        if (!isClickInsideMenu && !isClickOnMenuIcon && navList.classList.contains('active')) {
            menuIcon.classList.remove('active');
            navList.classList.remove('active');
        }
    });
});