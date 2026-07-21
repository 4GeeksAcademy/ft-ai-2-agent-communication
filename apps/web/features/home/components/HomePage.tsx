import { LocationStatusBanner } from "@/features/location/components/LocationStatusBanner";
import { TodoListPlaceholder } from "@/features/todos/components/TodoListPlaceholder";
import { AppShell } from "@/shared/components/AppShell";

import "../styles/home-page.css";

export function HomePage() {
  return (
    <AppShell>
      <div className="home-page">
        <section className="home-page__intro">
          <h2 className="home-page__intro-title">Welcome back</h2>
          <p className="home-page__intro-copy">
            Area Todo helps you remember what to do when you arrive somewhere.
            Start by enabling location, then add tasks tied to places that
            matter.
          </p>
        </section>

        <LocationStatusBanner />
        <TodoListPlaceholder />
      </div>
    </AppShell>
  );
}
