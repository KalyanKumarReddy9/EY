import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { MobileHeader } from "@/components/MobileHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Upload, FileText, Send, X, Bot, User as UserIcon } from "lucide-react";
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
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [documents, setDocuments] = useState<Document[]>([]);
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

    // Initialize chat when first document is uploaded
    if (documents.length === 0) {
      setChatMessages([
        {
          id: "1",
          role: "assistant",
          content: `I've analyzed your documents. Ask me anything about them!`,
        },
      ]);
    }
  };

  const removeDocument = (id: string) => {
    setDocuments((prev) => prev.filter((doc) => doc.id !== id));
    toast({
      title: "Document Removed",
      description: "Document has been removed from knowledge base",
    });
  };

  const sendChatMessage = () => {
    if (!chatInput.trim()) return;
    if (documents.length === 0) {
      toast({
        title: "No Documents",
        description: "Please upload documents first to start chatting",
        variant: "destructive",
      });
      return;
    }

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
        content: "Based on your uploaded documents, here are the key insights related to your question...",
      };
      setChatMessages((prev) => [...prev, aiMsg]);
    }, 1000);
  };

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <MobileHeader onMenuClick={() => setSidebarOpen(true)} />
      
      <main className="flex-1 md:ml-64 pt-14 md:pt-0">
        <div className="container max-w-5xl mx-auto py-4 md:py-8 px-4">
          <div className="mb-6 md:mb-8">
            <h1 className="mb-2 text-2xl md:text-3xl font-bold text-foreground">Knowledge Base</h1>
            <p className="text-sm md:text-base text-muted-foreground">
              Upload documents and chat with your research files using AI
            </p>
          </div>

          {/* Upload Section - Compact */}
          <div className="mb-6 grid gap-4 md:grid-cols-2">
            <Card className="shadow-card border-border/50 hover:shadow-elevated transition-all duration-300">
              <CardHeader className="pb-3">
                <CardTitle className="text-base md:text-lg">Upload Documents</CardTitle>
                <CardDescription className="text-xs">
                  PDF, DOCX, TXT files
                </CardDescription>
              </CardHeader>
              <CardContent>
                <label className="flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-primary/30 bg-gradient-to-br from-primary/5 to-transparent hover:from-primary/10 hover:border-primary/50 p-6 transition-all duration-300 group">
                  <Upload className="mb-2 h-8 w-8 text-primary group-hover:scale-110 transition-transform duration-300" />
                  <p className="mb-1 text-sm font-semibold text-foreground">
                    Click to upload
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Max 10MB
                  </p>
                  <input
                    type="file"
                    multiple
                    accept=".pdf,.doc,.docx,.txt"
                    onChange={handleFileUpload}
                    className="hidden"
                  />
                </label>
              </CardContent>
            </Card>

            {/* Uploaded Documents List */}
            <Card className="shadow-card border-border/50">
              <CardHeader className="pb-3">
                <CardTitle className="text-base md:text-lg flex items-center gap-2">
                  <FileText className="h-4 w-4 text-primary" />
                  Documents ({documents.length})
                </CardTitle>
                <CardDescription className="text-xs">
                  {documents.length > 0 ? "Your uploaded files" : "No files yet"}
                </CardDescription>
              </CardHeader>
              <CardContent>
                {documents.length > 0 ? (
                  <div className="max-h-[200px] overflow-y-auto space-y-2 pr-2">
                    {documents.map((doc) => (
                      <div
                        key={doc.id}
                        className="flex items-center justify-between rounded-lg border border-border bg-card/50 p-2.5 hover:bg-card transition-all duration-200 group"
                      >
                        <div className="flex items-center gap-2 min-w-0 flex-1">
                          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-gradient-to-br from-primary/10 to-primary/5 flex-shrink-0">
                            <FileText className="h-4 w-4 text-primary" />
                          </div>
                          <div className="min-w-0 flex-1">
                            <p className="text-sm font-medium text-foreground truncate">
                              {doc.name}
                            </p>
                            <p className="text-xs text-muted-foreground">
                              {doc.size}
                            </p>
                          </div>
                        </div>
                        <Button
                          size="icon"
                          variant="ghost"
                          onClick={() => removeDocument(doc.id)}
                          className="flex-shrink-0 h-7 w-7 text-destructive hover:bg-destructive/10 hover:text-destructive"
                        >
                          <X className="h-3.5 w-3.5" />
                        </Button>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="flex h-[200px] items-center justify-center rounded-lg border-2 border-dashed border-border bg-muted/10">
                    <p className="text-xs text-muted-foreground">Upload files to see them here</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Chat Section - Bottom with fixed input */}
          <Card className="shadow-card border-border/50">
            <CardHeader className="pb-3">
              <CardTitle className="text-base md:text-lg">Chat with Documents</CardTitle>
              <CardDescription className="text-xs">
                {documents.length > 0
                  ? `Ask questions about your ${documents.length} uploaded document${documents.length > 1 ? 's' : ''}`
                  : "Upload documents to start chatting"}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {documents.length > 0 ? (
                <>
                  {/* Chat Messages */}
                  <div className="h-80 md:h-96 space-y-3 overflow-y-auto rounded-lg border border-border bg-muted/20 p-3 md:p-4">
                    {chatMessages.map((msg) => (
                      <div
                        key={msg.id}
                        className={`flex gap-2.5 ${
                          msg.role === "user" ? "justify-end" : "justify-start"
                        }`}
                      >
                        {msg.role === "assistant" && (
                          <div className="flex h-7 w-7 items-center justify-center rounded-full bg-gradient-medical flex-shrink-0">
                            <Bot className="h-3.5 w-3.5 text-primary-foreground" />
                          </div>
                        )}
                        <div
                          className={`max-w-[75%] rounded-lg p-2.5 md:p-3 shadow-sm ${
                            msg.role === "user"
                              ? "bg-gradient-medical text-primary-foreground"
                              : "bg-card border border-border"
                          }`}
                        >
                          <p className="text-xs md:text-sm break-words leading-relaxed">{msg.content}</p>
                        </div>
                        {msg.role === "user" && (
                          <div className="flex h-7 w-7 items-center justify-center rounded-full bg-primary/10 flex-shrink-0">
                            <UserIcon className="h-3.5 w-3.5 text-primary" />
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <div className="flex h-80 md:h-96 items-center justify-center rounded-lg border-2 border-dashed border-border bg-muted/20">
                  <div className="text-center p-6">
                    <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary/10 to-primary/5">
                      <FileText className="h-6 w-6 text-primary" />
                    </div>
                    <p className="text-sm font-medium text-foreground mb-1.5">
                      No Documents Uploaded
                    </p>
                    <p className="text-xs text-muted-foreground max-w-xs mx-auto">
                      Upload documents above to start asking questions
                    </p>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Fixed Chat Input at Bottom */}
          {documents.length > 0 && (
            <div className="fixed bottom-0 left-0 right-0 md:left-64 border-t border-border bg-card/95 backdrop-blur-sm p-3 md:p-4 shadow-lg">
              <div className="container max-w-5xl mx-auto">
                <div className="flex gap-2">
                  <Input
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && sendChatMessage()}
                    placeholder="Ask about your documents..."
                    className="bg-input text-sm flex-1"
                  />
                  <Button 
                    onClick={sendChatMessage} 
                    size="icon" 
                    className="flex-shrink-0 h-10 w-10 bg-gradient-medical hover:opacity-90 transition-all"
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
