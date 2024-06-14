(function () {
	'use strict';

	/**
	 * Easy selector helper function
	 */
	const select = (el, all = false) => {
		el = el.trim();
		if (all) {
			return [...document.querySelectorAll(el)];
		} else {
			return document.querySelector(el);
		}
	};

	/**
	 * Easy event listener function
	 */
	const on = (type, el, listener, all = false) => {
		let selectEl = select(el, all);
		if (selectEl) {
			if (all) {
				selectEl.forEach((e) => e.addEventListener(type, listener));
			} else {
				selectEl.addEventListener(type, listener);
			}
		}
	};

	/**
	 * Easy on scroll event listener
	 */
	const onscroll = (el, listener) => {
		el.addEventListener('scroll', listener);
	};

	/**
	 * Scrolls to an element with header offset
	 */
	const scrollto = (el) => {
		let header = select('#header');
		let offset = header.offsetHeight;

		let elementPos = select(el).offsetTop;
		window.scrollTo({
			top: elementPos - offset,
			behavior: 'smooth',
		});
	};

	/**
	 * Navbar links active state on page navigation
	 */

	document.addEventListener('DOMContentLoaded', () => {
		const navbarLinks = document.querySelectorAll('#navbar a');
		const currentUrl = window.location.pathname.split('/').pop();

		navbarLinks.forEach((link) => {
			const linkHref = link.href.split('/').pop();
			if (linkHref === currentUrl) {
				link.classList.add('active');
			} else {
				link.classList.remove('active');
			}
		});
	});

	/**
	 * Back to top button
	 */
	let backtotop = select('.back-to-top');
	if (backtotop) {
		const toggleBacktotop = () => {
			if (window.scrollY > 100) {
				backtotop.classList.add('active');
			} else {
				backtotop.classList.remove('active');
			}
		};
		window.addEventListener('load', toggleBacktotop);
		onscroll(document, toggleBacktotop);
	}

	/**
	 * Mobile nav toggle
	 */
	on('click', '.mobile-nav-toggle', function (e) {
		select('#navbar').classList.toggle('navbar-mobile');
		this.classList.toggle('bi-list');
		this.classList.toggle('bi-x');
	});

	/**
	 * Mobile nav dropdowns activate
	 */
	on(
		'click',
		'.navbar .dropdown > a',
		function (e) {
			if (select('#navbar').classList.contains('navbar-mobile')) {
				e.preventDefault();
				this.nextElementSibling.classList.toggle('dropdown-active');
			}
		},
		true,
	);

	/**
	 * Scrool with ofset on links with a class name .scrollto
	 */
	on(
		'click',
		'.scrollto',
		function (e) {
			if (select(this.hash)) {
				e.preventDefault();

				let navbar = select('#navbar');
				if (navbar.classList.contains('navbar-mobile')) {
					navbar.classList.remove('navbar-mobile');
					let navbarToggle = select('.mobile-nav-toggle');
					navbarToggle.classList.toggle('bi-list');
					navbarToggle.classList.toggle('bi-x');
				}
				scrollto(this.hash);
			}
		},
		true,
	);

	/**
	 * Scroll with ofset on page load with hash links in the url
	 */
	window.addEventListener('load', () => {
		if (window.location.hash) {
			if (select(window.location.hash)) {
				scrollto(window.location.hash);
			}
		}
	});

	/**
	 * Preloader
	 */
	let preloader = select('#preloader');
	if (preloader) {
		window.addEventListener('load', () => {
			preloader.remove();
		});
	}

	/**
	 * Hero type effect
	 */
	const typed = select('.typed');
	if (typed) {
		let typed_strings = typed.getAttribute('data-typed-items');
		typed_strings = typed_strings.split(',');
		new Typed('.typed', {
			strings: typed_strings,
			loop: true,
			typeSpeed: 100,
			backSpeed: 50,
			backDelay: 2000,
		});
	}

	/**
	 * Portfolio isotope and filter
	 */
	window.addEventListener('load', () => {
		let portfolioContainer = document.querySelector('.portfolio-container');
		if (portfolioContainer) {
			let portfolioIsotope = new Isotope(portfolioContainer, {
				itemSelector: '.portfolio-item',
			});

			let portfolioFilters = document.querySelectorAll('#portfolio-flters li');

			portfolioFilters.forEach((el) => {
				el.addEventListener('click', function (e) {
					e.preventDefault();
					portfolioFilters.forEach(function (el) {
						el.classList.remove('filter-active');
					});
					this.classList.add('filter-active');

					portfolioIsotope.arrange({
						filter: this.getAttribute('data-filter'),
					});
					portfolioIsotope.on('arrangeComplete', function () {
						AOS.refresh();
					});
				});
			});
		}
	});

	/**
	 * Initiate portfolio lightbox
	 */
	const portfolioLightbox = GLightbox({
		selector: '.portfolio-lightbox',
	});

	/**
	 * Initiate portfolio details lightbox
	 */
	const portfolioDetailsLightbox = GLightbox({
		selector: '.portfolio-details-lightbox',
		width: '90%',
		height: '90vh',
	});

	/**
	 * Portfolio details slider
	 */
	new Swiper('.portfolio-details-slider', {
		speed: 400,
		loop: true,
		autoplay: {
			delay: 5000,
			disableOnInteraction: false,
		},
		pagination: {
			el: '.swiper-pagination',
			type: 'bullets',
			clickable: true,
		},
	});

	/**
	 * Skills animation
	 */
	let skilsContent = select('.skills-content');
	if (skilsContent) {
		new Waypoint({
			element: skilsContent,
			offset: '80%',
			handler: function (direction) {
				let progress = select('.progress .progress-bar', true);
				progress.forEach((el) => {
					el.style.width = el.getAttribute('aria-valuenow') + '%';
				});
			},
		});
	}

	/**
	 * Testimonials slider
	 */
	new Swiper('.testimonials-slider', {
		speed: 600,
		loop: true,
		autoplay: {
			delay: 5000,
			disableOnInteraction: false,
		},
		slidesPerView: 'auto',
		pagination: {
			el: '.swiper-pagination',
			type: 'bullets',
			clickable: true,
		},
	});

	/**
	 * Animation on scroll
	 */
	window.addEventListener('load', () => {
		AOS.init({
			duration: 1000,
			easing: 'ease-in-out',
			once: true,
			mirror: false,
		});
	});

	/**
	 * Flash Messages
	 */

	document.addEventListener('DOMContentLoaded', function () {
		let toastElements = document.querySelectorAll('.toast');
		toastElements.forEach(function (toastElement) {
			let toast = new bootstrap.Toast(toastElement, { delay: 5000 });
			toast.show();
		});
	});

	/**
	 * Auto Expand Textarea
	 */

	document.addEventListener('DOMContentLoaded', function () {
		const textareas = document.querySelectorAll('.auto-expand');

		textareas.forEach((textarea) => {
			textarea.style.height = 'auto';
			textarea.style.height = textarea.scrollHeight + 'px';

			textarea.addEventListener('input', function () {
				this.style.height = 'auto';
				this.style.height = this.scrollHeight + 'px';
			});
		});
	});

	/**
	 * Initiate Pure Counter
	 */
	new PureCounter();
})();
