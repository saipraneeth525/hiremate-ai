import { useEffect, useRef, useState } from "react";
import { Send, Bot, User } from "lucide-react";

export default function ChatPanel({ sendMessage }) {
  const [input, setInput] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "👋 Hi! I'm HireMate AI Recruiter.\n\nAsk me anything about the uploaded candidates.",
    },
  ]);

  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      sender: "user",
      text: input,
    };

    setMessages((prev) => [...prev, userMessage]);

    const question = input;

    setInput("");

    setLoading(true);

    try {
      const response = await sendMessage(question);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: response,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Unable to contact backend.",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg h-[600px] flex flex-col">

      {/* Header */}

      <div className="border-b p-4">

        <h2 className="text-xl font-bold">
          AI Recruiter
        </h2>

        <p className="text-gray-500 text-sm">
          Ask questions about uploaded resumes
        </p>

      </div>

      {/* Messages */}

      <div className="flex-1 overflow-y-auto p-5 space-y-5">

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${
              msg.sender === "user"
                ? "justify-end"
                : "justify-start"
            }`}
          >
            <div
              className={`flex gap-3 max-w-[80%] ${
                msg.sender === "user"
                  ? "flex-row-reverse"
                  : ""
              }`}
            >
              <div className="mt-1">
                {msg.sender === "bot" ? (
                  <Bot className="text-indigo-600" />
                ) : (
                  <User className="text-green-600" />
                )}
              </div>

              <div
                className={`rounded-xl px-4 py-3 whitespace-pre-wrap ${
                  msg.sender === "bot"
                    ? "bg-gray-100"
                    : "bg-indigo-600 text-white"
                }`}
              >
                {msg.text}
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="text-gray-500">
            HireMate AI is thinking...
          </div>
        )}

        <div ref={bottomRef}></div>

      </div>

      {/* Input */}

      <div className="border-t p-4 flex gap-3">

        <input
          className="flex-1 border rounded-lg px-4 py-3 outline-none"
          placeholder="Ask about candidates..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) =>
            e.key === "Enter" && handleSend()
          }
        />

        <button
          onClick={handleSend}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 rounded-lg"
        >
          <Send />
        </button>

      </div>

    </div>
  );
}