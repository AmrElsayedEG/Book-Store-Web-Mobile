const subtotalPrice = document.querySelector('.subtotal-price-SPP');
const subtotalPriceFull = document.querySelector('.subtotal-price-full-SPP');
const shippingPrice = document.querySelector('.shipping-price-SPP');
const shippingPriceFull = document.querySelector('.shipping-price-full-SPP');
const totalPrice = document.querySelector('.total-price-SPP');
const totalPriceFull = document.querySelector('.total-price-full-SPP');
const totalSummaryPrice = document.querySelector('.total-summary-price-SPP');
const showOrderSummaryText = document.querySelector('.show-order-summary-text');
const orderSummaryContent = document.querySelector('.order-summary-content');
let orderSummaryOpen = false ;


showOrderSummaryText.addEventListener('click',openOrderSummary);


// show purshased items menu function
function openOrderSummary(e) {

    if (!orderSummaryOpen) {
        orderSummaryOpen = true ;
        orderSummaryContent.style.display = 'grid';
    }
    else {
        orderSummaryOpen = false ;
        orderSummaryContent.style.display = 'none';
    }
    
}

// CHANING TOTAL PRICE 

const menuBtn = document.querySelector('.menu-btn');
const menuBtnClose = document.querySelector('.menu-btn-close');
const sideMenu = document.querySelector('.side-menu');
const menuOverlay = document.querySelector('.menu-overlay');
const cart = document.querySelector('.cart');
const cartMenu = document.querySelector('.cart-menu');
const cartBtnClose = document.querySelector('.cart-btn-close');
let menuOpen = false ;

// EVENT LISTENERS
menuBtn.addEventListener('click',menuAnimation);
menuBtnClose.addEventListener('click',menuClose);
cart.addEventListener('click', cartMenuOpen);
cartBtnClose.addEventListener('click',cartMenuClose);
menuOverlay.addEventListener('click',closeOverlay);

// MENU ANIMATION
 
function menuAnimation(e){
   if(!menuOpen){
     menuBtn.classList.add('open');
     menuOpen = true ;
     sideMenu.style.display = 'flex';
     menuOverlay.style.display = 'block';
     cartMenu.style.display = 'none';
   }
   else{
     menuBtn.classList.remove('open');
     menuOpen = false;
   }
   e.preventDefault();
 }

 function menuClose(e) {
   sideMenu.style.display = 'none';
   menuOverlay.style.display = 'none';
   menuBtn.classList.remove('open');
   menuOpen = false;
   e.preventDefault();
 }

 function closeOverlay(e) {
   if (e.target === menuOverlay) {
     menuOverlay.style.display = 'none';
     sideMenu.style.display = 'none';
     cartMenu.style.display = 'none';
     menuBtn.classList.remove('open');
     // menuBtnHome.classList.remove('open');
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