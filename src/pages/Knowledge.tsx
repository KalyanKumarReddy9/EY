import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Upload, FileText, MessageSquare, Send, X } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface Document {
  id: string;
  name: string;
  size: string;
  uploadedAt: Date;
}

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export default function Knowledge() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState("");
  const { toast } = useToast();

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    const newDocs: Document[] = Array.from(files).map((file) => ({
      id: Date.now().toString() + Math.random(),
      name: file.name,
      size: `${(file.size / 1024).toFixed(1)} KB`,
      uploadedAt: new Date(),
    }));

    setDocuments((prev) => [...prev, ...newDocs]);
    toast({
      title: "Documents Uploaded",
      description: `Successfully uploaded ${files.length} document(s)`,
    });
  };

  const openDocumentChat = (doc: Document) => {
    setSelectedDoc(doc);
    setChatMessages([
      {
        id: "1",
        role: "assistant",
        content: `I've analyzed "${doc.name}". Ask me anything about this document!`,
      },
    ]);
  };

  const sendChatMessage = () => {
    if (!chatInput.trim()) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: chatInput,
    };

    setChatMessages((prev) => [...prev, userMsg]);
    setChatInput("");

    // Simulate AI response
    setTimeout(() => {
      const aiMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Based on the document, here are the key insights related to your question...",
      };
      setChatMessages((prev) => [...prev, aiMsg]);
    }, 1000);
  };

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />
      
      <main className="ml-64 flex-1">
        <div className="container max-w-7xl py-8">
          <div className="mb-8">
            <h1 className="mb-2 text-3xl font-bold text-foreground">Knowledge Base</h1>
            <p className="text-muted-foreground">
              Upload documents and chat with your research files
            </p>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            {/* Upload Section */}
            <Card className="shadow-card">
              <CardHeader>
                <CardTitle>Upload Documents</CardTitle>
                <CardDescription>
                  Upload pharmaceutical research papers, reports, and data files
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <label className="flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-border bg-muted/30 p-12 transition-colors hover:bg-muted/50">
                  <Upload className="mb-4 h-12 w-12 text-muted-foreground" />
                  <p className="mb-2 text-sm font-medium text-foreground">
                    Click to upload files
                  </p>
                  <p className="text-xs text-muted-foreground">
                    PDF, DOCX, TXT up to 10MB
                  </p>
                  <input
                    type="file"
                    multiple
                    accept=".pdf,.doc,.docx,.txt"
                    onChange={handleFileUpload}
                    className="hidden"
                  />
                </label>

                {documents.length > 0 && (
                  <div className="space-y-2">
                    <h3 className="text-sm font-medium text-foreground">
                      Uploaded Documents
                    </h3>
                    <div className="space-y-2">
                      {documents.map((doc) => (
                        <div
                          key={doc.id}
                          className="flex items-center justify-between rounded-lg border border-border bg-card p-3"
                        >
                          <div className="flex items-center gap-3">
                            <FileText className="h-5 w-5 text-primary" />
                            <div>
                              <p className="text-sm font-medium text-foreground">
                                {doc.name}
                              </p>
                              <p className="text-xs text-muted-foreground">
                                {doc.size}
                              </p>
                            </div>
                          </div>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => openDocumentChat(doc)}
                          >
                            <MessageSquare className="h-4 w-4" />
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Chat Section */}
            <Card className="shadow-card">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Document Chat</CardTitle>
                    <CardDescription>
                      {selectedDoc
                        ? `Chatting with: ${selectedDoc.name}`
                        : "Select a document to start chatting"}
                    </CardDescription>
                  </div>
                  {selectedDoc && (
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => {
                        setSelectedDoc(null);
                        setChatMessages([]);
                      }}
                    >
                      <X className="h-5 w-5" />
                    </Button>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                {selectedDoc ? (
                  <div className="space-y-4">
                    {/* Chat Messages */}
                    <div className="h-96 space-y-4 overflow-y-auto rounded-lg border border-border bg-muted/20 p-4">
                      {chatMessages.map((msg) => (
                        <div
                          key={msg.id}
                          className={`flex ${
                            msg.role === "user" ? "justify-end" : "justify-start"
                          }`}
                        >
                          <div
                            className={`max-w-[80%] rounded-lg p-3 ${
                              msg.role === "user"
                                ? "bg-primary text-primary-foreground"
                                : "bg-card text-foreground"
                            }`}
                          >
                            <p className="text-sm">{msg.content}</p>
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Chat Input */}
                    <div className="flex gap-2">
                      <Input
                        value={chatInput}
                        onChange={(e) => setChatInput(e.target.value)}
                        onKeyPress={(e) => e.key === "Enter" && sendChatMessage()}
                        placeholder="Ask about this document..."
                        className="bg-input"
                      />
                      <Button onClick={sendChatMessage} size="icon">
                        <Send className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="flex h-96 items-center justify-center rounded-lg border border-dashed border-border bg-muted/20">
                    <div className="text-center">
                      <MessageSquare className="mx-auto mb-4 h-12 w-12 text-muted-foreground" />
                      <p className="text-sm text-muted-foreground">
                        Upload and select a document to start chatting
                      </p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
