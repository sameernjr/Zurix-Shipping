document.addEventListener('DOMContentLoaded', () => {
    const faqs = document.querySelectorAll('.faq');

    faqs.forEach(faq => {
        faq.addEventListener('click', () => {
            // Close all other Faqs
            faqs.forEach(item => {
                if (item !== faq && item.classList.contains('active')) {
                    item.classList.remove('active');
                }
            });

            // Toogle the Clicked FAQ

            faq.classList.toggle('active');
        });
    });
});
