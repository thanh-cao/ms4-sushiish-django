// Horizontally scroll category nav contents on arrow click is adapted from: 
// https://benfrain.com/a-horizontal-scrolling-navigation-pattern-for-touch-and-mouse-with-moving-current-indicator/

const SETTINGS = {
	navBarTravelling: false,
	navBarTravelDirection: "",
	navBarTravelDistance: 150
}

const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const categoryNav = document.getElementById("categoryNav");
const categoryNavContents = document.getElementById("categoryNavContents");

categoryNav.setAttribute("data-overflowing", determineOverflow(categoryNavContents, categoryNav));


// Handle the scroll of the horizontal container
let last_known_scroll_position = 0;
let ticking = false;

// set category navbar to sticky after scrolling passed the bottom of hero section
document.addEventListener('DOMContentLoaded', function () {
	window.addEventListener("scroll", function () {
		const productHeroSection = document.querySelector('section.product-listing-hero');
		const productHeroSectionBottom = productHeroSection.offsetHeight + productHeroSection.offsetTop;
		const categoryNavWrapper = document.querySelector('.category-nav-wrapper');
		const scrollPosition = window.scrollY;

		if (scrollPosition > productHeroSectionBottom) {
			categoryNavWrapper.classList.add('category-nav-fixed');
		} else {
			categoryNavWrapper.classList.remove('category-nav-fixed');
		}
	});
});


function doSomething(scroll_pos) {
	categoryNav.setAttribute("data-overflowing", determineOverflow(categoryNavContents, categoryNav));
}

categoryNav.addEventListener("scroll", function () {
	last_known_scroll_position = window.scrollY;
	if (!ticking) {
		window.requestAnimationFrame(function () {
			doSomething(last_known_scroll_position);
			ticking = false;
		});
	}
	ticking = true;
});

prevBtn.addEventListener("click", function () {
	// If in the middle of a move return
	if (SETTINGS.navBarTravelling === true) {
		return;
	}
	// If we have content overflowing both sides or on the left
	if (determineOverflow(categoryNavContents, categoryNav) === "left" || determineOverflow(categoryNavContents, categoryNav) === "both") {
		// Find how far this panel has been scrolled
		let availableScrollLeft = categoryNav.scrollLeft;
		// If the space available is less than two lots of our desired distance, just move the whole amount
		// otherwise, move by the amount in the settings
		if (availableScrollLeft < SETTINGS.navBarTravelDistance * 2) {
			categoryNavContents.style.transform = "translateX(" + availableScrollLeft + "px)";
		} else {
			categoryNavContents.style.transform = "translateX(" + SETTINGS.navBarTravelDistance + "px)";
		}
		// We do want a transition (this is set in CSS) when moving so remove the class that would prevent that
		categoryNavContents.classList.remove("category-nav_contents-no-transition");
		// Update our settings
		SETTINGS.navBarTravelDirection = "left";
		SETTINGS.navBarTravelling = true;
	}
	// Now update the attribute in the DOM
	categoryNav.setAttribute("data-overflowing", determineOverflow(categoryNavContents, categoryNav));
});

nextBtn.addEventListener("click", function () {
	// If in the middle of a move return
	if (SETTINGS.navBarTravelling === true) {
		return;
	}
	// If we have content overflowing both sides or on the right
	if (determineOverflow(categoryNavContents, categoryNav) === "right" || determineOverflow(categoryNavContents, categoryNav) === "both") {
		// Get the right edge of the container and content
		let navBarRightEdge = categoryNavContents.getBoundingClientRect().right;
		let navBarScrollerRightEdge = categoryNav.getBoundingClientRect().right;
		// Now we know how much space we have available to scroll
		let availableScrollRight = Math.floor(navBarRightEdge - navBarScrollerRightEdge);
		// If the space available is less than two lots of our desired distance, just move the whole amount
		// otherwise, move by the amount in the settings
		if (availableScrollRight < SETTINGS.navBarTravelDistance * 2) {
			categoryNavContents.style.transform = "translateX(-" + availableScrollRight + "px)";
		} else {
			categoryNavContents.style.transform = "translateX(-" + SETTINGS.navBarTravelDistance + "px)";
		}
		// We do want a transition (this is set in CSS) when moving so remove the class that would prevent that
		categoryNavContents.classList.remove("category-nav_contents-no-transition");
		// Update our settings
		SETTINGS.navBarTravelDirection = "right";
		SETTINGS.navBarTravelling = true;
	}
	// Now update the attribute in the DOM
	categoryNav.setAttribute("data-overflowing", determineOverflow(categoryNavContents, categoryNav));
});

categoryNavContents.addEventListener(
	"transitionend",
	function () {
		// get the value of the transform, apply that to the current scroll position (so get the scroll pos first) and then remove the transform
		let styleOfTransform = window.getComputedStyle(categoryNavContents, null);
		let tr = styleOfTransform.getPropertyValue("-webkit-transform") || styleOfTransform.getPropertyValue("transform");
		// If there is no transition we want to default to 0 and not null
		let amount = Math.abs(parseInt(tr.split(",")[4]) || 0);
		categoryNavContents.style.transform = "none";
		categoryNavContents.classList.add("category-nav_contents-no-transition");
		// Now lets set the scroll position
		if (SETTINGS.navBarTravelDirection === "left") {
			categoryNav.scrollLeft = categoryNav.scrollLeft - amount;
		} else {
			categoryNav.scrollLeft = categoryNav.scrollLeft + amount;
		}
		SETTINGS.navBarTravelling = false;
	},
	false
);

// Handle setting the currently active link
categoryNavContents.addEventListener("click", function (e) {
	let links = [].slice.call(document.querySelectorAll(".category-nav .nav-link"));
	links.forEach(function (item) {
		item.classList.remove("active");
	})
	e.target.classList.add("active");
});

function determineOverflow(content, container) {
	let containerMetrics = container.getBoundingClientRect();
	let containerMetricsRight = Math.floor(containerMetrics.right);
	let containerMetricsLeft = Math.floor(containerMetrics.left);
	let contentMetrics = content.getBoundingClientRect();
	let contentMetricsRight = Math.floor(contentMetrics.right);
	let contentMetricsLeft = Math.floor(contentMetrics.left);
	if (containerMetricsLeft > contentMetricsLeft && containerMetricsRight < contentMetricsRight) {
		prevBtn.style.display = "block";
		nextBtn.style.display = "block";
		return "both";
	} else if (contentMetricsLeft < containerMetricsLeft) {
		prevBtn.style.display = "block";
		nextBtn.style.display = "none";
		return "left";
	} else if (contentMetricsRight > containerMetricsRight) {
		prevBtn.style.display = "none";
		nextBtn.style.display = "block";
		return "right";
	} else {
		return "none";
	}
}
