export type GeolocationState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "granted"; latitude: number; longitude: number }
  | { status: "denied" }
  | { status: "unavailable" }
  | { status: "error"; message: string };
