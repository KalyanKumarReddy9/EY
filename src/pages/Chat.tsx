import { useState, useRef } from "react";
import { Sidebar } from "@/components/Sidebar";
import { MobileHeader } from "@/components/MobileHeader";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Mic, MicOff, Send, Bot, User, FileText } from "lucide-react";
import { agents as allAgents } from "./Agents";
import { useToast } from "@/hooks/use-toast";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string | Record<string, any>;
  timestamp: Date;
}

export default function Chat() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content:
        "Hello! I'm your Pharma AI Research assistant. I can help you interact with the site's worker agents (Market Insights, Trade Data, Clinical Trials, Patent & IP, Safety Signal, Regulatory Monitor, Supply Chain Risk, Clinical Evidence Summarizer). Ask about an agent or paste a document to start.",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [lastQuery, setLastQuery] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const currentInput = input;
    setInput("");
    setIsLoading(true);
    setLastQuery(currentInput);

    try {
      const endpoints = [
        'clinical-trials',
        'patents',
        'pubmed',
        'web-search',
        'openfda',
        'exim'
      ];
      const promises = endpoints.map(endpoint =>
        fetch(`http://localhost:4000/api/${endpoint}?query=${currentInput}`)
          .then(res => {
            if (!res.ok) {
              return res.json().then(err => { throw new Error(err.msg || `API Error on ${endpoint}`) });
            }
            return res.json();
          })
      );
      
      const responses = await Promise.allSettled(promises);
      const newResults = {};
      let hasResults = false;

      responses.forEach((result, i) => {
        const endpoint = endpoints[i];
        const key = endpoint.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase());
        if (result.status === 'fulfilled' && result.value) {
          newResults[key] = result.value;
          hasResults = true;
        } else if (result.status === 'rejected') {
          newResults[key] = { error: 'Failed to fetch' };
          console.error(`Failed to fetch from ${endpoint}:`, result.reason);
        }
      });

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: hasResults ? newResults : "Not found",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);

    } catch (error) {
      console.error("Error fetching search results:", error);
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Not found",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    const lastMessage = messages[messages.length - 1];
    if (!lastMessage || lastMessage.role !== 'assistant' || typeof lastMessage.content === 'string') {
      toast({ title: "No results to generate a report from.", variant: "destructive" });
      return;
    }

    setIsLoading(true);
    try {
      const res = await fetch('http://localhost:4000/api/generate-report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: lastQuery, results: lastMessage.content })
      });

      if (!res.ok) {
        throw new Error('Failed to generate report');
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'report.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();

    } catch (error) {
      console.error("Error generating report:", error);
      toast({ title: "Error generating report.", variant: "destructive" });
    } finally {
      setIsLoading(false);
    }
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
        <div className="border-b border-border bg-card/50 backdrop-blur-sm px-4 md:px-6 py-3 md:py-4 shadow-sm">
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
                  {message.role === "user" ? <User size={20} /> : <Bot size={20} />}
                </div>
                <Card
                  className={`max-w-[85%] rounded-2xl ${
                    message.role === "user"
                      ? "rounded-br-none bg-primary text-primary-foreground"
                      : "rounded-bl-none"
                  }`}
                >
                  <CardContent className="p-3 md:p-4 text-sm md:text-base">
                    {typeof message.content === 'string' ? (
                      <p>{message.content}</p>
                    ) : (
                      <div>
                        <div className="flex justify-between items-center">
                          <h3 className="font-bold mb-2">Agentic Search Results:</h3>
                          <Button size="sm" onClick={handleGenerateReport} disabled={isLoading}>
                            <FileText className="h-4 w-4 mr-2" />
                            Generate Report
                          </Button>
                        </div>
                        {Object.entries(message.content).map(([key, value]) => (
                          <details key={key} className="mb-2">
                            <summary className="font-semibold cursor-pointer">{key}</summary>
                            <pre className="overflow-x-auto bg-gray-100 p-2 rounded mt-1 text-xs">
                              {JSON.stringify(value, null, 2)}
                            </pre>
                          </details>
                        ))}
                      </div>
                    )}
                    <p className="mt-2 text-xs text-right opacity-70">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </CardContent>
                </Card>
              </div>
            ))}
            {isLoading && (
              <div className="flex gap-2 md:gap-4">
                <div className="flex h-8 w-8 md:h-10 md:w-10 shrink-0 items-center justify-center rounded-full bg-muted text-muted-foreground">
                  <Bot size={20} />
                </div>
                <Card className="max-w-[85%] rounded-2xl rounded-bl-none">
                  <CardContent className="p-3 md:p-4 text-sm md:text-base">
                    <p>Searching...</p>
                  </CardContent>
                </Card>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input */}
        <div className="border-t border-border bg-card/70 p-3 md:p-4">
          <div className="mx-auto max-w-3xl">
            <div className="relative">
              <Input
                placeholder="Ask about a molecule, disease, or patent..."
                className="pr-24 md:pr-28"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                disabled={isLoading}
              />
              <div className="absolute inset-y-0 right-2 flex items-center gap-1">
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={toggleRecording}
                  className="text-muted-foreground"
                  disabled={isLoading}
                >
                  {isRecording ? (
                    <MicOff className="h-5 w-5" />
                  ) : (
                    <Mic className="h-5 w-5" />
                  )}
                </Button>
                <Button size="icon" onClick={handleSend} disabled={isLoading}>
                  <Send className="h-5 w-5" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
