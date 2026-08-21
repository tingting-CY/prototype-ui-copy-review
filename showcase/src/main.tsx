/** 校样工作台展示站入口。 */
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import Home from "./Home";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Home />
  </StrictMode>,
);
