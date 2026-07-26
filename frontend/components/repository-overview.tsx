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
  };
};

function Detail({ label, value }: { label: string; value: string | number }) {
  return <div><dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</dt><dd className="mt-1 font-medium text-slate-900">{value}</dd></div>;
}

export function RepositoryOverview({ result }: { result: AnalysisResponse }) {
  const { metadata, languages, structure, technology_signals } = result.analysis;
  const updatedAt = new Intl.DateTimeFormat("en", { dateStyle: "medium", timeStyle: "short" }).format(new Date(metadata.last_updated_at));

  return (
    <section aria-live="polite" className="mt-6 rounded-2xl border border-emerald-200 bg-white p-6 text-left shadow-lg shadow-emerald-950/5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-start"><div><p className="text-sm font-semibold uppercase tracking-widest text-emerald-700">Inspection complete</p><h2 className="mt-2 text-2xl font-bold text-slate-950">{result.owner}/{result.repository}</h2></div><span className="w-fit rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">Public repository</span></div>
      {metadata.description ? <p className="mt-4 text-sm leading-6 text-slate-600">{metadata.description}</p> : null}
      <a className="mt-3 inline-block break-all text-sm font-medium text-blue-700 hover:underline" href={result.repository_url} rel="noreferrer" target="_blank">{result.repository_url}</a>
      <dl className="mt-6 grid gap-4 rounded-xl bg-slate-50 p-4 sm:grid-cols-2 lg:grid-cols-4"><Detail label="Default branch" value={metadata.default_branch} /><Detail label="Stars" value={metadata.stargazers_count.toLocaleString()} /><Detail label="Forks" value={metadata.forks_count.toLocaleString()} /><Detail label="Watchers" value={metadata.watchers_count.toLocaleString()} /><Detail label="Last updated" value={updatedAt} /><Detail label="License" value={metadata.license ?? "Not specified"} /><Detail label="README" value={structure.has_readme ? "Detected" : "Not detected"} /><Detail label="Status" value={metadata.is_archived ? "Archived" : "Active"} /></dl>
      {metadata.topics.length ? <section className="mt-6"><h3 className="text-sm font-semibold text-slate-900">Topics</h3><div className="mt-3 flex flex-wrap gap-2">{metadata.topics.map((topic) => <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700" key={topic}>{topic}</span>)}</div></section> : null}
      <section className="mt-6"><h3 className="text-sm font-semibold text-slate-900">Languages</h3>{languages.length ? <div className="mt-3 space-y-3">{languages.map((language) => <div key={language.name}><div className="flex justify-between gap-4 text-sm"><span className="font-medium text-slate-700">{language.name}</span><span className="text-slate-500">{language.percentage}%</span></div><div className="mt-1 h-2 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-blue-600" style={{ width: `${language.percentage}%` }} /></div></div>)}</div> : <p className="mt-2 text-sm text-slate-500">GitHub did not report language data for this repository.</p>}</section>
      <section className="mt-6 grid gap-6 sm:grid-cols-2"><div><h3 className="text-sm font-semibold text-slate-900">Technology signals</h3>{technology_signals.length ? <ul className="mt-3 space-y-2">{technology_signals.map((signal) => <li className="rounded-lg bg-slate-50 px-3 py-2 text-sm text-slate-700" key={signal.file_name}><span className="font-medium">{signal.file_name}</span><span className="text-slate-500"> - {signal.label}</span></li>)}</ul> : <p className="mt-2 text-sm text-slate-500">No recognized root-level configuration files were detected.</p>}</div><div><h3 className="text-sm font-semibold text-slate-900">Root structure</h3><p className="mt-2 text-xs font-semibold uppercase tracking-wide text-slate-500">Directories</p><p className="mt-1 text-sm text-slate-700">{structure.root_directories.join(", ") || "None"}</p><p className="mt-3 text-xs font-semibold uppercase tracking-wide text-slate-500">Files</p><p className="mt-1 text-sm text-slate-700">{structure.root_files.join(", ") || "None"}</p></div></section>
    </section>
  );
}
