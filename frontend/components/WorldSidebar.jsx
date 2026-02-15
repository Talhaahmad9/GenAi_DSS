"use client";
import { motion, AnimatePresence } from "framer-motion";
import { Box, User, Activity } from "lucide-react";

export default function WorldSidebar({ items = {} }) {
  return (
    <aside className="w-full md:w-80 h-full bg-white border-r border-gray-100 p-6 overflow-y-auto">
      <div className="flex items-center gap-3 mb-8">
        <div className="p-2 bg-blue-600 rounded-xl text-white">
          <Activity size={20} />
        </div>
        <h2 className="text-xl font-bold tracking-tight">World State</h2>
      </div>
      
      <div className="space-y-6">
        <h3 className="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">Live Registry</h3>
        <div className="space-y-3">
          <AnimatePresence mode="popLayout">
            {Object.entries(items).map(([name, info]) => (
              <motion.div 
                key={name}
                layout
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="p-4 bg-gray-50 rounded-2xl border border-gray-200/50 hover:border-blue-200 transition-colors group"
              >
                <div className="flex items-center gap-2 mb-3">
                  <Box size={14} className="text-gray-400 group-hover:text-blue-500 transition-colors" />
                  <p className="font-bold text-sm text-gray-800 capitalize">{name.replace('_', ' ')}</p>
                </div>
                
                <div className="grid grid-cols-2 gap-2">
                  <div className="bg-white p-2 rounded-lg border border-gray-100">
                    <p className="text-[8px] uppercase text-gray-400 font-bold mb-1">Owner</p>
                    <div className="flex items-center gap-1">
                      <User size={10} className="text-blue-500" />
                      <span className="text-[10px] font-bold text-gray-700">{info.owner || 'Common'}</span>
                    </div>
                  </div>
                  <div className="bg-white p-2 rounded-lg border border-gray-100">
                    <p className="text-[8px] uppercase text-gray-400 font-bold mb-1">Status</p>
                    <span className="text-[10px] font-bold text-amber-600 truncate block">{info.status}</span>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>
    </aside>
  );
}