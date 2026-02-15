"use client";
import { useState, useRef } from 'react';
import WorldSidebar from '@/components/WorldSidebar';
import EventFeed from '@/components/EventFeed';
import ControlPanel from '@/components/ControlPanel';

export default function Home() {
  const [events, setEvents] = useState([]);
  const [worldState, setWorldState] = useState({ items: {} });
  const [status, setStatus] = useState("Idle");
  
  // THE GATEKEEPER: Persistent storage for unique event fingerprints
  const processedKeys = useRef(new Set());

  const startSimulation = () => {
    setEvents([]);
    setWorldState({ items: {} });
    processedKeys.current.clear(); 
    setStatus("Running...");
    
    const eventSource = new EventSource("http://localhost:8000/stream-story");

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === "end") {
        setStatus("Complete");
        eventSource.close();
      } else {
        // Fingerprint: Turn + Type + first 30 chars of content
        const contentSnippet = (data.content || data.action || "").substring(0, 30);
        const fingerprint = `${data.turn}-${data.type}-${contentSnippet}`;

        if (!processedKeys.current.has(fingerprint)) {
          processedKeys.current.add(fingerprint);
          
          setEvents((prev) => [...prev, data]);

          // Update sidebar with Entity Registry snapshots
          if (data.entity_updates) {
            setWorldState({ items: data.entity_updates.items });
          }
        }
      }
    };

    eventSource.onerror = () => {
      setStatus("Disconnected");
      eventSource.close();
    };
  };

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden text-gray-900">
      <WorldSidebar items={worldState.items} />
      <main className="flex-1 flex flex-col h-full overflow-hidden">
        <ControlPanel status={status} onStart={startSimulation} />
        <EventFeed events={events} />
      </main>
    </div>
  );
}