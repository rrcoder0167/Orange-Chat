$(document).ready(() => {
    //tab bar functionality
    const tabs = document.querySelectorAll('.tab');
    const slide = document.querySelector('.slide');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => {
        // move the slide element to the clicked tab
        const offsetLeft = tab.offsetLeft + (tab.offsetWidth / 2) - (slide.offsetWidth / 2);
        slide.style.left = `${offsetLeft}px`;
    
        // remove active class from all tabs and add it to the clicked tab
        tabs.forEach((tab) => {
          tab.classList.remove('active');
        });
        tab.classList.add('active');
    
        // show the corresponding tab content and hide others
        tabContents.forEach((content) => {
          content.style.display = 'none';
        });
        const tabContentId = tab.dataset.tabContent;
        const tabContent = document.querySelector(`#${tabContentId}`);
        tabContent.style.display = 'block';
    
        // add jello class to slide
        slide.classList.add('jello');
        // remove jello class from slide after animation ends
        slide.addEventListener('animationend', () => {
          slide.classList.remove('jello');
        }, { once: true });
      });
    });
    
    // set slide element to the first icon by default
    const firstTab = tabs[0];
    const offsetLeft = firstTab.offsetLeft + (firstTab.offsetWidth / 2) - (slide.offsetWidth / 2);
    slide.style.left = `${offsetLeft}px`;
    firstTab.classList.add('active');
    
    // show the first tab content by default
    const firstTabContentId = firstTab.dataset.tabContent;
    const firstTabContent = document.querySelector(`#${firstTabContentId}`);
    firstTabContent.style.display = 'block';
    
    var dropdown = document.querySelector('.dropdown');
    var submenu = dropdown.querySelector('.dropdown-submenu');
    
    dropdown.addEventListener('click', function(event) {
      event.stopPropagation();
      submenu.classList.toggle('show');
    });
    
    document.addEventListener('click', function(event) {
      if (!dropdown.contains(event.target)) {
        submenu.classList.remove('show');
      }
    });

    var profileBtn = $('.profile-btn');
    var dropdownArrow = $('.dropdown-arrow');
    var dropdownMenu = $('.dropdown-menu');
    var isDropdownOpen = false;
    dropdownArrow.css('display', 'none');//set the arrow to be invisible by default
  
    profileBtn.on('mouseenter', function() {
      dropdownArrow.css('display', 'inline-block');
    });
  
    profileBtn.on('mouseleave', function() {
      if (!dropdownMenu.hasClass('open')) {
        dropdownArrow.css('display', 'none');
      }
    });
  
    profileBtn.on('click', function(e) {
      e.stopPropagation();
      isDropdownOpen = !isDropdownOpen;
      profileBtn.css('width', isDropdownOpen ? '250px' : '');
      dropdownMenu.toggleClass('open');
      dropdownArrow.toggleClass('open');
      dropdownArrow.css('display', isDropdownOpen ? 'inline-block' : 'none');
    });
    
    // profile btn js
    $(document).on('click', function(e) {
      if (!profileBtn.is(e.target) && !dropdownMenu.has(e.target).length) {
        isDropdownOpen = false;
        profileBtn.css('width', '');
        dropdownMenu.removeClass('open');
        dropdownArrow.removeClass('open');
        dropdownArrow.css('display', 'none');
      } else {
        dropdownArrow.css('display', isDropdownOpen ? 'inline-block' : 'none');
      }
    });
  
    let userBadge = $('.user-badge');
    userBadge.each(function() {
      let description = $(this).find('.description');
      let badgeRect = this.getBoundingClientRect();
      let descriptionRect = description[0].getBoundingClientRect();
  
      if (descriptionRect.width > badgeRect.width) {
        let halfDescriptionWidth = descriptionRect.width / 2;
        let leftOffset = halfDescriptionWidth - (badgeRect.width / 2);
  
        description.css('left', `-${leftOffset}px`);
      }
    });
});

