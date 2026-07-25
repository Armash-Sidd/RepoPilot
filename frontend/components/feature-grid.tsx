import { SparkIcon } from "./icons";

const features = [
  ["Architecture Analysis", "Understand project structure, key boundaries, and how the system fits together."],
  ["Security Review", "Surface practical security signals and focused hardening opportunities."],
  ["Documentation Review", "Find the gaps that make onboarding and maintenance harder than they should be."],
  ["Tech Stack Detection", "Identify languages, frameworks, dependencies, and development tooling."],
  ["Engineering Roadmap", "Convert observations into an ordered plan for measurable improvement."]
];

export function FeatureGrid() {
  return (
    <section className="px-6 py-20 sm:px-10" id="capabilities">
      <div className="mx-auto max-w-6xl">
        <div className="max-w-2xl"><p className="text-sm font-semibold uppercase tracking-widest text-blue-600">Review with confidence</p><h2 className="mt-3 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">Everything needed for a first, informed engineering read.</h2></div>
        <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {features.map(([title, description]) => <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:border-blue-200 hover:shadow-lg hover:shadow-blue-950/5" key={title}><span className="grid h-10 w-10 place-items-center rounded-xl bg-blue-50 text-blue-600"><SparkIcon className="h-5 w-5" /></span><h3 className="mt-5 text-lg font-semibold text-slate-900">{title}</h3><p className="mt-2 text-sm leading-6 text-slate-600">{description}</p></article>)}
        </div>
      </div>
    </section>
  );
}

