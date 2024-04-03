import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
if (!import.meta.env.VITE_SOCKET_URL) {
    throw new Error('Socket URL is not defined');
}

// "undefined" means the URL will be computed from the `window.location` object
const URL = import.meta.env.VITE_SOCKET_URL;


const socket = io(URL!);

export const useSocket = (setEngagementState: (value: any) => void) => {

    const [isConnected, setIsConnected] = useState(false);
    const [slideId, setSlideId] = useState<number | null>(null);
    const [postId, setPostId] = useState<number | null>(null);


    useEffect(() => {
      function onConnect() {
        setIsConnected(true);
      }
  
      function onDisconnect() {
        setIsConnected(false);
      }
  
      function onFooEvent(value: any) {
        
        setEngagementState(value.data);
      }

      function onMotionReport(payload: any) {
        socket.emit("full-report", {...payload, slideId, postId})

      }
  
      socket.on('connect', onConnect);
      socket.on('disconnect', onDisconnect);
      socket.on('message', onFooEvent);
      socket.on("motion-report", (payload: any) => onMotionReport(payload));
    }, []);

    return {
      isConnected,
      setSlideId, 
      setPostId
    }
    
}