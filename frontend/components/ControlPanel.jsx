export default function ControlPanel({ status, onStart }) {
  const isRunning = status === "Running...";

  return (
    <header className="bg-white border-b p-4 md:px-8 flex flex-col sm:flex-row justify-between items-center gap-4 shadow-sm z-10">
      <div className="text-center sm:text-left">
        <h1 className="font-bold text-lg md:text-xl text-gray-800">Narrative Engine</h1>
        <div className="flex items-center justify-center sm:justify-start gap-2">
          <span className={`w-2 h-2 rounded-full ${isRunning ? 'bg-green-500 animate-pulse' : 'bg-gray-300'}`} />
          <p className="text-[10px] text-gray-500 font-mono uppercase tracking-widest">{status}</p>
        </div>
      </div>
      <button 
        onClick={onStart}
        disabled={isRunning}
        className="w-full sm:w-auto bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 transition-all active:scale-95"
      >
        {isRunning ? "Running..." : "Start Simulation"}
      </button>
    </header>
  );
}