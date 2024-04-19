// App.tsx
import "reveal.js/dist/reveal.css";
import "reveal.js/dist/theme/white.css";
import RevealComponent from "./components/reveal-component";
import {motion} from "framer-motion";
import { FullScreen, useFullScreenHandle } from "react-full-screen";
import ReactWeather, { useOpenWeather } from 'react-open-weather';
import EmbeddingsCarousel from "./components/embeddings-carousel";
import FactsCarousel from "./components/facts-carousel";
import { useEffect, useState } from "react";
import { useEngagement } from "./context/engagement-state";


function App() {
    const handle = useFullScreenHandle();
    const handleFullScreen = () => {
        handle.enter();
    }
    const {engagementState} = useEngagement();


    const [opacity, setOpacity] = useState(0);

    useEffect(() => {
        if (engagementState === "leave") {
            setOpacity(0.8);
        } else {
            setOpacity(0);
        }

    }, [engagementState]);

    
    const { data, isLoading, errorMessage } = useOpenWeather({
        key: 'f7d0a17dbb4f5f8027630d62a813e9af',
        lat: '28.061604937548182',
        lon: '11-80.6244784705026',
        lang: 'en',
        unit: 'metric', // values are (metric, standard, imperial)
    
      });


    return (
        <FullScreen handle={handle} className="bg-white relative">
           
            <div className="relative z-0">
                <div className="top-bar">
                    AmbientAI
                    <button onClick={handleFullScreen}>Full screen</button>
                </div>
                <div className="parent-layout">
                    <div className="reveal-slides posts">
                        <RevealComponent  width="864px" height="984px"/>
                    </div >
                    
                    <div className="embeddings">
                        <EmbeddingsCarousel />
                    </div>
                    <div className="did-you-know">
                        <FactsCarousel />
                    </div>
                    

                </div> 
            </div >
            <motion.div className="absolute top-0 right-0 h-screen z-100 w-screen bg-black " 
                animate={{ opacity: opacity }}
            >
                

            </motion.div>     
        </FullScreen>
    )
}

export default App;