import { useState, useRef } from "react";
import { Sidebar } from "@/components/Sidebar";
import { MobileHeader } from "@/components/MobileHeader";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Mic, MicOff, Send, Bot, User } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function Chat() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hello! I'm your Pharma AI Research assistant. I can help you analyze market data, clinical trials, and trade information. How can I assist you today?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const { toast } = useToast();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "I've analyzed your query. Based on current pharmaceutical market trends and clinical trial data, here are some key insights...",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    }, 1000);
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    toast({
      title: isRecording ? "Recording Stopped" : "Recording Started",
      description: isRecording
        ? "Processing your audio message..."
        : "Speak now to send an audio message",
    });
  };

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <MobileHeader onMenuClick={() => setSidebarOpen(true)} />
      
      <main className="flex flex-1 flex-col md:ml-64 pt-14 md:pt-0">
        <div className="border-b border-border bg-card px-4 md:px-6 py-3 md:py-4">
          <h1 className="text-xl md:text-2xl font-bold text-foreground">AI Chat Assistant</h1>
          <p className="text-xs md:text-sm text-muted-foreground">
            Ask questions about pharmaceutical data, market insights, and research
          </p>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-3 md:p-6">
          <div className="mx-auto max-w-3xl space-y-4 md:space-y-6">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-2 md:gap-4 ${
                  message.role === "user" ? "flex-row-reverse" : ""
                }`}
              >
                <div
                  className={`flex h-8 w-8 md:h-10 md:w-10 shrink-0 items-center justify-center rounded-full ${
                    message.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-muted-foreground"
                  }`}
                >
                  {message.role === "user" ? (
                    <User className="h-4 w-4 md:h-5 md:w-5" />
                  ) : (
                    <Bot className="h-4 w-4 md:h-5 md:w-5" />
                  )}
                </div>
                <Card
                  className={`flex-1 shadow-soft ${
                    message.role === "user" ? "bg-primary/5" : ""
                  }`}
                >
                  <CardContent className="p-3 md:p-4">
                    <p className="text-xs md:text-sm leading-relaxed text-foreground break-words">
                      {message.content}
                    </p>
                    <p className="mt-1 md:mt-2 text-[10px] md:text-xs text-muted-foreground">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </CardContent>
                </Card>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="border-t border-border bg-card p-3 md:p-6">
          <div className="mx-auto max-w-3xl">
            <div className="flex gap-2 md:gap-3">
              <Button
                variant={isRecording ? "destructive" : "outline"}
                size="icon"
                onClick={toggleRecording}
                className="shrink-0 h-9 w-9 md:h-10 md:w-10"
              >
                {isRecording ? (
                  <MicOff className="h-4 w-4 md:h-5 md:w-5" />
                ) : (
                  <Mic className="h-4 w-4 md:h-5 md:w-5" />
                )}
              </Button>
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSend()}
                placeholder="Ask about pharmaceutical markets..."
                className="bg-input text-sm"
              />
              <Button onClick={handleSend} size="icon" className="shrink-0 h-9 w-9 md:h-10 md:w-10">
                <Send className="h-4 w-4 md:h-5 md:w-5" />
              </Button>
            </div>
            <p className="mt-2 text-[10px] md:text-xs text-muted-foreground text-center md:text-left">
              Click the microphone to send audio messages
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
