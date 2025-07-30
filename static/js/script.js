// ===== VARIABLES GLOBALES =====
let currentSlide = 0;
let slideInterval;
const slideDelay = 5000; // 5 segundos

// ===== INICIALIZACIÓN =====
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar componentes
    initCarousel();
    initAnimations();
    initModal();
    initCarrito();
    initForms();
    
    // Agregar espacio para navbar fijo
    document.body.style.paddingTop = '80px';
});

// ===== CARRUSEL =====
function initCarousel() {
    const carousel = document.querySelector('.carousel');
    if (!carousel) return;
    
    const container = carousel.querySelector('.carousel-container');
    const slides = carousel.querySelectorAll('.carousel-slide');
    const prevBtn = carousel.querySelector('.carousel-prev');
    const nextBtn = carousel.querySelector('.carousel-next');
    const indicators = carousel.querySelector('.carousel-indicators');
    
    if (!container || slides.length === 0) return;
    
    // Crear indicadores
    if (indicators) {
        indicators.innerHTML = '';
        slides.forEach((_, index) => {
            const indicator = document.createElement('div');
            indicator.className = `carousel-indicator ${index === 0 ? 'active' : ''}`;
            indicator.addEventListener('click', () => goToSlide(index));
            indicators.appendChild(indicator);
        });
    }
    
    // Event listeners para navegación
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);
    
    // Auto-play
    startSlideshow();
    
    // Pausar al hover
    carousel.addEventListener('mouseenter', stopSlideshow);
    carousel.addEventListener('mouseleave', startSlideshow);
    
    function goToSlide(index) {
        currentSlide = index;
        updateCarousel();
    }
    
    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        updateCarousel();
    }
    
    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        updateCarousel();
    }
    
    function updateCarousel() {
        const translateX = -currentSlide * 100;
        container.style.transform = `translateX(${translateX}%)`;
        
        // Actualizar indicadores
        const allIndicators = indicators?.querySelectorAll('.carousel-indicator');
        if (allIndicators) {
            allIndicators.forEach((indicator, index) => {
                indicator.classList.toggle('active', index === currentSlide);
            });
        }
    }
    
    function startSlideshow() {
        stopSlideshow();
        slideInterval = setInterval(nextSlide, slideDelay);
    }
    
    function stopSlideshow() {
        if (slideInterval) {
            clearInterval(slideInterval);
            slideInterval = null;
        }
    }
}

// ===== ANIMACIONES EN SCROLL =====
function initAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    if (animatedElements.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

// ===== MODAL =====
function initModal() {
    const modals = document.querySelectorAll('.modal');
    const modalTriggers = document.querySelectorAll('[data-modal]');
    const modalCloses = document.querySelectorAll('.modal-close');
    
    // Abrir modales
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            const modalId = trigger.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            if (modal) openModal(modal);
        });
    });
    
    // Cerrar modales
    modalCloses.forEach(close => {
        close.addEventListener('click', (e) => {
            const modal = close.closest('.modal');
            if (modal) closeModal(modal);
        });
    });
    
    // Cerrar al hacer clic fuera
    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal(modal);
        });
    });
    
    // Cerrar con ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal[style*="block"]');
            if (openModal) closeModal(openModal);
        }
    });
}

function openModal(modal) {
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModal(modal) {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// ===== CARRITO =====
function initCarrito() {
    // Botones agregar al carrito
    const addToCartBtns = document.querySelectorAll('.btn-agregar-carrito');
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', agregarAlCarrito);
    });
    
    // Actualizar cantidad en carrito
    const cantidadInputs = document.querySelectorAll('.cantidad-input');
    cantidadInputs.forEach(input => {
        input.addEventListener('change', actualizarCantidad);
    });
    
    // Botones eliminar del carrito
    const eliminarBtns = document.querySelectorAll('.btn-eliminar-carrito');
    eliminarBtns.forEach(btn => {
        btn.addEventListener('click', eliminarDelCarrito);
    });
}

async function agregarAlCarrito(e) {
    e.preventDefault();
    const platoId = this.getAttribute('data-plato-id');
    
    if (!platoId) {
        showAlert('Error al agregar producto', 'error');
        return;
    }
    
    try {
        const response = await fetch(`/agregar-carrito/${platoId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert(data.message, 'success');
            actualizarContadorCarrito(data.total_items);
        } else {
            showAlert('Error al agregar producto', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error de conexión', 'error');
    }
}

async function actualizarCantidad(e) {
    const itemId = this.getAttribute('data-item-id');
    const cantidad = parseInt(this.value);
    
    if (!itemId || cantidad < 0) return;
    
    try {
        const response = await fetch(`/actualizar-carrito/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ cantidad: cantidad })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Actualizar subtotal
            const subtotalElement = this.closest('.carrito-item').querySelector('.subtotal');
            if (subtotalElement) {
                subtotalElement.textContent = `€${data.subtotal.toFixed(2)}`;
            }
            
            // Actualizar total
            const totalElement = document.querySelector('.carrito-total');
            if (totalElement) {
                totalElement.textContent = `€${data.total.toFixed(2)}`;
            }
            
            // Si cantidad es 0, eliminar elemento
            if (cantidad === 0) {
                this.closest('.carrito-item').remove();
            }
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error al actualizar carrito', 'error');
    }
}

function eliminarDelCarrito(e) {
    e.preventDefault();
    
    if (confirm('¿Estás seguro de que quieres eliminar este producto del carrito?')) {
        window.location.href = this.href;
    }
}

function actualizarContadorCarrito(count) {
    const contador = document.querySelector('.carrito-count');
    if (contador) {
        contador.textContent = count;
        contador.style.display = count > 0 ? 'inline' : 'none';
    }
}

// ===== FORMULARIOS =====
function initForms() {
    // Validación en tiempo real
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', clearErrors);
        });
        
        form.addEventListener('submit', validateForm);
    });
    
    // Formulario de contacto
    const contactForm = document.getElementById('contacto-form');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactForm);
    }
}

function validateField(e) {
    const field = e.target;
    const value = field.value.trim();
    let isValid = true;
    let message = '';
    
    // Limpiar errores previos
    clearFieldError(field);
    
    // Validaciones por tipo
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'Este campo es obligatorio';
    } else if (field.type === 'email' && value && !isValidEmail(value)) {
        isValid = false;
        message = 'Introduce un email válido';
    } else if (field.type === 'password' && value && value.length < 8) {
        isValid = false;
        message = 'La contraseña debe tener al menos 8 caracteres';
    }
    
    if (!isValid) {
        showFieldError(field, message);
    }
    
    return isValid;
}

function validateForm(e) {
    const form = e.target;
    const fields = form.querySelectorAll('input, textarea, select');
    let isValid = true;
    
    fields.forEach(field => {
        if (!validateField({ target: field })) {
            isValid = false;
        }
    });
    
    if (!isValid) {
        e.preventDefault();
        showAlert('Por favor, corrige los errores en el formulario', 'error');
    }
}

function handleContactForm(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    // Mostrar loading
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Enviando...';
    submitBtn.disabled = true;
    
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.text())
    .then(html => {
        // Reemplazar formulario con respuesta
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newForm = doc.querySelector('#contacto-form');
        
        if (newForm) {
            form.innerHTML = newForm.innerHTML;
            initForms(); // Reinicializar eventos
        }
        
        showAlert('Mensaje enviado correctamente', 'success');
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error al enviar mensaje', 'error');
    })
    .finally(() => {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    });
}

// ===== UTILIDADES =====
function showAlert(message, type = 'info') {
    // Crear elemento de alerta
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    // Agregar al DOM
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alert, container.firstChild);
    
    // Auto-remove después de 5 segundos
    setTimeout(() => {
        alert.remove();
    }, 5000);
    
    // Scroll hacia arriba para mostrar alerta
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('error');
    
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    errorElement.style.color = '#DC3545';
    errorElement.style.fontSize = '0.875rem';
    errorElement.style.marginTop = '0.25rem';
    
    field.parentNode.appendChild(errorElement);
}

function clearFieldError(field) {
    field.classList.remove('error');
    const errorElement = field.parentNode.querySelector('.field-error');
    if (errorElement) {
        errorElement.remove();
    }
}

function clearErrors(e) {
    clearFieldError(e.target);
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    
    return cookieValue || document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

// ===== NAVEGACIÓN SUAVE =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== NAVBAR SCROLL =====
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 100) {
            navbar.style.background = 'linear-gradient(135deg, rgba(44, 24, 16, 0.95), rgba(139, 69, 19, 0.95))';
            navbar.style.backdropFilter = 'blur(10px)';
        } else {
            navbar.style.background = 'linear-gradient(135deg, var(--color-oscuro), var(--color-secundario))';
            navbar.style.backdropFilter = 'none';
        }
    }
});

// ===== LAZY LOADING PARA IMÁGENES =====
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

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ===== OPTIMIZACIÓN DE RENDIMIENTO =====
// Debounce function para eventos que se disparan frecuentemente
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Aplicar debounce a eventos de scroll y resize
window.addEventListener('scroll', debounce(() => {
    // Acciones en scroll con throttling
}, 100));

window.addEventListener('resize', debounce(() => {
    // Recalcular dimensiones si es necesario
    initCarousel();
}, 250));
