import React, { createContext, useState } from 'react';
import { EngagementState } from '../types/engagement-state';


interface EngagementContextProps {
  engagementState: EngagementState;
  setEngagementState: React.Dispatch<React.SetStateAction<EngagementState>>;
}
const EngagementContext = createContext<EngagementContextProps | undefined>(undefined);

export function useEngagement() {
  const context = React.useContext(EngagementContext);
  if (context === undefined) {
    throw new Error('useEngagement must be used within a EngagementProvider');
  }
  return context;
}


export default function EngagementProvider({ children }: {children: React.ReactNode}) {
  const [engagementState, setEngagementState] = useState<EngagementState>('enter');

  return (
    <EngagementContext.Provider value={{ engagementState, setEngagementState }}>
      {children}
    </EngagementContext.Provider>
  );
};