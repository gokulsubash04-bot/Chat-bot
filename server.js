const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

function detectIntent(message) {
  const text = message.toLowerCase();

  if (text.includes("hello") || text.includes("hi")) {
    return "greeting";
  }

  if (text.includes("bye")) {
    return "goodbye";
  }

  return "unknown";
}

function handleIntent(intent) {
  if (intent === "greeting") {
    return "Hello! How can I help you?";
  }

  if (intent === "goodbye") {
    return "Goodbye!";
  }

  return "I did not understand that.";
}

app.post("/chat", (req, res) => {
  const message = req.body.message;

  if (!message) {
    return res.status(400).json({ reply: "Message required." });
  }

  const intent = detectIntent(message);
  const reply = handleIntent(intent);

  res.json({ intent, reply });
});

app.listen(3000, () => {
  console.log("Chatbot running at http://localhost:3000");
});