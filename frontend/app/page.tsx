import { FeatureGrid } from "../components/feature-grid";
import { Hero } from "../components/hero";
import { Workflow } from "../components/workflow";

export default function HomePage() {
  return (
    <main>
      <Hero />
      <FeatureGrid />
      <Workflow />
    </main>
  );
}

