import { useEffect, useRef } from 'react';
import EventItem from './EventItem';

export default function EventFeed({ events }) {
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [events]);

  return (
    <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6">
      <div className="max-w-2xl mx-auto space-y-6">
        {events.map((ev, i) => (
          <EventItem key={`${ev.turn}-${i}`} event={ev} />
        ))}
        <div ref={scrollRef} className="h-20" />
      </div>
    </div>
  );
}