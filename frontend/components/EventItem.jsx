"use client";
import { motion } from "framer-motion";
import { MessageSquare, Zap, Search, Info, Brain } from "lucide-react";

export default function EventItem({ event }) {
  const { type, speaker, character, content, action, agentic_reasoning } = event;

  // Logic: Actions use 'character', Dialogue uses 'speaker'
  const performer = speaker || character || (type === 'director_note' ? 'Director' : type);

  const config = {
    dialogue: { icon: <MessageSquare size={14} />, styles: "bg-white border-gray-200" },
    action: { icon: <Zap size={14} />, styles: "bg-blue-600 border-blue-700 text-white shadow-md" },
    director_note: { icon: <Info size={14} />, styles: "bg-amber-50 border-amber-200 text-amber-900 border-l-4 border-l-amber-500" },
    mystery_clue: { icon: <Search size={14} />, styles: "bg-purple-600 border-purple-700 text-white" }
  };

  const current = config[type] || { icon: <Info size={14} />, styles: "bg-gray-50 text-gray-600" };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`p-5 rounded-2xl border transition-all ${current.styles}`}
    >
      <div className="flex items-center gap-2 mb-3">
        <span className={`p-1.5 rounded-lg ${type === 'action' || type === 'mystery_clue' ? 'bg-white/20' : 'bg-black/5'}`}>
          {current.icon}
        </span>
        <span className="text-[10px] font-black uppercase tracking-widest opacity-80">
          {performer}
        </span>
      </div>
      
      <p className="text-lg leading-relaxed font-medium italic">
        {content || action}
      </p>

      {agentic_reasoning?.thought && (
        <details className="mt-4 pt-3 border-t border-black/10 group cursor-pointer">
          <summary className="text-[10px] font-bold opacity-60 hover:opacity-100 list-none flex items-center gap-1 uppercase tracking-widest">
            <Brain size={12} className="group-open:rotate-12 transition-transform" /> 
            Chain of Thought
          </summary>
          <div className="mt-2 text-sm italic text-gray-500 bg-black/5 p-3 rounded-xl">
            {agentic_reasoning.thought}
          </div>
        </details>
      )}
    </motion.div>
  );
}