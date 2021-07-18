const statsMenu = document.querySelector('.stats-menu');
const statsMenuBtn = document.querySelector('.stats-menu-btn');
const statsMenuClose = document.querySelector('.stats-menu-close');

statsMenuBtn.addEventListener('click', (e) => {
    statsMenu.style.display = "flex";
    e.preventDefault();
})

statsMenuClose.addEventListener('click' , (e) => {
    statsMenu.style.display = "none";
    e.preventDefault();
})
