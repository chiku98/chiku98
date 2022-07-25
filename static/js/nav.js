let menu = document.querySelector('#nav_menu_btn');
let navbar_menu = document.querySelector('.navbar_menu');

menu.onclick = () =>{
    menu.classList.toggle('fa-times');
    navbar_menu.classList.toggle('active');
}

window.onscroll = () =>{
    menu.classList.remove('fa-times');
    navbar_menu.classList.remove('active');
}