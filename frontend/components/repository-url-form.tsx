"use client";

import { FormEvent, useState } from "react";
import { ArrowRightIcon, GithubIcon } from "./icons";

const githubRepositoryPattern = /^https:\/\/(?:www\.)?github\.com\/[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})\/[A-Za-z0-9._-]+\/?$/;

function getUrlError(value: string): string | null {
  if (!value.trim()) return "Enter a public GitHub repository URL to continue.";
  if (!githubRepositoryPattern.test(value.trim())) return "Use a repository URL such as https://github.com/owner/repository.";
  return null;
}

export function RepositoryUrlForm() {
  const [url, setUrl] = useState("");
  const [touched, setTouched] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const error = getUrlError(url);
  const canSubmit = !error && !isLoading;

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setTouched(true);
    if (!canSubmit) return;

    setIsLoading(true);
    // The backend integration is intentionally deferred to the next milestone.
    window.setTimeout(() => setIsLoading(false), 1200);
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
    </form>
  );
}

