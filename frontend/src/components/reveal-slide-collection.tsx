import Reveal from "reveal.js";
import { SlideCollection } from "../types/slide-collection"
import RevealSlideContent from "./reveal-slide-content";


type RevealSlideCollectionProps = {
    collection: SlideCollection;
    dockRef: Reveal.Api;
}


export default function RevealSlideCollection({collection, dockRef}: RevealSlideCollectionProps) {

    return (
        <section>
            {
                collection.slides.map((slide, index) => {
                    return (
                        <section key={index}>
                            <RevealSlideContent content={slide} dockRef={dockRef} />
                        </section>
                    )
                })
            }
        </section>
    )
}