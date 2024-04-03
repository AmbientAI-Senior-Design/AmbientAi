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
  
      socket.on('connect', onConnect);
      socket.on('disconnect', onDisconnect);
      socket.on('message', onFooEvent);
      
    }, []);

    return {
      isConnected,
      
    }
    
}