const menuBtnHome = document.querySelector('.menu-btn-home');
const sectionOne = document.querySelector('.home-first-section');
const navbar = document.querySelector('.nav-home');
const navLeft = document.querySelector('.nav-left-home');
const navLogo = document.querySelector('.logo-home');
const logoImg = document.querySelector('.logo-img');
const homeBtn = document.querySelector('.nav-home-btn-home');
const shopBtn = document.querySelector('.nav-shop-btn-home');
const menuBtnBrgrHome = document.querySelector('.menu-btn-burger-home');
const cartHome = document.querySelector('.cart-home');
const sideMenu = document.querySelector('.side-menu');
const menuBtnClose = document.querySelector('.menu-btn-close');
const cartMenu = document.querySelector('.cart-menu');
const cartBtnClose = document.querySelector('.cart-btn-close');
const menuOverlay = document.querySelector('.menu-overlay');


let menuOpen = false;


const sectionOneObserver = new IntersectionObserver(function(entries,sectionOneObserver){
  entries.forEach(entry => {
    if(!entry.isIntersecting){
      navbar.classList.add("scrolled-down");
      navLeft.classList.add("nav-left-scrolled");
      // navLogo.classList.add("logo-home-scrolled");
      // navLogo.classList.remove("logo-home");
      logoImg.src = 'logo dark.png';
      homeBtn.classList.add('nav-home-btn-scrolled');
      shopBtn.classList.add('nav-shop-btn-scrolled');
      menuBtnHome.classList.add("menu-btn-home-scrolled");
      menuBtnHome.classList.remove("menu-btn-home");
      menuBtnBrgrHome.classList.add("menu-btn-burger-home-scrolled");
      menuBtnBrgrHome.classList.remove("menu-btn-burger-home");
      cartHome.src = "icons/cart solid dark.png";
    }
    else if(entry.isIntersecting){
      navbar.classList.remove("scrolled-down");
      navLeft.classList.remove("nav-left-scrolled");
      // navLogo.classList.remove("logo-home-scrolled");
      homeBtn.classList.remove('nav-home-btn-scrolled');
      shopBtn.classList.remove('nav-shop-btn-scrolled');
      // navLogo.classList.add("logo-home");
      logoImg.src = 'logo light.png';
      homeBtn.classList.remove('nav-home-btn-scrolled');
      shopBtn.classList.remove('nav-shop-btn-scrolled');
      menuBtnHome.classList.remove("menu-btn-home-scrolled");
      menuBtnHome.classList.add("menu-btn-home");
      menuBtnBrgrHome.classList.remove("menu-btn-burger-home-scrolled");
      menuBtnBrgrHome.classList.add("menu-btn-burger-home");
      cartHome.src = "icons/cart solid light.png";
      
    }
  })
})

menuBtnHome.addEventListener('click',menuAnimation);
menuBtnClose.addEventListener('click',menuClose);
cartHome.addEventListener('click', cartMenuOpen);
cartBtnClose.addEventListener('click',cartMenuClose);
menuOverlay.addEventListener('click',closeOverlay);

// MENU ANIMATION
  
function menuAnimation(e){
  if(!menuOpen){
    menuBtnHome.classList.add('open');
    menuOpen = true ;
    sideMenu.style.display = 'flex';
    menuOverlay.style.display = 'block';
    cartMenu.style.display = 'none'
  }
  else{
    menuBtnHome.classList.remove('open');
    menuOpen = false;
  }
  e.preventDefault();
}

function menuClose(e) {
  sideMenu.style.display = 'none';
  menuOverlay.style.display = 'none';
  menuBtnHome.classList.remove('open');
  menuOpen = false;
  e.preventDefault();
}

function closeOverlay(e) {
  if (e.target === menuOverlay) {
    menuOverlay.style.display = 'none';
    sideMenu.style.display = 'none';
    cartMenu.style.display = 'none';
    menuBtnHome.classList.remove('open');
    menuOpen = false;

  }
  
  e.preventDefault();
}

// CART MENU OPEN 

function cartMenuOpen(e) {
    cartMenu.style.display = 'flex'
    menuOverlay.style.display = 'block';
    sideMenu.style.display = 'none';

  e.preventDefault();
}

function cartMenuClose(e) {
  cartMenu.style.display = 'none';
  menuOverlay.style.display = 'none';
}

  sectionOneObserver.observe(sectionOne);