document.addEventListener('DOMContentLoaded', function() {
    let slideIndex = 0;
    
    const generateCarrouselCell = (src, caption) => {
        return `
            <div class="mySlides fade">
                <img src="${src}" style="width:100%">
            </div>
        `;
    }

    const generateCarrousel = () => {

        let i;
        let hrefs = [
            'https://picsum.photos/1222/990',
            'https://picsum.photos/1222/990',
            'https://picsum.photos/1222/990'
        ]
        // insert cells for each href
        const container = document.getElementById('slideshow-container');
        container.innerHTML = '';
        hrefs.forEach(href => {
            container.innerHTML += generateCarrouselCell(href, 'Caption');
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
        generateCarrousel();
    }
    
    showSlides();
});