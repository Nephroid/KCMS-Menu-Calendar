/**
 * KCMS & Waynesboro Public Schools - Interactive Menu Calendar Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  // App State
  let menuData = null;
  let currentYear = 2026;
  let currentMonth = 8; // August
  let selectedSchool = 'middle'; // KCMS Middle School default
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

  // Fetch Menu JSON
  fetch('data/menus.json')
    .then(response => {
      if (!response.ok) throw new Error('Failed to load menu data');
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

    // Meal Filter Segmented Control
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

    // Modal Close handlers
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

    const firstDayIndex = new Date(currentYear, currentMonth - 1, 1).getDay(); // 0 = Sun
    // Convert to 0 = Mon, 6 = Sun
    const adjustedFirstDay = (firstDayIndex + 6) % 7;
    const totalDaysInMonth = new Date(currentYear, currentMonth, 0).getDate();

    // Previous month padding cells
    const prevMonthDays = new Date(currentYear, currentMonth - 1, 0).getDate();
    for (let i = adjustedFirstDay - 1; i >= 0; i--) {
      const dayNum = prevMonthDays - i;
      const cell = document.createElement('div');
      cell.className = 'calendar-day other-month';
      cell.innerHTML = `<div class="day-header"><span class="day-number">${dayNum}</span></div>`;
      calendarGrid.appendChild(cell);
    }

    // Current month cells
    for (let day = 1; day <= totalDaysInMonth; day++) {
      const monthStr = currentMonth.toString().padStart(2, '0');
      const dayStr = day.toString().padStart(2, '0');
      const dateKey = `${currentYear}-${monthStr}-${dayStr}`;

      const dt = new Date(currentYear, currentMonth - 1, day);
      const isWeekend = dt.getDay() === 0 || dt.getDay() === 6;
      const isToday = currentYear === 2026 && currentMonth === 8 && day === 27;

      const dayData = menuData && menuData.calendar ? menuData.calendar[dateKey] : null;

      const cell = document.createElement('div');
      cell.className = `calendar-day ${isWeekend ? 'weekend' : ''} ${isToday ? 'is-today' : ''}`;
      
      let cellHtml = `
        <div class="day-header">
          <span class="day-number">${day}</span>
          <span class="day-status">${isWeekend ? 'Weekend' : 'School Day'}</span>
        </div>
      `;

      if (isWeekend) {
        cellHtml += `<div class="weekend-notice">No Meals Served</div>`;
      } else if (dayData && dayData.is_school_day) {
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
          cell.style.opacity = '0.25';
        }

        cellHtml += `<div class="meal-preview-container">`;

        // Breakfast preview
        if ((selectedMealFilter === 'all' || selectedMealFilter === 'breakfast') && bfast) {
          cellHtml += `
            <div class="meal-block breakfast-block">
              <div class="meal-label"><i class="fa-solid fa-sun"></i> BFAST</div>
              <div class="meal-main-title">${bfast.main}</div>
            </div>
          `;
        }

        // Lunch preview
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
            <span class="cell-action-hint">Click details <i class="fa-solid fa-arrow-right"></i></span>
          </div>
        `;

        cell.addEventListener('click', () => openModal(dt, dateKey, dayData));
      } else {
        cellHtml += `<div class="weekend-notice">Menu Info Pending</div>`;
      }

      cell.innerHTML = cellHtml;
      calendarGrid.appendChild(cell);
    }

    // Next month padding cells
    const totalRendered = adjustedFirstDay + totalDaysInMonth;
    const remainingCells = (7 - (totalRendered % 7)) % 7;
    for (let i = 1; i <= remainingCells; i++) {
      const cell = document.createElement('div');
      cell.className = 'calendar-day other-month';
      cell.innerHTML = `<div class="day-header"><span class="day-number">${i}</span></div>`;
      calendarGrid.appendChild(cell);
    }
  }

  function renderPdfDownloads() {
    if (!menuData || !menuData.pdf_downloads) return;

    pdfGrid.innerHTML = menuData.pdf_downloads.slice(0, 8).map(pdf => `
      <a href="${pdf.url}" target="_blank" rel="noopener" class="pdf-card">
        <i class="fa-solid fa-file-pdf pdf-icon"></i>
        <div class="pdf-info">
          <span class="pdf-title">${pdf.title}</span>
          <span class="pdf-meta">Waynesboro School Nutrition • PDF Download</span>
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

    modalBody.innerHTML = `
      <div class="modal-meal-section breakfast">
        <div class="modal-meal-title"><i class="fa-solid fa-sun" style="color:#F59E0B;"></i> Breakfast Offering</div>
        <div class="modal-meal-main">${bfast ? bfast.main : 'Breakfast Sandwich & Fruit'}</div>
        <ul class="modal-sides-list">
          ${(bfast?.sides || ['Fresh Fruit Cup', '100% Fruit Juice', 'Choice of Low-Fat Milk']).map(s => `<li>${s}</li>`).join('')}
        </ul>
      </div>

      <div class="modal-meal-section">
        <div class="modal-meal-title"><i class="fa-solid fa-utensils" style="color:#10B981;"></i> Lunch Entrée</div>
        <div class="modal-meal-main">${lunch ? lunch.main : 'Chef Special Entrée'}</div>
        <ul class="modal-sides-list">
          ${(lunch?.sides || ['Steamed Vegetables', 'Fresh Side Salad', 'Chilled Fruit', 'Choice of Milk']).map(s => `<li>${s}</li>`).join('')}
        </ul>
        <div class="tags-row" style="margin-top: 12px;">
          ${(lunch?.tags || ['Student Meal FREE']).map(t => `<span class="badge badge-tag">${t}</span>`).join('')}
        </div>
      </div>
    `;

    dayModal.classList.remove('hidden');
  }

  function closeModal() {
    dayModal.classList.add('hidden');
  }
});
