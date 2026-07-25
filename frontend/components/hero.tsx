import { RepositoryUrlForm } from "./repository-url-form";
import { SparkIcon } from "./icons";

export function Hero() {
  return (
    <section className="relative overflow-hidden border-b border-blue-100 bg-gradient-to-b from-white via-blue-50 to-[#f8fbff] px-6 pb-24 pt-6 sm:px-10 sm:pb-32">
      <div className="absolute left-1/2 top-0 -z-0 h-96 w-96 -translate-x-1/2 rounded-full bg-blue-300/20 blur-3xl" />
      <div className="relative z-10 mx-auto max-w-6xl">
        <nav className="flex items-center justify-between" aria-label="Main navigation">
          <a className="flex items-center gap-2 text-lg font-bold tracking-tight text-slate-950" href="#top"><span className="grid h-8 w-8 place-items-center rounded-lg bg-blue-600 text-white"><SparkIcon className="h-4 w-4" /></span> RepoPilot</a>
          <a className="text-sm font-medium text-slate-600 transition hover:text-blue-700" href="#workflow">How it works</a>
        </nav>
        <div className="mx-auto max-w-4xl pt-20 text-center sm:pt-28">
          <p className="mx-auto inline-flex items-center gap-2 rounded-full border border-blue-200 bg-white/80 px-4 py-2 text-sm font-medium text-blue-700 shadow-sm"><span className="h-2 w-2 rounded-full bg-blue-500" /> Engineering intelligence for public repositories</p>
          <h1 className="mt-7 text-5xl font-bold tracking-tight text-slate-950 sm:text-7xl">Repo<span className="text-blue-600">Pilot</span></h1>
          <p className="mt-5 text-xl font-medium text-slate-700 sm:text-2xl">Your Autonomous Engineering Review Team</p>
          <p className="mx-auto mt-5 max-w-2xl text-base leading-7 text-slate-600 sm:text-lg">Turn an unfamiliar codebase into a clear engineering plan—architecture, security, documentation, and the next best improvements.</p>
          <RepositoryUrlForm />
        </div>
      </div>
    </section>
  );
}

