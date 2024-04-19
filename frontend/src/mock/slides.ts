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
    {
        slideId: 2,
        slides: [
            {
                slideId: 2,
                index: 0,
                duration: 1000,
                src: host + "ambientAICompanyPage.png"
            },
            {
                slideId: 2,
                index: 1,
                duration: 2000,
                src: host + "whatAmbientAI.png"
            },
            {
                slideId: 2,
                index: 2,
                duration: 2000,
                src: host + "whyAmbientAI.png"
            },
            {
                slideId: 2,
                index: 3,
                duration: 2000,
                src: host + "howAmbientAI.png"
            },
        ]
    },
    {
        slideId: 3,
        slides: [
            {
                slideId: 3,
                index: 0,
                duration: 1000,
                src: host + "flTechFactsTitle.png"
            },
            {
                slideId: 3,
                index: 1,
                duration: 2000,
                src: host + "Space.png"
            },
            {
                slideId: 3,
                index: 2,
                duration: 2000,
                src: host + "NotableAlumni.png"
            },
            {
                slideId: 3,
                index: 3,
                duration: 2000,
                src: host + "CompSci.png"
            },
            {
                slideId: 3,
                index: 4,
                duration: 2000,
                src: host + "Diversity.png"
            },
            
            
        ]
    },
    
];