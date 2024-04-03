import { SlideContent } from "../types/slide-content"
import Reveal from "reveal.js"


type RevealSlideContentProps = {
    content: SlideContent;
    dockRef: Reveal.Api;
}


export default function RevealSlideContent({content}: RevealSlideContentProps) {

    return (
        <section data-markdown={true}>
            {content.content}
        </section>
    )
}