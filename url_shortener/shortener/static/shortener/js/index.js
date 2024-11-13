import React from "react";
import { createRoot } from "react-dom/client";
import URLShortener from "./components/URLShortener";

const container = document.getElementById("react-app");
const root = createRoot(container);
root.render(<URLShortener />);
