import { InputForm } from "./InputForm";
import { useEffect, useState } from "react";

interface WelcomeScreenProps {
  handleSubmit: (
    submittedInputValue: string,
    effort: string,
    model: string
  ) => void;
  onCancel: () => void;
  isLoading: boolean;
}

const Star = ({ delay }: { delay: number }) => (
  <div
    className="absolute w-1 h-1 bg-white rounded-full opacity-70 animate-fall"
    style={{
      left: `${Math.random() * 100}%`,
      animationDelay: `${delay}s`,
      animationDuration: `${3 + Math.random() * 4}s`,
    }}
  />
);

const ShootingStar = ({ delay }: { delay: number }) => (
  <div
    className="absolute w-0 h-0 border-l-[0px] border-l-transparent border-r-[2px] border-r-white transform rotate-[-45deg] opacity-0 animate-shoot"
    style={{
      top: `${Math.random() * 20}%`,
      left: "100%",
      animationDelay: `${delay}s`,
      animationDuration: `${1 + Math.random() * 2}s`,
    }}
  />
);

const Sunray = ({ delay, angle }: { delay: number; angle: number }) => (
  <div
    className="absolute top-0 left-1/2 w-[2px] h-full origin-top opacity-0 animate-sunray"
    style={{
      background: 'linear-gradient(to bottom, rgba(255, 220, 150, 0.4), transparent)',
      transform: `rotate(${angle}deg)`,
      animationDelay: `${delay}s`,
    }}
  />
);

export const WelcomeScreen: React.FC<WelcomeScreenProps> = ({
  handleSubmit,
  onCancel,
  isLoading,
}) => {
  const [stars, setStars] = useState<number[]>([]);

  useEffect(() => {
    // Generate 50 random stars for background twinkling/falling
    const starDelays = Array.from({ length: 50 }, (_, i) => i * 0.1);
    setStars(starDelays);
  }, []);

  const sunrays = Array.from({ length: 12 }, (_, i) => ({
    angle: (i * 30) - 165,
    delay: i * 0.5,
  }));

  return (
    <div className="relative h-full flex flex-col items-center justify-center text-center px-4 flex-1 w-full max-w-3xl mx-auto gap-4 overflow-hidden">
      {/* Space Background with Darker Nebula Gradient */}
      <div className="fixed inset-0 bg-gradient-to-br from-black via-indigo-950/30 to-slate-900/40">
        {/* Twinkling Stars */}
        {stars.map((delay, i) => (
          <div
            key={`twinkle-${i}`}
            className="absolute w-[2px] h-[2px] bg-white rounded-full opacity-40 animate-twinkle"
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              animationDelay: `${delay}s`,
            }}
          />
        ))}
        
        {/* Falling Stars */}
        {stars.slice(0, 20).map((delay, i) => (
          <Star key={`fall-${i}`} delay={delay} />
        ))}
        
        {/* Shooting Stars */}
        {stars.slice(0, 5).map((delay, i) => (
          <ShootingStar key={`shoot-${i}`} delay={delay * 2} />
        ))}
        
        {/* Sunrays */}
        <div className="absolute inset-0 flex items-center justify-center overflow-hidden">
          {sunrays.map((ray, i) => (
            <Sunray key={`sunray-${i}`} delay={ray.delay} angle={ray.angle} />
          ))}
        </div>
        
        {/* Subtle Solar System Orb - Central Glow */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-32 h-32 bg-gradient-to-r from-amber-400/15 via-orange-400/10 to-yellow-500/15 rounded-full blur-xl animate-pulse-slow opacity-25" />
        </div>
        
        {/* Orbiting Planet (subtle) */}
        <div className="absolute top-1/4 left-1/4 w-4 h-4 bg-gradient-to-r from-blue-400/40 to-indigo-500/40 rounded-full animate-orbit opacity-50" />
      </div>

      {/* Content Overlay */}
      <div className="relative z-10 flex flex-col items-center gap-4">
        <div className="animate-fade-in-up">
          <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-blue-400 via-indigo-400 to-cyan-400 bg-clip-text text-transparent drop-shadow-lg mb-3 tracking-wide">
            Welcome.
          </h1>
          <p className="text-xl md:text-2xl text-neutral-300/80 backdrop-blur-sm drop-shadow-sm">
            How can I help you today?
          </p>
        </div>
        <div className="w-full mt-4 animate-fade-in-up animation-delay-200">
          <InputForm
            onSubmit={handleSubmit}
            isLoading={isLoading}
            onCancel={onCancel}
            hasHistory={false}
          />
        </div>
        <p className="text-xs text-neutral-500/70 animate-fade-in-up animation-delay-400 backdrop-blur-sm">
          Powered by Google Gemini and LangChain LangGraph.
        </p>
      </div>

      <style>{`
        @keyframes fall {
          0% {
            transform: translateY(-100vh) rotate(0deg);
            opacity: 1;
          }
          100% {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
          }
        }
        @keyframes shoot {
          0% {
            opacity: 0;
            transform: translateX(-100vw) translateY(0);
          }
          50% {
            opacity: 1;
          }
          100% {
            opacity: 0;
            transform: translateX(-200vw) translateY(-50vh);
          }
        }
        @keyframes twinkle {
          0%, 100% { opacity: 0.4; transform: scale(1); }
          50% { opacity: 0.8; transform: scale(1.2); }
        }
        @keyframes orbit {
          0% { transform: rotate(0deg) translateX(100px) rotate(0deg); }
          100% { transform: rotate(360deg) translateX(100px) rotate(-360deg); }
        }
        @keyframes fade-in-up {
          0% {
            opacity: 0;
            transform: translateY(20px);
          }
          100% {
            opacity: 1;
            transform: translateY(0);
          }
        }
        @keyframes pulse-slow {
          0%, 100% { opacity: 0.3; transform: scale(1); }
          50% { opacity: 0.5; transform: scale(1.1); }
        }
        @keyframes sunray {
          0% {
            opacity: 0;
            height: 0;
          }
          20% {
            opacity: 0.3;
            height: 50%;
          }
          40% {
            opacity: 0.5;
            height: 100%;
          }
          60% {
            opacity: 0.3;
            height: 100%;
          }
          100% {
            opacity: 0;
            height: 100%;
          }
        }
        .animate-fall {
          animation: fall linear infinite;
        }
        .animate-shoot {
          animation: shoot linear infinite;
        }
        .animate-twinkle {
          animation: twinkle 2s ease-in-out infinite;
        }
        .animate-orbit {
          animation: orbit 20s linear infinite;
        }
        .animate-fade-in-up {
          animation: fade-in-up 0.8s ease-out forwards;
        }
        .animation-delay-200 {
          animation-delay: 0.2s;
        }
        .animation-delay-400 {
          animation-delay: 0.4s;
        }
        .animate-pulse-slow {
          animation: pulse-slow 4s ease-in-out infinite;
        }
        .animate-sunray {
          animation: sunray 8s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
};