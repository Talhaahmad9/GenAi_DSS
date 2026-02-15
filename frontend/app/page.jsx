"use client";
import { useState, useRef, useEffect } from 'react';
import WorldSidebar from '@/components/WorldSidebar';
import EventFeed from '@/components/EventFeed';
import ControlPanel from '@/components/ControlPanel';

export default function Home() {
  const [events, setEvents] = useState([]);
  const [worldState, setWorldState] = useState({ items: {} });
  const [status, setStatus] = useState("Idle");
  
  // The Gatekeeper: Persists across re-renders to block duplicates
  const seenEvents = useRef(new Set());

  const startSimulation = () => {
    setEvents([]);
    setWorldState({ items: {} });
    seenEvents.current.clear(); // Clear the gatekeeper for new run
    setStatus("Running...");
    
    const eventSource = new EventSource("http://localhost:8000/stream-story");

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === "end") {
        setStatus("Complete");
        eventSource.close();
      } else {
        // Create a Unique Fingerprint
        // We use turn + type + first 20 chars of content to identify the event
        const contentSnippet = (data.content || data.action || "").substring(0, 20);
        const eventId = `${data.turn}-${data.type}-${contentSnippet}`;

        if (!seenEvents.current.has(eventId)) {
          seenEvents.current.add(eventId);
          
          setEvents((prev) => [...prev, data]);

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
      <main className="flex-1 flex flex-col h-full">
        <ControlPanel status={status} onStart={startSimulation} />
        <EventFeed events={events} />
      </main>
    </div>
  );
}