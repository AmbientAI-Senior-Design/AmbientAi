import { useEffect } from "react";
import { SlideContent } from "../types/slide-content";


type SlideProps = {
    setSlideId: (slideId: number | null) => void;
    slide: SlideContent;
}

export const Slide = ({setSlideId, slide}: SlideProps) => {
    useEffect(() => {
        setSlideId(slide.slideId);
        return () => {
            setSlideId(null);
        }
    }, []);

    
    return (
       // @ts-ignore
        <section postId={slide.slideId} index={slide.index}>
            <img className="m-0" src={"https://placehold.co/864x994"} alt={"slide"} width={864} height={994} />
        </section>
    )
}
