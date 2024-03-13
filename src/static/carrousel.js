// Assuming you have Socket.IO available
const socket = io.connect('http://127.0.0.1:8000');


socket.on('connect', () => console.log('connected to socket'));
socket.on("connect_error", (err) => {
  console.log(`connect_error due to ${err.message}`);
});

socket.on('connect_error', function() {
    const container = document.getElementById('slideshow-container');
    container.innerHTML = 'Failed to connect to the server';
});

let slideIndex = 0;

const generateCarrouselCell = (src) => {
    return `
        <div class="mySlides fade">
            <img src="${src}" style="width:100%">
        </div>
    `;
}

const generateCarrousel = (hrefs) => {
    let i;
    // insert cells for each href
    const container = document.getElementById('slideshow-container');
    container.innerHTML = '';
    hrefs.forEach(href => {
        container.innerHTML += generateCarrouselCell(href);
    });

    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    slideIndex++;
    if (slideIndex > slides.length) {slideIndex = 1}    
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";  

    setTimeout(showSlides, 10000); // Change image every 10 seconds
}

function showSlides() {
    socket.emit('refresh');
}

socket.on('update_data', function(hrefs) {
    generateCarrousel(hrefs);
});

