// App.tsx
import "reveal.js/dist/reveal.css";
import "reveal.js/dist/theme/white.css";
import RevealComponent from "./components/reveal-component";

import { FullScreen, useFullScreenHandle } from "react-full-screen";
import ReactWeather, { useOpenWeather } from 'react-open-weather';
import EmbeddingsCarousel from "./components/embeddings-carousel";
import FactsCarousel from "./components/facts-carousel";

function App() {
    const handle = useFullScreenHandle();
    const handleFullScreen = () => {
        handle.enter();
    }

    const { data, isLoading, errorMessage } = useOpenWeather({
        key: 'f7d0a17dbb4f5f8027630d62a813e9af',
        lat: '28.061604937548182',
        lon: '11-80.6244784705026',
        lang: 'en',
        unit: 'metric', // values are (metric, standard, imperial)
    
      });


    return (
        <FullScreen handle={handle} className="bg-white">
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
        </FullScreen>
    )
}

export default App;