import { SlideCollection } from "../types/slide-collection";


export const mockSlides: SlideCollection[] = [
    {
        slideId: 1,
        slides: [
            {
                slideId: 1,
                index: 0,
                duration: 1000,
                content: "Slide 1"
            },
            {
                slideId: 1,
                index: 1,
                duration: 2000,
                content: "Slide 2"
            },
            
        ]
    },
    {
        slideId: 2,
        slides: [
            {
                slideId: 2,
                index: 0,
                duration: 2000,
                content: "Slide 1"
            },
            {
                slideId: 2,
                index: 1,
                duration: 3000,
                content: "Slide 2"
            },
            
        ]
    },
    {
        slideId: 3,
        slides: [
            {
                slideId: 3,
                index: 0,
                duration: 2000,
                content: "Slide 1"
            },
            
        ]
    },
    {
        slideId: 4,
        slides: [
            {
                slideId: 4,
                index: 0,
                duration: 2000,
                content: "Slide 1"
            },
           
        ]
    }
];