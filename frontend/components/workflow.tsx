import { ArrowRightIcon, GithubIcon, SparkIcon } from "./icons";

const steps = ["Repository", "Architecture Agent", "Security Agent", "Documentation Agent", "Roadmap Agent", "Engineering Report"];

export function Workflow() {
  return (
    <section className="bg-slate-950 px-6 py-20 text-white sm:px-10" id="workflow">
      <div className="mx-auto max-w-6xl">
        <div className="text-center"><p className="text-sm font-semibold uppercase tracking-widest text-blue-300">A clear path from code to action</p><h2 className="mt-3 text-3xl font-bold tracking-tight sm:text-4xl">One repository. A complete engineering perspective.</h2></div>
        <ol className="mx-auto mt-12 flex max-w-4xl flex-col items-center gap-2 md:flex-row md:items-stretch md:gap-0">
          {steps.map((step, index) => <li className="flex w-full items-center md:w-auto md:flex-1" key={step}><div className="flex min-h-24 flex-1 flex-col items-center justify-center rounded-xl border border-white/15 bg-white/5 px-3 text-center"><span className="mb-2 text-blue-300">{index === 0 ? <GithubIcon className="h-5 w-5" /> : <SparkIcon className="h-5 w-5" />}</span><span className="text-sm font-semibold">{step}</span></div>{index < steps.length - 1 && <ArrowRightIcon className="my-1 h-5 w-5 shrink-0 rotate-90 text-blue-300 md:mx-2 md:rotate-0" />}</li>)}
        </ol>
      </div>
    </section>
  );
}

