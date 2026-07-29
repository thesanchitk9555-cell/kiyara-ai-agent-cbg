import { create } from 'zustand';

interface AgentState {
  isCallActive: boolean;
  toggleCall: () => void;
}

export const useAgentStore = create<AgentState>((set) => ({
  isCallActive: false,
  toggleCall: () => set((state) => ({ isCallActive: !state.isCallActive })),
}));
