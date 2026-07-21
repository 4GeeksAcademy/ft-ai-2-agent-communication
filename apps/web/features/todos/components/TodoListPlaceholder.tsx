import "../styles/todo-list.css";

export function TodoListPlaceholder() {
  return (
    <section className="todo-list" aria-labelledby="todo-list-heading">
      <h2 id="todo-list-heading" className="todo-list__heading">
        Nearby tasks
      </h2>
      <p className="todo-list__empty">
        No tasks yet. Once you add todos, they will appear here sorted by
        proximity to your current location.
      </p>
      <button type="button" className="todo-list__hint" disabled>
        Add your first task
      </button>
    </section>
  );
}
