$(document).ready(function() {
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
  