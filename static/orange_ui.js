$(document).ready(() => {
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
    
});