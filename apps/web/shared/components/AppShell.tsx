import type { ReactNode } from "react";

import "../styles/app-shell.css";

type AppShellProps = {
  children: ReactNode;
};

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="app-shell">
      <header className="app-shell__header">
        <h1 className="app-shell__title">Area Todo</h1>
        <p className="app-shell__subtitle">
          Tasks sorted by where you are
        </p>
      </header>
      <main className="app-shell__main">{children}</main>
    </div>
  );
}
