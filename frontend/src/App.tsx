
// App.tsx
import { useEffect, useRef, useState } from "react";
import Reveal from "reveal.js";
import "reveal.js/dist/reveal.css";
import "reveal.js/dist/theme/white.css";
import {motion} from "framer-motion";
import { useSocket } from "./socket";
import { EngagementState } from "./types/engagement-state";
import { SlideContent } from "./types/slide-content";
import {mockSlides} from "../src/mock/slides";


type SlideProps = {
    setSlideId: (slideId: number | null) => void;
    slide: SlideContent;
}

const Slide = ({ setSlideId, slide }: SlideProps) => {
    useEffect(() => {
        setSlideId(slide.slideId);
        return () => setSlideId(null);
    }, [setSlideId, slide.slideId]);

    // Function to convert text with periods into text with line breaks
    const formatText = (text:string) => {
        const newText = text.replace(/\. /g, '.<br /><br />');
        return {__html: newText};  // Returning an object suitable for dangerouslySetInnerHTML
    };

    return (
        <section 
            style={{
                display: 'flex',
                flexDirection: 'column',
                minHeight: '90vh',
                width: '100vw',
                margin: '5vh 0',
                overflow: 'hidden',
                alignItems: 'flex-start',
            }}
            data-post-id={slide.slideId}
            data-index={slide.index}
        >
            <div style={{ 
                height: '45vh',
                width: '100%',
                display: 'flex',
                justifyContent: 'flex-start',
                overflow: 'hidden'
            }}>
                <img 
                    src={slide.image} 
                    alt="Slide Image" 
                    style={{
                        height: '100%',
                        objectFit: 'cover'
                    }} 
                />
            </div>
            <div 
                style={{
                    height: '45vh',
                    width: 'calc(100% - 10px)',
                    marginLeft: '0px',
                    padding: '20px 20px 20px 0px',
                    boxSizing: 'border-box',
                    overflowY: 'auto',
                    textAlign: 'left',
                }}
            >
                <h2 style={{ margin: '0', padding: '0', fontSize: '34px' }}>{slide.slideId}</h2>
                <p style={{ margin: '0', padding: '0', fontSize: '24px' }} dangerouslySetInnerHTML={formatText(slide.content)}></p>
            </div>
        </section>
    );
}



type PostProps = {
    postId: number;
    setPostId: (postId: number | null) => void;
    setSlideId: (slideId: number | null) => void;
    slides: SlideContent[];
}

const Post = ({setPostId, postId, setSlideId, slides}: PostProps) => {

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


function App() {
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
       <div
       style={{
        position: "relative",
       }}
        >
            <motion.div 
            animate={{opacity: engagementState === "leave" ? 0.5 : 0,}}
                style={{
                position: "absolute", 
                top: 0, 
                left: 0 ,
                width: "100vw",
                height: "100vh",
                backgroundColor: "black",
                zIndex: 100,
                
                }}>
                
            </motion.div>
        <div style={{
         width: "100vw",
         height: "100vh",
        }}>
 
          <div className="reveal" ref={deckDivRef} >
              <div className="slides">
                  {

                    mockSlides.map((post, index) => (
                        <Post key={index} postId={post.slideId} setPostId={setPostId} setSlideId={setSlideId} slides={post.slides} />
                    ))

                  }
              </div>
          </div>
        </div>
       </div>
    );
}

export default App;