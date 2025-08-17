// 全局动画脚本
(function() {
    'use strict';

    // 滚动动画
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                        entry.target.classList.add('animate');
                        // 添加额外的动画类
                        if (entry.target.classList.contains('scroll-animate')) {
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'translateY(0)';
                        }
                        observer.unobserve(entry.target);
                    }
            });
        }, observerOptions);

        // 观察所有需要滚动动画的元素
        const scrollElements = document.querySelectorAll('.scroll-animate, .card-hover, .dashboard-card, .discussion-card');
        scrollElements.forEach(el => {
            observer.observe(el);
        });
    }

    // 导航栏滚动效果
    function initNavbarScroll() {
        let lastScrollTop = 0;
        const navbar = document.querySelector('.navbar');
        
        if (!navbar) return;

        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > 100) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
            
            lastScrollTop = scrollTop;
        });
    }

    // 打字机效果
    function initTypewriterEffect() {
        const typewriterElements = document.querySelectorAll('.typewriter');
        
        typewriterElements.forEach(element => {
            const text = element.getAttribute('data-text') || element.textContent;
            element.textContent = '';
            let i = 0;
            
            function typeWriter() {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, 100);
                }
            }
            
            // 当元素进入视口时开始打字
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        typeWriter();
                        observer.unobserve(entry.target);
                    }
                });
            });
            
            observer.observe(element);
        });
    }

    // 数字计数动画
    function initCounterAnimation() {
        const counterElements = document.querySelectorAll('.counter');
        
        counterElements.forEach(element => {
            const target = parseInt(element.getAttribute('data-target'));
            const duration = parseInt(element.getAttribute('data-duration')) || 2000;
            const increment = target / (duration / 16);
            let current = 0;
            
            const updateCounter = () => {
                if (current < target) {
                    current += increment;
                    if (current > target) current = target;
                    element.textContent = Math.floor(current);
                    requestAnimationFrame(updateCounter);
                }
            };
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        updateCounter();
                        observer.unobserve(entry.target);
                    }
                });
            });
            
            observer.observe(element);
        });
    }

    // 鼠标跟随效果
    function initMouseFollow() {
        const cursor = document.createElement('div');
        cursor.className = 'custom-cursor';
        cursor.style.cssText = `
            position: fixed;
            width: 20px;
            height: 20px;
            background: radial-gradient(circle, rgba(100, 115, 255, 0.3) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            transition: transform 0.1s ease;
            transform: translate(-50%, -50%);
        `;
        
        document.body.appendChild(cursor);
        
        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
        });
        
        // 鼠标悬停效果
        const hoverElements = document.querySelectorAll('.card-hover, .btn-animate, .hover-lift');
        hoverElements.forEach(el => {
            el.addEventListener('mouseenter', () => {
                cursor.style.transform = 'translate(-50%, -50%) scale(1.5)';
            });
            
            el.addEventListener('mouseleave', () => {
                cursor.style.transform = 'translate(-50%, -50%) scale(1)';
            });
        });
    }

    // 加载动画
    function initLoadingAnimation() {
        const loadingElements = document.querySelectorAll('.loading-content');
        
        loadingElements.forEach(element => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                element.style.transition = 'all 0.6s ease';
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, 300);
        });
    }

    // 视差滚动效果
    function initParallax() {
        const parallaxElements = document.querySelectorAll('.parallax');
        
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            
            parallaxElements.forEach(element => {
                const speed = element.getAttribute('data-speed') || 0.5;
                const yPos = -(scrolled * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
        });
    }

    // 平滑滚动
    function initSmoothScroll() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // 页面加载完成后的初始化
    document.addEventListener('DOMContentLoaded', () => {
        initScrollAnimations();
        initNavbarScroll();
        initTypewriterEffect();
        initCounterAnimation();
        initLoadingAnimation();
        initParallax();
        initSmoothScroll();
        
        // 可选：鼠标跟随效果（默认禁用，可根据需要启用）
        // initMouseFollow();
    });

    // 为动态加载的内容添加动画支持
    window.addEventListener('DOMContentLoaded', () => {
        // 延迟加载的内容
        const delayedElements = document.querySelectorAll('.animate-delay-1, .animate-delay-2, .animate-delay-3, .animate-delay-4, .animate-delay-5');
        
        delayedElements.forEach((element, index) => {
            const delay = (index + 1) * 100;
            element.style.animationDelay = `${delay}ms`;
        });
    });

    // 导出全局函数供其他脚本使用
    window.Animations = {
        scrollToElement: (selector) => {
            const element = document.querySelector(selector);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        },
        
        addAnimation: (element, className) => {
            if (element) {
                element.classList.add(className);
            }
        },
        
        removeAnimation: (element, className) => {
            if (element) {
                element.classList.remove(className);
            }
        }
    };
})();