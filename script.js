/**
 * KCMS (Kate Collins Middle School) - Official V3 Menu Calendar Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  // App State
  let menuData = null;
  let currentYear = 2026;
  let currentMonth = 8; // August 2026 default
  let selectedSchool = 'middle'; // KCMS Middle default
  let selectedMealFilter = 'all';
  let searchQuery = '';

  // DOM Elements
  const calendarGrid = document.getElementById('calendarGrid');
  const currentMonthLabel = document.getElementById('currentMonthLabel');
  const schoolSelector = document.getElementById('schoolSelector');
  const mealFilter = document.getElementById('mealFilter');
  const searchInput = document.getElementById('searchInput');
  const clearSearch = document.getElementById('clearSearch');
  const pdfGrid = document.getElementById('pdfGrid');
  
  // Navigation Buttons
  const btnPrevMonth = document.getElementById('btnPrevMonth');
  const btnNextMonth = document.getElementById('btnNextMonth');
  const btnToday = document.getElementById('btnToday');

  // Modal Elements
  const dayModal = document.getElementById('dayModal');
  const modalClose = document.getElementById('modalClose');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalDate = document.getElementById('modalDate');
  const modalSchoolName = document.getElementById('modalSchoolName');
  const modalBody = document.getElementById('modalBody');

  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

  // Fetch Menu JSON Dataset
  fetch('data/menus.json')
    .then(response => {
      if (!response.ok) throw new Error('Failed to load menu dataset');
      return response.json();
    })
    .then(data => {
      menuData = data;
      initApp();
    })
    .catch(error => {
      console.error('Error initializing menu data:', error);
      calendarGrid.innerHTML = `
        <div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: #F43F5E;">
          <i class="fa-solid fa-triangle-exclamation" style="font-size: 2rem; margin-bottom: 12px;"></i>
          <p style="font-weight: 600;">Unable to load KCMS menu data.</p>
        </div>
      `;
    });

  function initApp() {
    setupEventListeners();
    renderCalendar();
    renderPdfDownloads();
  }

  function setupEventListeners() {
    // School Switcher Tabs
    schoolSelector.addEventListener('click', (e) => {
      const tab = e.target.closest('.school-tab');
      if (!tab) return;
      
      document.querySelectorAll('.school-tab').forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');
      selectedSchool = tab.dataset.school;
      renderCalendar();
    });

    // Meal Filter
    mealFilter.addEventListener('click', (e) => {
      const btn = e.target.closest('.segment-btn');
      if (!btn) return;

      document.querySelectorAll('#mealFilter .segment-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedMealFilter = btn.dataset.meal;
      renderCalendar();
    });

    // Month Navigation
    btnPrevMonth.addEventListener('click', () => {
      currentMonth--;
      if (currentMonth < 1) {
        currentMonth = 12;
        currentYear--;
      }
      renderCalendar();
    });

    btnNextMonth.addEventListener('click', () => {
      currentMonth++;
      if (currentMonth > 12) {
        currentMonth = 1;
        currentYear++;
      }
      renderCalendar();
    });

    btnToday.addEventListener('click', () => {
      currentYear = 2026;
      currentMonth = 8;
      renderCalendar();
    });

    // Search Input
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.toLowerCase().trim();
      clearSearch.classList.toggle('hidden', searchQuery === '');
      renderCalendar();
    });

    clearSearch.addEventListener('click', () => {
      searchInput.value = '';
      searchQuery = '';
      clearSearch.classList.add('hidden');
      renderCalendar();
    });

    // Modal Close
    modalClose.addEventListener('click', closeModal);
    modalCloseBtn.addEventListener('click', closeModal);
    dayModal.addEventListener('click', (e) => {
      if (e.target === dayModal) closeModal();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !dayModal.classList.contains('hidden')) {
        closeModal();
      }
    });
  }

  function renderCalendar() {
    currentMonthLabel.textContent = `${monthNames[currentMonth - 1]} ${currentYear}`;
    calendarGrid.innerHTML = '';

    const totalDaysInMonth = new Date(currentYear, currentMonth, 0).getDate();

    // Collect all weekday dates (Monday - Friday) for current month
    let schoolDays = [];
    for (let day = 1; day <= totalDaysInMonth; day++) {
      const dt = new Date(currentYear, currentMonth - 1, day);
      const weekday = dt.getDay(); // 0 = Sun, 1 = Mon, ..., 5 = Fri, 6 = Sat
      if (weekday >= 1 && weekday <= 5) {
        schoolDays.push({ day, dt, weekday: weekday - 1 }); // 0 = Mon, 4 = Fri
      }
    }

    if (schoolDays.length === 0) return;

    // Calculate padding offset for first week (0 = Monday, 4 = Friday)
    const firstWeekday = schoolDays[0].weekday;
    for (let i = 0; i < firstWeekday; i++) {
      const cell = document.createElement('div');
      cell.className = 'calendar-day other-month';
      cell.innerHTML = `<div class="day-header"><span class="day-number">--</span></div>`;
      calendarGrid.appendChild(cell);
    }

    // Render 5-Day School Calendar Cells
    schoolDays.forEach(({ day, dt }) => {
      const monthStr = currentMonth.toString().padStart(2, '0');
      const dayStr = day.toString().padStart(2, '0');
      const dateKey = `${currentYear}-${monthStr}-${dayStr}`;

      const isToday = currentYear === 2026 && currentMonth === 8 && day === 27;
      const dayData = menuData && menuData.calendar ? menuData.calendar[dateKey] : null;

      const cell = document.createElement('div');
      cell.className = `calendar-day ${isToday ? 'is-today' : ''}`;

      let cellHtml = `
        <div class="day-header">
          <span class="day-number">${day}</span>
          <span class="day-status"><i class="fa-solid fa-graduation-cap"></i> School Day</span>
        </div>
      `;

      if (dayData && dayData.is_school_day) {
        let bfast = dayData.kcms_breakfast;
        let lunch = dayData.kcms_lunch;

        if (selectedSchool === 'elementary') lunch = dayData.elementary_lunch || lunch;
        if (selectedSchool === 'high') lunch = dayData.high_school_lunch || lunch;

        let matchesSearch = true;
        if (searchQuery) {
          const bText = (bfast?.main + ' ' + (bfast?.sides || []).join(' ')).toLowerCase();
          const lText = (lunch?.main + ' ' + (lunch?.sides || []).join(' ')).toLowerCase();
          matchesSearch = bText.includes(searchQuery) || lText.includes(searchQuery);
        }

        if (!matchesSearch) {
          cell.style.opacity = '0.2';
        }

        cellHtml += `<div class="meal-preview-container">`;

        // Meal Image Preview for Lunch
        if ((selectedMealFilter === 'all' || selectedMealFilter === 'lunch') && lunch && lunch.image) {
          cellHtml += `
            <img src="${lunch.image}" alt="${lunch.main}" class="meal-img-preview" loading="lazy" />
          `;
        }

        // Breakfast block preview
        if ((selectedMealFilter === 'all' || selectedMealFilter === 'breakfast') && bfast) {
          cellHtml += `
            <div class="meal-block breakfast-block">
              <div class="meal-label"><i class="fa-solid fa-sun"></i> BFAST</div>
              <div class="meal-main-title">${bfast.main}</div>
            </div>
          `;
        }

        // Lunch block preview
        if ((selectedMealFilter === 'all' || selectedMealFilter === 'lunch') && lunch) {
          cellHtml += `
            <div class="meal-block">
              <div class="meal-label"><i class="fa-solid fa-utensils"></i> LUNCH</div>
              <div class="meal-main-title">${lunch.main}</div>
              <div class="tags-row">
                ${(lunch.tags || []).slice(0, 2).map(t => `<span class="badge badge-tag">${t}</span>`).join('')}
              </div>
            </div>
          `;
        }

        cellHtml += `</div>
          <div class="cell-footer">
            <span class="cell-action-hint">View Dish <i class="fa-solid fa-angle-right"></i></span>
          </div>
        `;

        cell.addEventListener('click', () => openModal(dt, dateKey, dayData));
      } else {
        cellHtml += `<div class="weekend-notice">${dayData?.note || 'No School Served'}</div>`;
      }

      cell.innerHTML = cellHtml;
      calendarGrid.appendChild(cell);
    });

    // End padding to complete row
    const totalRendered = firstWeekday + schoolDays.length;
    const remaining = (5 - (totalRendered % 5)) % 5;
    for (let i = 0; i < remaining; i++) {
      const cell = document.createElement('div');
      cell.className = 'calendar-day other-month';
      cell.innerHTML = `<div class="day-header"><span class="day-number">--</span></div>`;
      calendarGrid.appendChild(cell);
    }
  }

  function renderPdfDownloads() {
    if (!menuData || !menuData.pdf_downloads) return;

    pdfGrid.innerHTML = menuData.pdf_downloads.map(pdf => `
      <a href="${pdf.url}" target="_blank" rel="noopener" class="pdf-card">
        <i class="fa-solid fa-file-pdf pdf-icon"></i>
        <div class="pdf-info">
          <span class="pdf-title">${pdf.title}</span>
          <span class="pdf-meta">Waynesboro & KCMS School Nutrition • Official PDF</span>
        </div>
      </a>
    `).join('');
  }

  function openModal(dt, dateKey, dayData) {
    const formattedDate = dt.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });

    const schoolNames = {
      middle: 'Kate Collins Middle School (KCMS)',
      elementary: 'Waynesboro Elementary Schools',
      high: 'Waynesboro High School',
      prek: 'Wayne Hills Preschool'
    };

    modalDate.textContent = formattedDate;
    modalSchoolName.textContent = schoolNames[selectedSchool] || schoolNames.middle;

    let bfast = dayData.kcms_breakfast;
    let lunch = dayData.kcms_lunch;
    if (selectedSchool === 'elementary') lunch = dayData.elementary_lunch || lunch;
    if (selectedSchool === 'high') lunch = dayData.high_school_lunch || lunch;

    let modalHtml = '';

    // Hero Lunch Meal Image
    if (lunch && lunch.image) {
      modalHtml += `<img src="${lunch.image}" alt="${lunch.main}" class="modal-hero-img" />`;
    }

    modalHtml += `
      <div class="modal-meal-section breakfast">
        <div class="modal-meal-title"><i class="fa-solid fa-sun" style="color:#3B82F6;"></i> Breakfast Offering</div>
        <div class="modal-meal-main">${bfast ? bfast.main : 'Breakfast Sandwich & Fruit'}</div>
        <ul class="modal-sides-list">
          ${(bfast?.sides || ['Fresh Fruit Cup', '100% Fruit Juice', 'Choice of Milk']).map(s => `<li>${s}</li>`).join('')}
        </ul>
      </div>

      <div class="modal-meal-section">
        <div class="modal-meal-title"><i class="fa-solid fa-utensils" style="color:#F59E0B;"></i> Main Lunch Entrée</div>
        <div class="modal-meal-main">${lunch ? lunch.main : 'Chef Special Entrée'}</div>
        <ul class="modal-sides-list">
          ${(lunch?.sides || ['Steamed Vegetables', 'Fresh Side Salad', 'Chilled Fruit', 'Choice of Milk']).map(s => `<li>${s}</li>`).join('')}
        </ul>
        
        ${lunch?.alts ? `
          <div style="margin-top: 12px; padding-top: 10px; border-top: 1px rgba(255,255,255,0.1) solid;">
            <span style="font-size: 0.8rem; color: #F59E0B; font-weight: 700;">DAILY ALTERNATIVE ENTRÉES:</span>
            <div style="display: flex; gap: 6px; margin-top: 4px; flex-wrap: wrap;">
              ${lunch.alts.map(alt => `<span class="badge badge-tag" style="background: rgba(255,255,255,0.1); color:#FFF;">${alt}</span>`).join('')}
            </div>
          </div>
        ` : ''}

        <div class="tags-row" style="margin-top: 12px;">
          ${(lunch?.tags || ['Student Meal FREE']).map(t => `<span class="badge badge-tag">${t}</span>`).join('')}
        </div>
      </div>
    `;

    modalBody.innerHTML = modalHtml;
    dayModal.classList.remove('hidden');
  }

  function closeModal() {
    dayModal.classList.add('hidden');
  }
});
