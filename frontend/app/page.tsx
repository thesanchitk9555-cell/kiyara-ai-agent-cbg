'use client';
import { useAgentStore } from '../store/useAgentStore';
import { motion } from 'framer-motion';

export default function KiyaraAIWorld() {
  const { isCallActive, toggleCall } = useAgentStore();

  return (
    <div className="min-h-screen bg-black text-cyan-400 font-sans flex flex-col items-center justify-center relative overflow-hidden">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1f2937_1px,transparent_1px),linear-gradient(to_bottom,#1f2937_1px,transparent_1px)] bg-[size:20px_20px] opacity-30"></div>

      <main className="z-10 flex flex-col items-center">
        <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-purple-500 mb-2">
          KIYARA AI
        </h1>
        <p className="text-gray-400 mb-10 tracking-widest text-sm uppercase">Autonomous College Agent</p>

        <div 
          onClick={toggleCall}
          className={`w-56 h-56 rounded-full cursor-pointer flex items-center justify-center transition-all duration-500 ${isCallActive ? 'shadow-[0_0_80px_#06b6d4]' : 'shadow-[0_0_20px_#a855f7] hover:shadow-[0_0_40px_#a855f7]'}`}
        >
          {isCallActive ? (
            <motion.div 
              animate={{ scale: [1, 1.3, 1] }} 
              transition={{ repeat: Infinity, duration: 1.2 }}
              className="w-24 h-24 bg-cyan-400 rounded-full blur-lg"
            />
          ) : (
            <span className="text-white font-bold tracking-wider z-20">START AGENT</span>
          )}
          <div className="absolute w-56 h-56 bg-gradient-to-br from-cyan-900 to-purple-900 rounded-full opacity-20"></div>
        </div>
      </main>
    </div>
  );
}
