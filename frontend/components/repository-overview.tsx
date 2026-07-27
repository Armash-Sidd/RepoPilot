"use client";

export type AnalysisResponse = {
  success: true;
  owner: string;
  repository: string;
  repository_url: string;
  analysis: {
    metadata: { description: string | null; default_branch: string; topics: string[]; license: string | null; is_archived: boolean; stargazers_count: number; forks_count: number; watchers_count: number; last_updated_at: string };
    languages: Array<{ name: string; bytes: number; percentage: number }>;
    structure: { has_readme: boolean; root_files: string[]; root_directories: string[] };
    technology_signals: Array<{ file_name: string; category: string; label: string }>;
    evidence: { directory_tree: string[]; files: Array<{ path: string; category: string; content: string }>; tree_was_truncated: boolean };
    engineering_review: {
      architecture_summary: string;
      architecture_evidence_paths: string[];
      technology_stack: string[];
      technology_stack_evidence_paths: string[];
      findings: Array<{ category: string; title: string; detail: string; severity: string; evidence_paths: string[]; recommendation: string | null; priority: number | null }>;
    };
    health: {
      overall_score: number;
      label: "Excellent" | "Good" | "Fair" | "Needs Improvement";
      categories: Array<{ name: string; score: number; weight: number; explanation: string; evidence_paths: string[]; recommendation: string | null }>;
      top_strengths: Array<{ category: string; title: string; detail: string; evidence_paths: string[] }>;
      highest_priority_improvements: Array<{ category: string; title: string; detail: string; evidence_paths: string[] }>;
    };
    intelligence: {
      documentation: Array<{ title: string; detail: string; status: string; evidence_paths: string[] }>;
      development_workflow: Array<{ title: string; detail: string; status: string; evidence_paths: string[] }>;
      project_type: { project_type: string; detail: string; evidence_paths: string[] };
      technology_understanding: Array<{ title: string; detail: string; status: string; evidence_paths: string[] }>;
      best_practices: Array<{ title: string; detail: string; status: string; evidence_paths: string[] }>;
    };
  };
};

function Detail({ label, value }: { label: string; value: string | number }) {
  return <div><dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</dt><dd className="mt-1 font-medium text-slate-900">{value}</dd></div>;
}

export function RepositoryOverview({ result }: { result: AnalysisResponse }) {
  const { metadata, languages, structure, technology_signals, evidence, engineering_review, health, intelligence } = result.analysis;
  const updatedAt = new Intl.DateTimeFormat("en", { dateStyle: "medium", timeStyle: "short" }).format(new Date(metadata.last_updated_at));

  return (
    <section aria-live="polite" className="mt-6 rounded-2xl border border-emerald-200 bg-white p-6 text-left shadow-lg shadow-emerald-950/5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-start"><div><p className="text-sm font-semibold uppercase tracking-widest text-emerald-700">Inspection complete</p><h2 className="mt-2 text-2xl font-bold text-slate-950">{result.owner}/{result.repository}</h2></div><span className="w-fit rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">Public repository</span></div>
      {metadata.description ? <p className="mt-4 text-sm leading-6 text-slate-600">{metadata.description}</p> : null}
      <a className="mt-3 inline-block break-all text-sm font-medium text-blue-700 hover:underline" href={result.repository_url} rel="noreferrer" target="_blank">{result.repository_url}</a>
      <dl className="mt-6 grid gap-4 rounded-xl bg-slate-50 p-4 sm:grid-cols-2 lg:grid-cols-4"><Detail label="Default branch" value={metadata.default_branch} /><Detail label="Stars" value={metadata.stargazers_count.toLocaleString()} /><Detail label="Forks" value={metadata.forks_count.toLocaleString()} /><Detail label="Watchers" value={metadata.watchers_count.toLocaleString()} /><Detail label="Last updated" value={updatedAt} /><Detail label="License" value={metadata.license ?? "Not specified"} /><Detail label="README" value={structure.has_readme ? "Detected" : "Not detected"} /><Detail label="Status" value={metadata.is_archived ? "Archived" : "Active"} /></dl>
      <RepositoryHealth health={health} />
      <RepositoryIntelligence intelligence={intelligence} />
      {metadata.topics.length ? <section className="mt-6"><h3 className="text-sm font-semibold text-slate-900">Topics</h3><div className="mt-3 flex flex-wrap gap-2">{metadata.topics.map((topic) => <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700" key={topic}>{topic}</span>)}</div></section> : null}
      <section className="mt-6"><h3 className="text-sm font-semibold text-slate-900">Languages</h3>{languages.length ? <div className="mt-3 space-y-3">{languages.map((language) => <div key={language.name}><div className="flex justify-between gap-4 text-sm"><span className="font-medium text-slate-700">{language.name}</span><span className="text-slate-500">{language.percentage}%</span></div><div className="mt-1 h-2 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-blue-600" style={{ width: `${language.percentage}%` }} /></div></div>)}</div> : <p className="mt-2 text-sm text-slate-500">GitHub did not report language data for this repository.</p>}</section>
      <section className="mt-6 grid gap-6 sm:grid-cols-2"><div><h3 className="text-sm font-semibold text-slate-900">Technology signals</h3>{technology_signals.length ? <ul className="mt-3 space-y-2">{technology_signals.map((signal) => <li className="rounded-lg bg-slate-50 px-3 py-2 text-sm text-slate-700" key={signal.file_name}><span className="font-medium">{signal.file_name}</span><span className="text-slate-500"> - {signal.label}</span></li>)}</ul> : <p className="mt-2 text-sm text-slate-500">No recognized root-level configuration files were detected.</p>}</div><div><h3 className="text-sm font-semibold text-slate-900">Root structure</h3><p className="mt-2 text-xs font-semibold uppercase tracking-wide text-slate-500">Directories</p><p className="mt-1 text-sm text-slate-700">{structure.root_directories.join(", ") || "None"}</p><p className="mt-3 text-xs font-semibold uppercase tracking-wide text-slate-500">Files</p><p className="mt-1 text-sm text-slate-700">{structure.root_files.join(", ") || "None"}</p></div></section>
      <section className="mt-8 border-t border-slate-200 pt-6"><div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-end"><div><p className="text-sm font-semibold uppercase tracking-widest text-blue-700">Engineering review</p><h3 className="mt-1 text-xl font-bold text-slate-950">Evidence-backed findings</h3></div><p className="text-xs text-slate-500">{evidence.files.length} files collected{evidence.tree_was_truncated ? "; tree limited by GitHub" : ""}</p></div><div className="mt-5 rounded-xl bg-blue-50 p-4"><p className="text-sm font-medium text-slate-900">{engineering_review.architecture_summary}</p><EvidencePaths paths={engineering_review.architecture_evidence_paths} /></div>{engineering_review.technology_stack.length ? <div className="mt-4"><p className="text-sm font-semibold text-slate-900">Observed technology stack</p><div className="mt-2 flex flex-wrap gap-2">{engineering_review.technology_stack.map((technology) => <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700" key={technology}>{technology}</span>)}</div><EvidencePaths paths={engineering_review.technology_stack_evidence_paths} /></div> : null}<div className="mt-5 space-y-3">{engineering_review.findings.map((finding) => <article className="rounded-xl border border-slate-200 bg-white p-4" key={`${finding.category}-${finding.title}`}><div className="flex flex-wrap items-center gap-2"><span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold uppercase tracking-wide text-slate-600">{finding.category.replace("_", " ")}</span><span className="text-xs font-semibold text-slate-500">{finding.severity}</span></div><h4 className="mt-3 font-semibold text-slate-900">{finding.title}</h4><p className="mt-1 text-sm leading-6 text-slate-600">{finding.detail}</p>{finding.recommendation ? <p className="mt-3 rounded-lg bg-amber-50 px-3 py-2 text-sm text-amber-900"><span className="font-semibold">Recommendation{finding.priority ? ` ${finding.priority}` : ""}:</span> {finding.recommendation}</p> : null}<EvidencePaths paths={finding.evidence_paths} /></article>)}</div></section>
    </section>
  );
}

function EvidencePaths({ paths }: { paths: string[] }) {
  return <p className="mt-3 text-xs text-slate-500"><span className="font-semibold">Evidence:</span> {paths.join(", ")}</p>;
}

function RepositoryHealth({ health }: { health: AnalysisResponse["analysis"]["health"] }) {
  const labelClasses = { Excellent: "bg-emerald-100 text-emerald-800", Good: "bg-blue-100 text-blue-800", Fair: "bg-amber-100 text-amber-800", "Needs Improvement": "bg-rose-100 text-rose-800" }[health.label];

  return (
    <section className="mt-8 overflow-hidden rounded-2xl border border-slate-200 bg-slate-950 p-6 text-white shadow-xl shadow-slate-950/10"><div className="flex flex-col gap-6 lg:flex-row lg:items-center"><div className="flex shrink-0 items-center gap-5"><div className="grid h-28 w-28 place-items-center rounded-full border-8 border-blue-400 bg-slate-900 shadow-inner shadow-blue-300/20"><div className="text-center"><span className="block text-4xl font-bold tracking-tight">{health.overall_score}</span><span className="text-xs font-semibold uppercase tracking-wider text-slate-400">out of 100</span></div></div><div><p className="text-sm font-semibold uppercase tracking-widest text-blue-300">Repository health</p><h3 className="mt-1 text-2xl font-bold">Engineering readiness</h3><span className={`mt-3 inline-block rounded-full px-3 py-1 text-xs font-bold ${labelClasses}`}>{health.label}</span></div></div><p className="max-w-xl text-sm leading-6 text-slate-300">A transparent weighted score from repository evidence only. Each category below links the score to the collected paths that support it.</p></div><div className="mt-7 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{health.categories.map((category) => <article className="rounded-xl border border-white/10 bg-white/5 p-4" key={category.name}><div className="flex items-baseline justify-between gap-3"><h4 className="font-semibold text-white">{category.name}</h4><span className="text-lg font-bold text-blue-300">{category.score}</span></div><p className="mt-1 text-xs text-slate-400">{category.weight}% of overall score</p><div className="mt-3 h-2 overflow-hidden rounded-full bg-white/10"><div className="h-full rounded-full bg-blue-400" style={{ width: `${category.score}%` }} /></div><p className="mt-3 text-xs leading-5 text-slate-300">{category.explanation}</p><EvidencePaths paths={category.evidence_paths} /></article>)}</div><div className="mt-6 grid gap-4 lg:grid-cols-2"><HealthHighlights title="Top strengths" highlights={health.top_strengths} tone="strength" /><HealthHighlights title="Highest-priority improvements" highlights={health.highest_priority_improvements} tone="improvement" /></div></section>
  );
}

function HealthHighlights({ title, highlights, tone }: { title: string; highlights: AnalysisResponse["analysis"]["health"]["top_strengths"]; tone: "strength" | "improvement" }) {
  return <div className={`rounded-xl p-4 ${tone === "strength" ? "bg-emerald-400/10" : "bg-amber-400/10"}`}><h4 className="font-semibold text-white">{title}</h4>{highlights.length ? <div className="mt-3 space-y-3">{highlights.map((highlight) => <div key={`${highlight.category}-${highlight.title}`}><p className="text-sm font-semibold text-slate-100">{highlight.title}</p><p className="mt-1 text-xs leading-5 text-slate-300">{highlight.detail}</p><EvidencePaths paths={highlight.evidence_paths} /></div>)}</div> : <p className="mt-3 text-sm text-slate-300">No improvement is currently flagged by this evidence-based score.</p>}</div>;
}

type IntelligenceItem = AnalysisResponse["analysis"]["intelligence"]["documentation"][number];

function RepositoryIntelligence({ intelligence }: { intelligence: AnalysisResponse["analysis"]["intelligence"] }) {
  return (
    <section className="mt-8 rounded-2xl border border-violet-200 bg-gradient-to-br from-violet-50 via-white to-blue-50 p-6 shadow-lg shadow-violet-950/5"><div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between"><div><p className="text-sm font-semibold uppercase tracking-widest text-violet-700">Repository intelligence</p><h3 className="mt-1 text-2xl font-bold text-slate-950">What the evidence means</h3></div><p className="max-w-md text-sm leading-6 text-slate-600">A deterministic engineering read of the README, workflows, configuration, structure, and health evidence.</p></div><article className="mt-6 rounded-xl border border-violet-200 bg-white p-5"><p className="text-xs font-semibold uppercase tracking-widest text-violet-700">Likely project type</p><h4 className="mt-2 text-xl font-bold text-slate-950">{intelligence.project_type.project_type}</h4><p className="mt-2 text-sm leading-6 text-slate-600">{intelligence.project_type.detail}</p><EvidencePaths paths={intelligence.project_type.evidence_paths} /></article><div className="mt-5 grid gap-5 lg:grid-cols-2"><IntelligenceGroup title="Documentation quality" insights={intelligence.documentation} /><IntelligenceGroup title="Development workflow" insights={intelligence.development_workflow} /><IntelligenceGroup title="Technology understanding" insights={intelligence.technology_understanding} /><IntelligenceGroup title="Verified best practices" insights={intelligence.best_practices} /></div></section>
  );
}

function IntelligenceGroup({ title, insights }: { title: string; insights: IntelligenceItem[] }) {
  return <article className="rounded-xl border border-slate-200 bg-white p-5"><h4 className="font-semibold text-slate-950">{title}</h4><div className="mt-4 space-y-4">{insights.map((insight) => <div key={`${insight.title}-${insight.status}`}><div className="flex flex-wrap items-center gap-2"><p className="text-sm font-semibold text-slate-800">{insight.title}</p><InsightStatus status={insight.status} /></div><p className="mt-1 text-sm leading-6 text-slate-600">{insight.detail}</p><EvidencePaths paths={insight.evidence_paths} /></div>)}</div></article>;
}

function InsightStatus({ status }: { status: string }) {
  const classes = status === "present" || status === "detected" ? "bg-emerald-100 text-emerald-800" : status === "partial" ? "bg-amber-100 text-amber-800" : "bg-slate-100 text-slate-600";
  return <span className={`rounded-full px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide ${classes}`}>{status.replaceAll("_", " ")}</span>;
}
