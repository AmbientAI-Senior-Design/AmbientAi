import { useRef, useState, useEffect } from "react";
import Reveal from "reveal.js";
import { mockSlides } from "../mock/slides";
import { useSocket } from "../socket";
import { EngagementState } from "../types/engagement-state";
import { Post } from "../App"; 


export default function RevealComponent() {
    const deckDivRef = useRef<HTMLDivElement>(null); // reference to deck container div
    const deckRef = useRef<Reveal.Api | null>(null); // reference to deck reveal instance
    const [engagementState, setEngagementState] = useState<EngagementState>("enter");

    const {setPostId, setSlideId } = useSocket(setEngagementState);
    const [isReady, setIsReady] = useState(false);
   

     useEffect(() => {
         if (!isReady) return;
         // run at an interval of 10 seconds
         const interval = setInterval(() => {
             if (engagementState === "leave") {
                 return;
             }

             if (engagementState === "user_engaged") {
                 deckRef.current?.down();
                 return;
             }
             deckRef.current?.right();

         }, 5000);
         return () => clearInterval(interval);

     }, [isReady, engagementState]);
    
    useEffect(() => {
        // Prevents double initialization in strict mode
        if (deckRef.current) return;

        deckRef.current = new Reveal(deckDivRef.current!, {
            transition: "slide",
            // other config options
            loop: true,
            controls: false,
            progress: false,
            touch: false,
            
        });

        deckRef.current.on("slidechanged", (event) => {
            // @ts-ignore
            setPostId(event.currentSlide.getAttribute("postId")!);
            // @ts-ignore
            setSlideId(event.currentSlide.getAttribute("index")!);
            
        });


        deckRef.current.initialize().then(() => {
            // good place for event handlers and plugin setups
            setIsReady(true);
            
        });

        return () => {
            try {
                if (deckRef.current) {
                    deckRef.current.destroy();
                    deckRef.current = null;
                }
            } catch (e) {
                console.warn("Reveal.js destroy call failed.");
                console.error(e);
            }
        };
    }, [engagementState]);

    return (
        <div className="reveal" ref={deckDivRef} >
              <div className="slides">
                  {

                    mockSlides.map((post, index) => (
                        <Post key={index} postId={post.slideId} setPostId={setPostId} setSlideId={setSlideId} slides={post.slides} />
                    ))

                  }
              </div>
          </div>
    )

}