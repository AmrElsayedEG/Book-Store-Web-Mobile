 const aProductCP = document.querySelectorAll('.product-details-CP') ;
 const plusCP = document.querySelector('.plus-CP'); 
 const minusCP = document.querySelector('.minus-CP');
 const quantityCP = document.querySelector('.quantity-CP');
 const RemoveCP = document.querySelector('.remove-product-CP');
 const productTotalPriceCP = document.querySelector('.book-total-price-CP');
 const allBooksTotalPriceCP = document.querySelector('.all-products-total-price-CP');
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
//  document.body.addEventListener('click',increaseQuantityCP);
//  document.body.addEventListener('click',decreaseQuantityCP);
 document.body.addEventListener('click',removeItemCP);

// DECCREASING QUANTITY FUNCTION CART
  // function decreaseQuantityCP(e){
  //   if(e.target.className === ('minus-CP')) {
  //     productQuantity = parseInt(e.target.parentElement.childNodes[3].innerText);
  //   if(productQuantity !== 1){
  //       productQuantity -=1;
  //       e.target.parentElement.childNodes[3].innerText = productQuantity;
  //       productMainPrice = parseFloat(e.target.parentElement.parentElement.childNodes[3].childNodes[1].textContent);       
  //       e.target.parentElement.parentElement.childNodes[7].childNodes[1].childNodes[2].textContent= (productQuantity * productMainPrice).toFixed(2);
  //       totalPriceFunction();
  //     }
  //   }
  //    e.preventDefault();
  // }

   // INCREASING QUANTITY FUNCTION CART
  // function increaseQuantityCP(e){
  //     if(e.target.className === ('plus-CP')){
  //         productQuantity = parseInt(e.target.parentElement.childNodes[3].innerText);
  //         productQuantity +=1;
  //         e.target.parentElement.childNodes[3].innerText = productQuantity;
  //         productMainPrice = parseFloat(e.target.parentElement.parentElement.childNodes[3].childNodes[1].nodeValue);
  //         e.target.parentElement.parentElement.childNodes[7].childNodes[1].childNodes[2].textContent= (productQuantity * productMainPrice).toFixed(2);
  //         totalPriceFunction();
  //     }
  //    e.preventDefault();
  // }

  // REMOVING AN ITEM FROM THE CART
  function removeItemCP(e){
    if(e.target.className === ('remove-product-CP')){
      e.target.parentElement.parentElement.remove();
      // itemPrice = parseFloat(e.target.parentElement.childNodes[1].childNodes[2].textContent) ;
      // allBooksTotalPriceCP.childNodes[2].textContent = (parseFloat(allBooksTotalPriceCP.childNodes[2].textContent) - itemPrice).toFixed(2) ;
    }
  }

    
    // CHANGING THE TOTAL PRICE
    // function totalPriceFunction() {
    //   let singleProductPrice = 0;
    //   let TotalProductsPrice = 0 ;
    //   for (i = 0  ; i < aProductCP.length ; i++ ) {
    //      singleProductPrice = parseFloat(aProductCP[i].childNodes[7].childNodes[1].childNodes[2].textContent) ;
    //      TotalProductsPrice = TotalProductsPrice + singleProductPrice ;
    //      allBooksTotalPriceCP.childNodes[2].textContent = TotalProductsPrice.toFixed(2);
    //    }
    // }

    // totalPriceFunction();
    


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