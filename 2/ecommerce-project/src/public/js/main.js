// JavaScript الأساسي للمتجر
document.addEventListener('DOMContentLoaded', function() {
    console.log('🛍️ متجر إلكتروني يعمل بنجاح!');
    
    // إضافة تأثيرات للصور عند التحميل
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => imageObserver.observe(img));
    }
    
    // إدارة السلة (سيتم تطويره لاحقاً)
    const cartButtons = document.querySelectorAll('.add-to-cart');
    cartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            addToCart(productId);
        });
    });
});

function addToCart(productId) {
    console.log(`تم إضافة المنتج ${productId} إلى السلة`);
    // سيتم تطويره في وحدة السلة لاحقاً
}

// وظائف مساعدة
function formatPrice(price) {
    return new Intl.NumberFormat('ar-SA', {
        style: 'currency',
        currency: 'SAR'
    }).format(price);
}
