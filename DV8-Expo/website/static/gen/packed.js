window.onscroll=()=>{scrollFunction()};window.onload=()=>{scrollFunction()};function scrollFunction(){let nav=document.querySelector("nav");let scrollHeight=0;if(document.body.scrollTop>scrollHeight||document.documentElement.scrollTop>scrollHeight){nav.classList.add("scrolled");}else{nav.classList.remove("scrolled");}}