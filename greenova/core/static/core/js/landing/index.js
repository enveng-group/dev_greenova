import { fetchLandingPageContent, submitNewsletterSignup } from "./proto";
import { showNotification } from "../shared/dom";
document.addEventListener("DOMContentLoaded", async () => {
    // Load and render landing page content
    try {
        const content = await fetchLandingPageContent();
        const heroTitle = document.getElementById("hero-heading");
        if (heroTitle && content.hero_title) {
            heroTitle.textContent = content.hero_title;
        }
        // TODO: Render features, stats, benefits, testimonials, CTA, etc. from content
    }
    catch (err) {
        console.error("Failed to load landing page content:", err);
        showNotification("Failed to load landing page content", "error");
    }
    // Newsletter signup form handler
    const form = document.querySelector('form[action$="newsletter_signup"]');
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const emailInput = form.querySelector("input[type='email']");
            if (!emailInput)
                return;
            const email = emailInput.value.trim();
            try {
                const resp = await submitNewsletterSignup(email);
                if (resp.success) {
                    showNotification(resp.message, "success");
                    form.reset();
                }
                else {
                    showNotification(resp.message, "error");
                }
            }
            catch (err) {
                showNotification("Failed to sign up for newsletter.", "error");
            }
        });
    }
});
