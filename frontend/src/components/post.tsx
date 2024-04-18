import { useEffect } from "react";
import { SlideContent } from "../types/slide-content";

import { Slide } from "./slide";


type PostProps = {
    postId: number;
    setPostId: (postId: number | null) => void;
    setSlideId: (slideId: number | null) => void;
    slides: SlideContent[];
}


export const Post = ({setPostId, postId, setSlideId, slides}: PostProps) => {

    useEffect(() => {
        setPostId(postId);
    }, []);

    return (
        <section id={`${postId}`}>
            {
                slides.map((slide, index) => (
                    <Slide key={index} setSlideId={setSlideId} slide={slide} />
                ))
            }
        </section>
    )
}