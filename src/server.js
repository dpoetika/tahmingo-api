import express from "express";
import cors from "cors";

import { ENV } from "./config/env.js";

import matchRouter from "./routes/matches.routes.js";

const app = express();

app.use(cors());
app.use(express.json());



app.get("/", (req, res) => res.send("Server is alive"));



// error handling middleware
app.use((err, req, res, next) => {
  console.error("Unhandled error:", err);
  res.status(500).json({ error: err.message || "Internal server error" });
});

app.use("/matches",matchRouter)

const startServer = async () => {
  try {
    if (ENV.NODE_ENV !== "production") {
      app.listen(ENV.PORT, () => console.log(`Server is up and running on PORT: http://localhost:${ENV.PORT}/`));
    }
  } catch (error) {
    console.error("Failed to start server:", error.message);
    process.exit(1);
  }
};

startServer();

// export for vercel
export default app;