"use client";

import { useGeolocation } from "../hooks/useGeolocation";
import type { GeolocationState } from "../types";
import "../styles/location-status.css";

type LocationMessage = {
  label: string;
  message: string;
  tone: string;
  showAction: boolean;
  actionLabel?: string;
};

function getLocationMessage(state: GeolocationState): LocationMessage {
  switch (state.status) {
    case "idle":
      return {
        label: "Location",
        message:
          "Enable location to see tasks sorted by proximity, or pin this session to a place later.",
        tone: "idle",
        showAction: true,
        actionLabel: "Use my location",
      };
    case "loading":
      return {
        label: "Location",
        message: "Checking your current location…",
        tone: "loading",
        showAction: false,
      };
    case "granted":
      return {
        label: "Location active",
        message: `Using ${state.latitude.toFixed(4)}, ${state.longitude.toFixed(4)} to sort nearby tasks.`,
        tone: "granted",
        showAction: false,
      };
    case "denied":
      return {
        label: "Location blocked",
        message:
          "Allow location access to see tasks near you, or pin this session to a place later.",
        tone: "denied",
        showAction: true,
        actionLabel: "Try again",
      };
    case "unavailable":
      return {
        label: "Location unavailable",
        message:
          "This device does not support geolocation. You can still browse all tasks.",
        tone: "unavailable",
        showAction: false,
      };
    case "error":
      return {
        label: "Location error",
        message: state.message,
        tone: "error",
        showAction: true,
        actionLabel: "Try again",
      };
  }
}

export function LocationStatusBanner() {
  const { state, requestLocation } = useGeolocation();
  const content = getLocationMessage(state);

  return (
    <section
      className={`location-status location-status--${content.tone}`}
      aria-live="polite"
    >
      <p className="location-status__label">{content.label}</p>
      <p className="location-status__message">{content.message}</p>
      {content.showAction ? (
        <button
          type="button"
          className="location-status__action"
          onClick={requestLocation}
        >
          {content.actionLabel ?? "Try again"}
        </button>
      ) : null}
    </section>
  );
}
