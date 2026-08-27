/* ==========================================================================
   Executive Procurement Dashboard Script
   Interactive TCO Calculator, Hardware Matrix Filtering, & Lightbox Modal
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initCalculator();
    initMatrixFilters();
    initLightboxKeyboard();
});

/* --------------------------------------------------------------------------
   1. Interactive TCO & Lifespan Calculator
   -------------------------------------------------------------------------- */
function initCalculator() {
    const hoursSlider = document.getElementById('hours-slider');
    const priceSlider = document.getElementById('price-slider');
    const tvPriceSlider = document.getElementById('tv-price-slider');

    const hoursVal = document.getElementById('hours-val');
    const priceVal = document.getElementById('price-val');
    const tvPriceVal = document.getElementById('tv-price-val');

    const resYears = document.getElementById('res-years');
    const resDaily = document.getElementById('res-daily');
    const resDays = document.getElementById('res-days');
    const resSavings = document.getElementById('res-savings');
    const pctSavings = document.getElementById('pct-savings');

    const barProjector = document.getElementById('bar-projector');
    const barSavings = document.getElementById('bar-savings');

    const TOTAL_LASER_HOURS = 20000;

    function recalculate() {
        const hoursPerDay = parseInt(hoursSlider.value, 10);
        const projectorPrice = parseFloat(priceSlider.value);
        const tvPrice = parseFloat(tvPriceSlider.value);

        // Update Labels
        hoursVal.textContent = `${hoursPerDay} Hours / Day`;
        priceVal.textContent = `$${projectorPrice.toLocaleString()} USD`;
        tvPriceVal.textContent = `$${tvPrice.toLocaleString()} USD`;

        // Calculations
        const totalDays = TOTAL_LASER_HOURS / hoursPerDay;
        const totalYears = totalDays / 365.25;
        const dailyCost = projectorPrice / totalDays;
        const netSavings = Math.max(0, tvPrice - projectorPrice);
        const savingsPercentage = Math.round((netSavings / tvPrice) * 100);

        // Display Outputs
        resYears.textContent = `${totalYears.toFixed(2)} Years`;
        resDaily.textContent = `$${dailyCost.toFixed(2)} / day`;
        resDays.textContent = `${Math.round(totalDays).toLocaleString()} Days`;
        resSavings.textContent = `$${netSavings.toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
        pctSavings.textContent = `${savingsPercentage}% Cost Reduction`;

        // Chart Bar Percentages
        const projPct = Math.min(100, Math.max(15, Math.round((projectorPrice / tvPrice) * 100)));
        const savPct = 100 - projPct;

        barProjector.style.width = `${projPct}%`;
        barProjector.textContent = `Projector ($${Math.round(projectorPrice)})`;

        barSavings.style.width = `${savPct}%`;
        barSavings.textContent = `Savings ($${Math.round(netSavings)})`;
    }

    hoursSlider.addEventListener('input', recalculate);
    priceSlider.addEventListener('input', recalculate);
    tvPriceSlider.addEventListener('input', recalculate);

    recalculate();
}

/* --------------------------------------------------------------------------
   2. Hardware Matrix Filter Tabs
   -------------------------------------------------------------------------- */
function initMatrixFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const matrixCards = document.querySelectorAll('.matrix-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.getAttribute('data-filter');

            matrixCards.forEach(card => {
                if (filter === 'all') {
                    card.style.display = 'flex';
                } else {
                    const category = card.getAttribute('data-category');
                    if (category === filter) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                }
            });
        });
    });
}

/* --------------------------------------------------------------------------
   3. Lightbox Gallery Modal
   -------------------------------------------------------------------------- */
function openLightbox(imgSrc, title, desc) {
    const modal = document.getElementById('lightbox-modal');
    const modalImg = document.getElementById('lightbox-img');
    const modalTitle = document.getElementById('lightbox-title');
    const modalDesc = document.getElementById('lightbox-desc');

    modalImg.src = imgSrc;
    modalTitle.textContent = title;
    modalDesc.textContent = desc;

    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    const modal = document.getElementById('lightbox-modal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

function initLightboxKeyboard() {
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeLightbox();
        }
    });
}

/* Smooth Scrolling Helper */
function scrollToSection(sectionId) {
    const el = document.getElementById(sectionId);
    if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
    }
}
