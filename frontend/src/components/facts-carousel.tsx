import { useEffect, useState } from "react";
import {
    Carousel,
    CarouselContent,
    CarouselItem,
    type CarouselApi,
  } from "./ui/carousel"
import { useEngagement } from "../context/engagement-state";
import { mockFacts } from "../mock/facts";
  

export default function FactsCarousel() {

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
             

        }, 10000);
        return () => clearInterval(interval);

    }, [api]);
    
    return (
        <Carousel setApi={setApi} className="w-[864px] h-[497px] " opts={{loop: true}}>
            <CarouselContent>
                {
                    mockFacts.map((fact, index) => (
                        <CarouselItem key={index}>
                            <img src={fact.src}
                                className="w-[864px] h-[497px] object-cover"
                                alt="fact"
                            />
                        </CarouselItem>
                    ))
                }
            </CarouselContent>
           
           
        </Carousel>

    )
}