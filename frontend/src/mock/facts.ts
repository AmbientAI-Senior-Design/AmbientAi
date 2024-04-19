type Fact = {
    src: string;
}


const host = "http://localhost:8000/static/";

export const mockFacts: Fact[]  = [
    
        {
            src: host + "fact-top-gun.png"
        },
        {
            src: host + "fact-monroe.png"
        },
        {
            src: host + "fact-microwave.png"
        },
        {
            src: host + "fact-harris.png"
        },
        {
            src: host + "fact-grumman.png"
        },
        
    
]