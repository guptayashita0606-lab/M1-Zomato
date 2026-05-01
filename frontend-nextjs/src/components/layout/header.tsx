"use client";

interface HeaderProps {
  location?: string;
}

export function Header({ location = "Manhattan, NY" }: HeaderProps) {
  return (
    <header className="flex justify-between items-center px-6 py-4 w-full sticky top-0 z-50 bg-[#FFF9F5] border-b border-red-100/50 shadow-[0_4px_20px_rgba(226,55,68,0.05)] rounded-lg mb-xl">
      <div>
        <h1 className="text-2xl font-black text-[#E23744] tracking-tighter font-display-xl">Curated for You</h1>
        <p className="font-body-md text-on-secondary-container">Human-like intelligence, tailored to your unique palette.</p>
      </div>
      <div className="flex items-center gap-lg">
        <span className="font-headline font-medium text-stone-800">
          Location: <span className="text-[#E23744]">{location}</span>
        </span>
        <button className="material-symbols-outlined text-stone-800 hover:bg-red-50 p-2 rounded-full transition-colors">
          account_circle
        </button>
      </div>
    </header>
  );
}
