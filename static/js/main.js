console.log("E-Commerce Website Loaded Successfully");

// Welcome Message
window.onload = function () {
    console.log("Welcome to Django E-Commerce");
};

// Confirm Before Submit
function confirmSave() {

    return confirm("Do you want to save this product?");

}

// Delete Confirmation
function confirmDelete(){

    return confirm("Are you sure to delete this product?");

}

// Alert Message
function showMessage(){

    alert("Welcome to E-Commerce Website");

}

// Dark Mode
function darkMode(){

    document.body.classList.toggle("dark");

}

// Scroll Top Button
window.onscroll = function(){

    let btn = document.getElementById("topBtn");

    if(btn){

        if(document.body.scrollTop > 200 || document.documentElement.scrollTop > 200){

            btn.style.display = "block";

        }

        else{

            btn.style.display = "none";

        }

    }

};

function topFunction(){

    window.scrollTo({

        top:0,

        behavior:"smooth"

    });

}