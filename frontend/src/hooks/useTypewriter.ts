import { useEffect, useState } from "react";

export function useTypewriter(text: string, speed = 30): string {
  const [displayed, setDisplayed] = useState("");

  useEffect(() => {
    const prefersReduced =
      typeof window.matchMedia === "function" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (prefersReduced) {
      setDisplayed(text);
      return;
    }

    setDisplayed("");
    let i = 0;
    const timer = setInterval(() => {
      i++;
      setDisplayed(text.slice(0, i));
      if (i >= text.length) clearInterval(timer);
    }, speed);

    return () => clearInterval(timer);
  }, [text, speed]);

  return displayed;
}
