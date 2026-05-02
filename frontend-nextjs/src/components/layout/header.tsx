"use client";

interface HeaderProps {
  location?: string;
}

export function Header({ location = "Manhattan, NY" }: HeaderProps) {
  return (
    <header className="flex justify-between items-center px-6 py-4 w-full sticky top-0 z-50 bg-[#FFF9F5] border-b border-red-100/50 shadow-lg rounded-lg mb-8">
      <div>
        <h1 className="text-2xl font-black text-[#b7122a] tracking-tighter" style={{ fontFamily: 'Epilogue, sans-serif' }}>
          Curated for You
        </h1>
        <p className="text-sm text-gray-600" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>
          Human-like intelligence, tailored to your unique palette.
        </p>
      </div>
      <div className="flex items-center gap-4">
        <span className="text-sm font-medium text-gray-800" style={{ fontFamily: 'Epilogue, sans-serif' }}>
          Location: <span className="text-[#b7122a]">{location}</span>
        </span>
        <button className="material-symbols-outlined text-gray-800 hover:bg-red-50 p-2 rounded-full transition-colors">
          account_circle
        </button>
      </div>
    </header>
  );
}
