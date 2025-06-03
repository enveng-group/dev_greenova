/**
 * Copyright 2025 Enveng Group.
 * SPDX-License-Identifier: AGPL-3.0-or-later
 *
 * Landing Page Animations and Interactions
 * This script enhances the landing page with GSAP animations and interactive features
 * while maintaining accessibility.
 */

// Wait for DOM to be fully loaded
document.addEventListener("DOMContentLoaded", () => {
	// Register GSAP plugins
	gsap.registerPlugin(
		Flip,
		MotionPathPlugin,
		MorphSVGPlugin,
		Physics2DPlugin,
		ScrambleTextPlugin,
		ScrollTrigger,
		ScrollSmoother,
		SplitText,
		CustomEase,
	);

	// Check if user prefers reduced motion
	const prefersReducedMotion = window.matchMedia(
		"(prefers-reduced-motion: reduce)",
	).matches;

	if (!prefersReducedMotion) {
		// Initialize GSAP animations
		initGsapAnimations();
	} else {
		// Apply simple visible class for users who prefer reduced motion
		document.querySelectorAll(".fade-in, .slide-up").forEach((el) => {
			el.classList.add("visible");
		});
	}

	// Initialize scroll animations for non-GSAP elements
	initScrollAnimations();

	// Initialize testimonial slider if it exists
	const testimonialContainer = document.querySelector(
		".testimonials-container",
	);
	if (testimonialContainer) {
		initTestimonialSlider();
	}

	// Add interaction to feature cards
	initFeatureCards();
});

/**
 * Initialize GSAP animations
 * Sets up scroll-triggered animations and hero section effects
 */
function initGsapAnimations() {
	// Create a smooth scroller
	if (ScrollSmoother) {
		const smoother = ScrollSmoother.create({
			smooth: 1.5, // Smooth time (seconds)
			effects: true, // Look for data-speed and data-lag attributes on elements
			normalizeScroll: true,
			ignoreMobileResize: true,
		});
	}

	// Hero section animations
	const heroTl = gsap.timeline();

	// Custom entrance animation for hero section
	heroTl
		.from(".hero-logo", {
			y: -50,
			opacity: 0,
			duration: 1.2,
			ease: "power3.out",
		})
		.from(
			".hero-brand-title",
			{
				opacity: 0,
				y: 20,
				duration: 0.8,
				ease: "back.out(1.7)",
			},
			"-=0.5",
		)
		.from(
			".hero-title",
			{
				opacity: 0,
				y: 30,
				duration: 1,
				ease: "power2.out",
			},
			"-=0.3",
		)
		.from(
			".hero-subtitle",
			{
				opacity: 0,
				y: 20,
				duration: 0.8,
				ease: "power2.out",
			},
			"-=0.7",
		)
		.from(
			".hero-cta .btn-primary, .hero-cta .btn-secondary",
			{
				opacity: 0,
				y: 20,
				stagger: 0.2,
				duration: 0.6,
				ease: "power1.out",
			},
			"-=0.5",
		)
		.from(
			".scroll-indicator",
			{
				opacity: 0,
				y: -10,
				duration: 0.6,
				ease: "power1.out",
				repeat: -1,
				yoyo: true,
			},
			"-=0.2",
		);

	// Create scroll-triggered animations for sections
	gsap.utils
		.toArray(
			".features-section, .stats-section, .benefits-section, .testimonials-section, .cta-section",
		)
		.forEach((section, i) => {
			// Create timeline for each section
			const tl = gsap.timeline({
				scrollTrigger: {
					trigger: section,
					start: "top 80%",
					end: "bottom 20%",
					toggleActions: "play none none none",
				},
			});

			// Animate section title
			tl.from(section.querySelector(".section-title"), {
				opacity: 0,
				y: 50,
				duration: 0.8,
				ease: "power2.out",
			});

			// Animate content based on section type
			if (section.classList.contains("features-section")) {
				// Features section animations
				tl.from(
					section.querySelectorAll(".feature-card"),
					{
						opacity: 0,
						y: 50,
						stagger: 0.2,
						duration: 0.8,
						ease: "back.out(1.4)",
					},
					"-=0.4",
				);
			} else if (section.classList.contains("stats-section")) {
				// Stats section animations
				tl.from(
					section.querySelectorAll(".stat-item"),
					{
						opacity: 0,
						scale: 0.8,
						stagger: 0.15,
						duration: 0.7,
						ease: "back.out(1.7)",
					},
					"-=0.4",
				).from(
					section.querySelectorAll(".stat-value"),
					{
						textContent: 0,
						duration: 2,
						snap: { textContent: 1 },
						stagger: 0.15,
						ease: "power2.out",
					},
					"-=0.8",
				);
			} else if (section.classList.contains("benefits-section")) {
				// Benefits section animations
				tl.from(
					section.querySelectorAll(".benefit-item"),
					{
						opacity: 0,
						x: i % 2 === 0 ? -50 : 50,
						stagger: 0.2,
						duration: 0.8,
						ease: "power2.out",
					},
					"-=0.4",
				);
			} else if (section.classList.contains("testimonials-section")) {
				// Testimonials section animations
				tl.from(
					section.querySelector(".testimonials-container"),
					{
						opacity: 0,
						y: 30,
						duration: 0.8,
						ease: "power2.out",
					},
					"-=0.4",
				);
			} else if (section.classList.contains("cta-section")) {
				// CTA section animations
				tl.from(
					section.querySelector(".cta-title"),
					{
						opacity: 0,
						y: 30,
						duration: 0.8,
						ease: "power2.out",
					},
					"-=0.4",
				)
					.from(
						section.querySelector(".cta-description"),
						{
							opacity: 0,
							y: 20,
							duration: 0.6,
							ease: "power2.out",
						},
						"-=0.5",
					)
					.from(
						section.querySelector(".cta-btn"),
						{
							opacity: 0,
							y: 20,
							scale: 0.9,
							duration: 0.6,
							ease: "back.out(1.7)",
						},
						"-=0.3",
					)
					.from(
						section.querySelector(".newsletter-form"),
						{
							opacity: 0,
							y: 20,
							duration: 0.6,
							ease: "power2.out",
						},
						"-=0.2",
					);
			}
		});

	// Add parallax effects
	initParallax();
}

/**
 * Initialize scroll animations for elements with .fade-in class
 * Uses Intersection Observer API for better performance than scroll events
 * This handles elements not covered by GSAP animations
 */
function initScrollAnimations() {
	// Check if user prefers reduced motion
	const prefersReducedMotion = window.matchMedia(
		"(prefers-reduced-motion: reduce)",
	).matches;

	// Skip animations if reduced motion is preferred
	if (prefersReducedMotion) {
		document.querySelectorAll(".fade-in").forEach((el) => {
			el.classList.add("visible");
		});
		return;
	}

	// Set up the Intersection Observer
	if ("IntersectionObserver" in window) {
		const fadeElements = document.querySelectorAll(".fade-in");

		const appearOptions = {
			threshold: 0.15,
			rootMargin: "0px 0px -100px 0px",
		};

		const appearOnScroll = new IntersectionObserver((entries, observer) => {
			entries.forEach((entry) => {
				if (!entry.isIntersecting) return;
				entry.target.classList.add("visible");
				observer.unobserve(entry.target);
			});
		}, appearOptions);

		fadeElements.forEach((element) => {
			appearOnScroll.observe(element);
		});
	} else {
		// Fallback for browsers that don't support Intersection Observer
		document.querySelectorAll(".fade-in").forEach((el) => {
			el.classList.add("visible");
		});
	}
}

/**
 * Create a simple testimonial slider with navigation
 */
function initTestimonialSlider() {
	const container = document.querySelector(".testimonials-container");
	const items = container.querySelectorAll(".testimonial-item");

	// Only setup if we have more than 1 item
	if (items.length <= 1) return;

	// Create slider navigation
	const nav = document.createElement("div");
	nav.className = "testimonial-nav";
	nav.setAttribute("role", "tablist");
	nav.setAttribute("aria-label", "Testimonial Navigation");

	// Add slider controls
	const prevBtn = document.createElement("button");
	prevBtn.className = "testimonial-prev";
	prevBtn.innerHTML = "←";
	prevBtn.setAttribute("aria-label", "Previous testimonial");

	const nextBtn = document.createElement("button");
	nextBtn.className = "testimonial-next";
	nextBtn.innerHTML = "→";
	nextBtn.setAttribute("aria-label", "Next testimonial");

	// Create dots for navigation
	const dots = document.createElement("div");
	dots.className = "testimonial-dots";

	items.forEach((_, index) => {
		const dot = document.createElement("button");
		dot.className = "testimonial-dot";
		dot.setAttribute("aria-label", `Go to testimonial ${index + 1}`);
		dot.setAttribute("role", "tab");
		dot.setAttribute("aria-selected", index === 0 ? "true" : "false");
		dot.dataset.index = index;

		dot.addEventListener("click", () => goToSlide(index));
		dots.appendChild(dot);
	});

	nav.appendChild(prevBtn);
	nav.appendChild(dots);
	nav.appendChild(nextBtn);
	container.appendChild(nav);

	// Set initial state
	let currentIndex = 0;

	// Create a GSAP timeline for testimonial transitions
	const testimonialTimeline = gsap.timeline();
	updateSlider();

	// Add event listeners to buttons
	prevBtn.addEventListener("click", () => {
		currentIndex = (currentIndex - 1 + items.length) % items.length;
		updateSlider();
	});

	nextBtn.addEventListener("click", () => {
		currentIndex = (currentIndex + 1) % items.length;
		updateSlider();
	});

	// Set up auto rotation with pause on hover/focus
	let slideInterval = setInterval(() => {
		currentIndex = (currentIndex + 1) % items.length;
		updateSlider();
	}, 6000);

	container.addEventListener("mouseenter", () => {
		clearInterval(slideInterval);
	});

	container.addEventListener("mouseleave", () => {
		slideInterval = setInterval(() => {
			currentIndex = (currentIndex + 1) % items.length;
			updateSlider();
		}, 6000);
	});

	container.addEventListener("focusin", () => {
		clearInterval(slideInterval);
	});

	container.addEventListener("focusout", (e) => {
		if (!container.contains(e.relatedTarget)) {
			slideInterval = setInterval(() => {
				currentIndex = (currentIndex + 1) % items.length;
				updateSlider();
			}, 6000);
		}
	});

	// Function to go to a specific slide
	function goToSlide(index) {
		currentIndex = index;
		updateSlider();
	}

	// Update the slider display using GSAP animations
	function updateSlider() {
		testimonialTimeline.clear();

		items.forEach((item, index) => {
			if (index === currentIndex) {
				// Active testimonial animation
				testimonialTimeline.to(
					item,
					{
						opacity: 1,
						transform: "translateX(0)",
						duration: 0.6,
						ease: "power2.out",
						onStart: () => {
							item.classList.add("active");
							item.setAttribute("aria-hidden", "false");
						},
					},
					0,
				);
			} else {
				// Hide inactive testimonials
				testimonialTimeline.to(
					item,
					{
						opacity: 0,
						transform:
							index < currentIndex ? "translateX(-100px)" : "translateX(100px)",
						duration: 0.6,
						ease: "power2.in",
						onComplete: () => {
							item.classList.remove("active");
							item.setAttribute("aria-hidden", "true");
						},
					},
					0,
				);
			}
		});

		// Update dots
		dots.querySelectorAll(".testimonial-dot").forEach((dot, index) => {
			if (index === currentIndex) {
				dot.classList.add("active");
				dot.setAttribute("aria-selected", "true");

				// Animate the active dot with GSAP
				gsap.to(dot, {
					scale: 1.2,
					backgroundColor: "var(--greenova-green-primary)",
					duration: 0.3,
					ease: "power1.out",
				});
			} else {
				dot.classList.remove("active");
				dot.setAttribute("aria-selected", "false");

				// Reset inactive dots
				gsap.to(dot, {
					scale: 1,
					backgroundColor: "var(--greenova-text-tertiary-dark)",
					duration: 0.3,
					ease: "power1.out",
				});
			}
		});
	}
}

/**
 * Add interaction effects to feature cards
 */
function initFeatureCards() {
	const cards = document.querySelectorAll(".feature-card");

	cards.forEach((card) => {
		// Make the entire card clickable if it contains a link
		const link = card.querySelector("a");
		if (link) {
			card.addEventListener("click", (e) => {
				// Don't trigger if the click was on the link itself
				if (e.target.tagName !== "A" && !e.target.closest("a")) {
					link.click();
				}
			});

			// Keyboard accessibility - make card focused state visible
			card.setAttribute("tabindex", "0");
			card.addEventListener("keydown", (e) => {
				// Trigger link click on Enter or Space
				if (e.key === "Enter" || e.key === " ") {
					e.preventDefault();
					link.click();
				}
			});
		}

		// Add hover effects with GSAP
		card.addEventListener("mouseenter", () => {
			gsap.to(card, {
				y: -5,
				boxShadow: "0 12px 30px rgba(0, 0, 0, 0.15)",
				duration: 0.3,
				ease: "power2.out",
			});

			// Animate the card header line
			gsap.to(card.querySelector(".feature-icon"), {
				scale: 1.1,
				duration: 0.4,
				ease: "back.out(1.7)",
			});

			// Animate the link arrow
			const featureLink = card.querySelector(".feature-link");
			if (featureLink) {
				gsap.to(featureLink.querySelector("::after"), {
					x: 4,
					duration: 0.3,
					ease: "power1.out",
				});
			}
		});

		card.addEventListener("mouseleave", () => {
			gsap.to(card, {
				y: 0,
				boxShadow: "0 8px 24px rgba(0, 0, 0, 0.07)",
				duration: 0.3,
				ease: "power2.out",
			});

			// Reset the card header line
			gsap.to(card.querySelector(".feature-icon"), {
				scale: 1,
				duration: 0.4,
				ease: "power2.out",
			});

			// Reset the link arrow
			const featureLink = card.querySelector(".feature-link");
			if (featureLink) {
				gsap.to(featureLink.querySelector("::after"), {
					x: 0,
					duration: 0.3,
					ease: "power1.out",
				});
			}
		});
	});
}

/**
 * Add parallax effect to hero section and other elements
 * This creates a subtle movement as the user scrolls
 */
function initParallax() {
	const heroSection = document.querySelector(".hero-section");

	if (heroSection) {
		// Setup ScrollTrigger for parallax effects
		gsap.to(".hero-decoration-1", {
			scrollTrigger: {
				trigger: heroSection,
				start: "top top",
				end: "bottom top",
				scrub: true,
			},
			y: 100,
			ease: "none",
		});

		gsap.to(".hero-decoration-2", {
			scrollTrigger: {
				trigger: heroSection,
				start: "top top",
				end: "bottom top",
				scrub: true,
			},
			y: -80,
			ease: "none",
		});

		// Parallax for hero content
		gsap.to(".hero-content", {
			scrollTrigger: {
				trigger: heroSection,
				start: "top top",
				end: "bottom top",
				scrub: true,
			},
			y: 50,
			ease: "none",
		});
	}

	// Parallax effect for other sections
	gsap.utils.toArray(".feature-card").forEach((card) => {
		gsap.to(card, {
			scrollTrigger: {
				trigger: card,
				start: "top bottom",
				end: "bottom top",
				scrub: true,
			},
			y: 20,
			ease: "none",
		});
	});

	// Stats counter animation
	const statValues = document.querySelectorAll(".stat-value");
	statValues.forEach((stat) => {
		const value = stat.textContent.trim();
		let endValue;

		// Determine if the stat is a percentage, number with plus, or plain number
		if (value.includes("%")) {
			endValue = parseFloat(value);
			ScrollTrigger.create({
				trigger: stat,
				start: "top 80%",
				onEnter: () => {
					gsap.from(stat, {
						textContent: 0,
						duration: 2,
						ease: "power2.out",
						snap: { textContent: 1 },
						stagger: {
							each: 0.2,
							onUpdate: function () {
								stat.textContent =
									Math.round(this.targets()[0].textContent) + "%";
							},
						},
					});
				},
			});
		} else if (value.includes("+")) {
			endValue = parseFloat(value);
			ScrollTrigger.create({
				trigger: stat,
				start: "top 80%",
				onEnter: () => {
					gsap.from(stat, {
						textContent: 0,
						duration: 2,
						ease: "power2.out",
						snap: { textContent: 1 },
						stagger: {
							each: 0.2,
							onUpdate: function () {
								stat.textContent =
									Math.round(this.targets()[0].textContent) + "+";
							},
						},
					});
				},
			});
		}
	});
}

// Initialize ScrollTrigger animations once the page is fully loaded
window.addEventListener("load", () => {
	// Preloading images for smoother animations
	const imageLinks = Array.from(document.images);
	const imagePromises = imageLinks.map((image) => {
		return new Promise((resolve, reject) => {
			const img = new Image();
			img.src = image.src;
			img.onload = resolve;
			img.onerror = reject;
		});
	});

	// Once all images are loaded, refresh ScrollTrigger
	Promise.all(imagePromises).then(() => {
		if (typeof ScrollTrigger !== "undefined") {
			ScrollTrigger.refresh();
		}
	});
});
