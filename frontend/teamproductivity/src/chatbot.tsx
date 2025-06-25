import axios from "axios";
import { useState } from "react";

type Message = [sender: "You" | "Bot", content: string];

export default function Chatbot({ onClose }: { onClose: () => void }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;
    console.log(input,input[0])
    const updated: Message[] = [...messages, ["You", input]];
    setMessages(updated);
    setInput("");

    const query = { user_query: input };

    try {
      const res = await axios.post(`${import.meta.env.VITE_CHATBOT_API}`, query);
      const botMessage: Message = ["Bot", res.data.response];
      setMessages([...updated, botMessage]);
    } catch (error) {
      setMessages([...updated, ["Bot", "Error responding to your query."]]);
    }
  };

  return (
    <div className="fixed right-4 bottom-4 w-[320px] h-[400px] bg-white border border-gray-300 rounded-xl shadow-lg flex flex-col z-50">
      {/* Header */}
      <div className="bg-indigo-600 text-white text-sm font-medium px-4 py-2 rounded-t-xl flex justify-between items-center">
        <span>🧠 Team Assistant</span>
        <button onClick={onClose} className="text-white text-lg font-bold leading-none hover:text-gray-200">
          ×
        </button>
      </div>

      {/* Message area */}
      <div className="flex flex-col h-[300px] overflow-y-auto px-3 py-2 text-sm space-y-1">
        {messages.map((msg: Message, idx: number) => (
          <div
            key={idx}
            className={`
              max-w-[70%]
              p-2 rounded
              ${msg[0] === "Bot" ? "bg-gray-100 self-start text-black" : "bg-purple-500 self-end text-white"}
            `}
          >
            <p>{msg[1]}</p>
          </div>
        ))}
      </div>

      {/* Input box */}
      <div className="flex items-center border-t px-2 py-2">
        <input
          className="flex-1 text-sm px-2 py-1 border rounded mr-2"
          placeholder="Ask your query..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button
          onClick={handleSend}
          className="bg-indigo-600 text-white text-sm px-3 py-1 rounded"
        >
          Send
        </button>
      </div>
    </div>
  );
}
