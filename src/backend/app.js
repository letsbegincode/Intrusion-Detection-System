
const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
const PORT = process.env.PORT || 5000;


// Middleware
app.use(cors());
app.use(bodyParser.json());

// Dummy API Routes
app.get("/", (req, res) => {
  res.send({ message: "Welcome to the test API!" });
});

app.get("/api/hello", (req, res) => {
  res.json({ message: "Hello, World!" });
});

app.post("/api/data", (req, res) => {
  const { name, age } = req.body;
  res.json({ message: `Received data for ${name}, age ${age}` });
});

// Start Server
app.listen(PORT, () => {
  console.log(` server statrted , Server is running on port ${PORT}`);
});
