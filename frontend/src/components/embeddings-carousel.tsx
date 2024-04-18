import { useEffect, useState } from "react";
import {
    Carousel,
    CarouselContent,
    CarouselItem,
    type CarouselApi,
  } from "./ui/carousel"
import { useEngagement } from "../context/engagement-state";

  

export default function EmbeddingsCarousel() {

    const [api, setApi] = useState<CarouselApi>()
    const {engagementState} = useEngagement();

    useEffect(() => {
        if (!api) return;
        // run at an interval of 10 seconds
        const interval = setInterval(() => {

            if (engagementState === "leave") {
                return;
            }

            api.scrollNext();
             

        }, 5000);
        return () => clearInterval(interval);

    }, [api]);
    
    return (
        <Carousel setApi={setApi} className="w-[864px] h-[497px] " opts={{loop: true}}>
            <CarouselContent>
                <CarouselItem className="">
                    <embed src="https://livethreatmap.radware.com/" width={864} height={497}></embed>
                </CarouselItem>
                <CarouselItem>
                <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d5476.858140374368!2d-80.62191519482731!3d28.06522494267135!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x88de1204fc52a6f7%3A0x37ba57635d6a3f15!2sFlorida%20Institute%20of%20Technology!5e0!3m2!1sen!2sus!4v1713470959208!5m2!1sen!2sus" width="864" height="497"  loading="lazy"></iframe>
                </CarouselItem>
                <CarouselItem>
                    <embed src="https://threatmap.fortiguard.com/" width={864} height={497}></embed>
                </CarouselItem>
            </CarouselContent>
           
           
        </Carousel>

    )
}