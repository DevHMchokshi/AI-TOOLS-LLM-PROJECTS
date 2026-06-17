document.addEventListener('DOMContentLoaded', () => {
    // 1. Hero Carousel Logic
    const carouselWrapper = document.getElementById('carousel-wrapper');
    const dots = document.querySelectorAll('.dot');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    let currentSlide = 0;
    const totalSlides = dots.length;
    let autoPlayInterval;

    function updateCarousel() {
        // Move wrapper
        carouselWrapper.style.transform = `translateX(-${currentSlide * 100}%)`;
        // Update dots
        dots.forEach(dot => dot.classList.remove('active'));
        dots[currentSlide].classList.add('active');
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        updateCarousel();
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
        updateCarousel();
    }

    function startAutoPlay() {
        autoPlayInterval = setInterval(nextSlide, 5000);
    }

    function stopAutoPlay() {
        clearInterval(autoPlayInterval);
    }

    prevBtn.addEventListener('click', () => {
        prevSlide();
        stopAutoPlay();
        startAutoPlay();
    });

    nextBtn.addEventListener('click', () => {
        nextSlide();
        stopAutoPlay();
        startAutoPlay();
    });

    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            updateCarousel();
            stopAutoPlay();
            startAutoPlay();
        });
    });

    startAutoPlay();

    // 2. Add to Cart & Toast Notification
    const addToCartBtns = document.querySelectorAll('.add-to-cart-btn');
    const cartBadge = document.getElementById('cart-badge');
    let cartCount = 0;

    function showToast(message) {
        const toastContainer = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = 'toast success';
        toast.innerHTML = `<i class='bx bxs-check-circle'></i> <span>${message}</span>`;
        
        toastContainer.appendChild(toast);
        
        // Remove toast after animation (3s)
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Update cart count
            cartCount++;
            cartBadge.textContent = cartCount;
            
            // Add a little pop animation to the badge
            cartBadge.classList.add('bump');
            setTimeout(() => {
                cartBadge.classList.remove('bump');
            }, 200);

            // Show success toast
            const productName = this.parentElement.querySelector('.product-name').textContent;
            showToast(`${productName} added to cart!`);
        });
    });

    // 3. Heart Icon (Wishlist) Toggle
    const heartIcons = document.querySelectorAll('.favorite-icon');
    heartIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            this.classList.toggle('active');
            
            // Change icon from outline to solid when active
            if (this.classList.contains('active')) {
                this.classList.remove('bx-heart');
                this.classList.add('bxs-heart');
                showToast("Added to Wishlist");
            } else {
                this.classList.remove('bxs-heart');
                this.classList.add('bx-heart');
                showToast("Removed from Wishlist");
            }
        });
    });

    // 4. Price Slider Logic
    const priceRange = document.getElementById('price-range');
    const priceValue = document.getElementById('price-value');
    
    if (priceRange && priceValue) {
        priceRange.addEventListener('input', (e) => {
            // Map 0-100 to 0-1,00,000 for demonstration
            const val = e.target.value;
            const mappedPrice = val * 1000;
            priceValue.textContent = mappedPrice.toLocaleString('en-IN');
        });
    }
});
