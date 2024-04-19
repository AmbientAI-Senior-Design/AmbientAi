import { SlideCollection } from "../types/slide-collection";


const host = "http://localhost:8000/static/";

export const mockSlides: SlideCollection[] = [
    {
        slideId: 1,
        slides: [
            {
                slideId: 1,
                index: 0,
                duration: 1000,
                src: host + "l3harrisT.png"
            },
            {
                slideId: 1,
                index: 1,
                duration: 2000,
                src: host + "countersatL3V.png"
            },
            {
                slideId: 1,
                index: 2,
                duration: 2000,
                src: host + "viperL3V.png"
            },
            
        ]
    },
    
];