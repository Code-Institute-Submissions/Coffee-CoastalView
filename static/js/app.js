// Side Menu
    const sideNav = document.querySelector('.sidenav');
    M.Sidenav.init(sideNav, {});

// Slider
    const slider = document.querySelector('.slider');
    M.Slider.init(slider, {
        indicators: false,
        height: 500,
        transition: 500,
        interval: 6000
      });      

// Modal Init
    let modalElems = document.querySelectorAll('.modal');
    M.Modal.init(modalElems);    
// Validation

var password = document.getElementById("password")
var confirm_password = document.getElementById("confirm_password");
function validatePassword()
{
    if(password.value != confirm_password.value)
    {
        confirm_password.setCustomValidity("Passwords Don't Match");
    }
    else
    {
        confirm_password.setCustomValidity('');
    }
}

password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;