export function GraphIcon() {
  return (
    <svg width="36" height="36" viewBox="0 0 28 28" fill="none" aria-hidden="true">
      <style>{`
        .gi-pulse {
          animation: gi-pulse-anim 2.5s infinite ease-in-out;
          transform-origin: 14px 14px;
        }
        .gi-travel {
          offset-path: path('M14 14 L21 7');
          animation: gi-travel-anim 3s infinite linear;
          opacity: 0;
        }
        @keyframes gi-pulse-anim {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.15); }
        }
        @keyframes gi-travel-anim {
          0% { offset-distance: 0%; opacity: 0.8; }
          90% { offset-distance: 100%; opacity: 0.8; }
          100% { offset-distance: 100%; opacity: 0; }
        }
        @media (prefers-reduced-motion: reduce) {
          .gi-pulse, .gi-travel { animation: none; }
          .gi-travel { opacity: 0; }
        }
      `}</style>
      <g stroke="rgba(0,229,195,0.25)" strokeWidth="0.8">
        <line x1="14" y1="14" x2="7" y2="8" />
        <line x1="14" y1="14" x2="21" y2="7" />
        <line x1="14" y1="14" x2="7" y2="21" />
        <line x1="14" y1="14" x2="22" y2="20" />
        <line x1="7" y1="21" x2="22" y2="20" />
      </g>
      <g fill="#00e5c3">
        <circle cx="7" cy="8" r="2.5" opacity="0.7" />
        <circle cx="21" cy="7" r="2.5" opacity="0.7" />
        <circle cx="7" cy="21" r="2.5" opacity="0.7" />
        <circle cx="22" cy="20" r="2.5" opacity="0.7" />
        <circle cx="14" cy="14" r="2.5" className="gi-pulse" />
        <circle r="1.2" className="gi-travel" />
      </g>
    </svg>
  );
}

export function PatternIcon() {
  return (
    <svg width="36" height="36" viewBox="0 0 28 28" fill="none" aria-hidden="true">
      <style>{`
        .pi-scan {
          animation: pi-scan-anim 4s infinite linear;
          transform-origin: 14px 14px;
        }
        .pi-arc1 { animation: pi-fade 0.6s ease-out 0.0s both; }
        .pi-arc2 { animation: pi-fade 0.6s ease-out 0.2s both; }
        .pi-arc3 { animation: pi-fade 0.6s ease-out 0.4s both; }
        @keyframes pi-scan-anim {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @keyframes pi-fade {
          from { opacity: 0; } to { opacity: 1; }
        }
        @media (prefers-reduced-motion: reduce) {
          .pi-scan, .pi-arc1, .pi-arc2, .pi-arc3 { animation: none; }
        }
      `}</style>
      <g stroke="#ff9a3c" strokeLinecap="round" fill="none">
        <path d="M24 14 A10 10 0 0 1 9 22.66" strokeWidth="1.5" opacity="0.35" transform="rotate(-20,14,14)" className="pi-arc1" />
        <path d="M21 14 A7 7 0 0 1 10.5 20.06" strokeWidth="1.2" opacity="0.6" transform="rotate(20,14,14)" className="pi-arc2" />
        <path d="M18 14 A4 4 0 0 1 12 17.46" strokeWidth="1" opacity="0.9" transform="rotate(60,14,14)" className="pi-arc3" />
      </g>
      <line x1="14" y1="14" x2="14" y2="4" stroke="rgba(255,154,60,0.5)" strokeWidth="1" strokeLinecap="round" className="pi-scan" />
      <circle cx="14" cy="14" r="1.5" fill="#ff9a3c" />
    </svg>
  );
}

export function InvestigationIcon() {
  return (
    <svg width="36" height="36" viewBox="0 0 28 28" fill="none" aria-hidden="true">
      <style>{`
        .ii-glow {
          animation: ii-glow-anim 2.5s infinite ease-in-out;
        }
        @keyframes ii-glow-anim {
          0%, 100% { opacity: 0.1; }
          50% { opacity: 0.4; }
        }
        @media (prefers-reduced-motion: reduce) {
          .ii-glow { animation: none; opacity: 0.2; }
        }
      `}</style>
      <circle cx="12" cy="12" r="9" fill="rgba(78,168,222,0.15)" className="ii-glow" />
      <circle cx="12" cy="12" r="7" stroke="#4ea8de" strokeWidth="1.5" fill="none" />
      <line x1="17" y1="17" x2="23" y2="23" stroke="#4ea8de" strokeWidth="2.5" strokeLinecap="round" />
      <g stroke="rgba(78,168,222,0.5)" strokeWidth="0.7">
        <line x1="12" y1="9.5" x2="9.5" y2="13.5" />
        <line x1="9.5" y1="13.5" x2="14.5" y2="13.5" />
        <line x1="14.5" y1="13.5" x2="12" y2="9.5" />
      </g>
      <g fill="#4ea8de">
        <circle cx="12" cy="9.5" r="1.2" />
        <circle cx="9.5" cy="13.5" r="1.2" />
        <circle cx="14.5" cy="13.5" r="1.2" />
      </g>
    </svg>
  );
}
