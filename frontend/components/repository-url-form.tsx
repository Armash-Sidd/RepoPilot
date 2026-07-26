"use client";

import { FormEvent, useState } from "react";
import { ArrowRightIcon, GithubIcon } from "./icons";

const githubRepositoryPattern = /^https:\/\/(?:www\.)?github\.com\/[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})\/[A-Za-z0-9._-]+\/?$/;
const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

type AnalysisResponse = {
  success: true;
  owner: string;
  repository: string;
  repository_url: string;
};

type ApiValidationError = {
  detail?: string | Array<{ msg?: string }>;
};

function getUrlError(value: string): string | null {
  if (!value.trim()) return "Enter a public GitHub repository URL to continue.";
  if (!githubRepositoryPattern.test(value.trim())) return "Use a repository URL such as https://github.com/owner/repository.";
  return null;
}

export function RepositoryUrlForm() {
  const [url, setUrl] = useState("");
  const [touched, setTouched] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [submissionError, setSubmissionError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const error = getUrlError(url);
  const canSubmit = !error && !isLoading;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setTouched(true);
    if (!canSubmit) return;

    setIsLoading(true);
    setSubmissionError(null);
    setResult(null);

    try {
      const response = await fetch(`${apiBaseUrl}/api/analyze`, {
        body: JSON.stringify({ repository_url: url.trim() }),
        headers: { "Content-Type": "application/json" },
        method: "POST"
      });
      const body = (await response.json()) as AnalysisResponse | ApiValidationError;

      if (!response.ok) {
        const detail = (body as ApiValidationError).detail;
        const message = Array.isArray(detail) ? detail[0]?.msg : detail;
        throw new Error(message || "We could not validate that repository URL.");
      }

      setResult(body as AnalysisResponse);
    } catch (error) {
      setSubmissionError(error instanceof Error ? error.message : "We could not reach RepoPilot. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <form className="mx-auto mt-10 max-w-2xl" noValidate onSubmit={handleSubmit}>
      <label className="sr-only" htmlFor="repository-url">GitHub repository URL</label>
      <div className="rounded-2xl border border-blue-100 bg-white p-2 shadow-xl shadow-blue-950/10 sm:flex sm:gap-2">
        <div className="flex min-w-0 flex-1 items-center gap-3 px-3 py-3">
          <GithubIcon className="h-5 w-5 shrink-0 text-slate-400" />
          <input
            aria-describedby={touched && error ? "repository-url-error" : undefined}
            aria-invalid={touched && Boolean(error)}
            className="min-w-0 flex-1 bg-transparent text-sm text-slate-900 outline-none placeholder:text-slate-400 sm:text-base"
            id="repository-url"
            onBlur={() => setTouched(true)}
            onChange={(event) => setUrl(event.target.value)}
            placeholder="https://github.com/owner/repository"
            type="url"
            value={url}
          />
        </div>
        <button
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-200 disabled:cursor-not-allowed disabled:bg-slate-300 sm:w-auto"
          disabled={!canSubmit}
          type="submit"
        >
          {isLoading ? <><span className="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" /> Preparing analysis…</> : <>Analyze Repository <ArrowRightIcon className="h-4 w-4" /></>}
        </button>
      </div>
      {touched && error ? <p className="mt-3 text-left text-sm text-rose-600" id="repository-url-error" role="alert">{error}</p> : <p className="mt-3 text-left text-sm text-slate-500">Public GitHub repositories only. No code is executed.</p>}
      {submissionError ? <p className="mt-3 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-left text-sm text-rose-700" role="alert">{submissionError}</p> : null}
      {result ? (
        <section aria-live="polite" className="mt-6 rounded-2xl border border-emerald-200 bg-emerald-50 p-6 text-left shadow-sm">
          <p className="text-sm font-semibold uppercase tracking-widest text-emerald-700">Repository ready</p>
          <h2 className="mt-2 text-xl font-bold text-slate-950">Repository details</h2>
          <dl className="mt-5 grid gap-4 sm:grid-cols-3">
            <div><dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">Repository Owner</dt><dd className="mt-1 font-medium text-slate-900">{result.owner}</dd></div>
            <div><dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">Repository Name</dt><dd className="mt-1 font-medium text-slate-900">{result.repository}</dd></div>
            <div><dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">Repository URL</dt><dd className="mt-1 break-all font-medium text-blue-700"><a className="hover:underline" href={result.repository_url} rel="noreferrer" target="_blank">{result.repository_url}</a></dd></div>
          </dl>
        </section>
      ) : null}
    </form>
  );
}
