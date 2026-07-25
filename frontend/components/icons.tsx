import type { SVGProps } from "react";

type IconProps = SVGProps<SVGSVGElement>;

export function ArrowRightIcon(props: IconProps) {
  return <svg aria-hidden="true" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" {...props}><path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14m-6-6 6 6-6 6" /></svg>;
}

export function GithubIcon(props: IconProps) {
  return <svg aria-hidden="true" fill="currentColor" viewBox="0 0 24 24" {...props}><path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.18-3.37-1.18-.46-1.16-1.11-1.47-1.11-1.47-.9-.62.07-.61.07-.61 1 .07 1.52 1.02 1.52 1.02.89 1.52 2.32 1.08 2.89.82.09-.64.35-1.08.63-1.33-2.22-.25-4.56-1.11-4.56-4.94 0-1.09.39-1.98 1.02-2.68-.1-.25-.44-1.27.1-2.65 0 0 .84-.27 2.75 1.02A9.6 9.6 0 0 1 12 6.46c.85 0 1.7.11 2.5.34 1.91-1.3 2.75-1.02 2.75-1.02.54 1.38.2 2.4.1 2.65.63.7 1.02 1.59 1.02 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.9.68 1.82v2.68c0 .27.18.58.69.48A10 10 0 0 0 12 2Z" /></svg>;
}

export function SparkIcon(props: IconProps) {
  return <svg aria-hidden="true" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.8" {...props}><path strokeLinecap="round" strokeLinejoin="round" d="m12 3 1.48 5.52L19 10l-5.52 1.48L12 17l-1.48-5.52L5 10l5.52-1.48L12 3ZM19 16l.68 2.32L22 19l-2.32.68L19 22l-.68-2.32L16 19l2.32-.68L19 16Z" /></svg>;
}

