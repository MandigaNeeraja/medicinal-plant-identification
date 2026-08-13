import { useEffect, useRef, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import api, { getErrorMessage } from '../api/client';

export default function Chat() {
  const { name } = useParams();
  const [messages, setMessages] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    async function initChat() {
      setLoading(true);
      try {
        const [historyRes, initRes] = await Promise.all([
          api.get(`/chat/history/${encodeURIComponent(name)}`),
          api.post('/chat/init', { plant_name: name }),
        ]);

        const historyMessages = historyRes.data.data?.messages || [];
        if (historyMessages.length > 0) {
          setMessages(historyMessages);
        } else {
          setMessages([
            {
              role: 'assistant',
              content: initRes.data.data?.message || `Chat initialized for ${name}.`,
            },
          ]);
        }
        setSuggestions(initRes.data.data?.suggestions || []);
      } catch (error) {
        toast.error(getErrorMessage(error));
      } finally {
        setLoading(false);
      }
    }

    initChat();
  }, [name]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sending]);

  const sendMessage = async (text) => {
    const question = (text || input).trim();
    if (!question || sending) return;

    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: question }]);
    setSending(true);

    try {
      const response = await api.post('/chat/message', {
        plant_name: name,
        message: question,
      });
      const answer = response.data.data?.answer || 'No response received.';
      setMessages((prev) => [...prev, { role: 'assistant', content: answer }]);
      setSuggestions(response.data.data?.suggestions || []);
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setSending(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-purple-500/30 border-t-purple-400" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <section className="card flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold gradient-text">Chat about {name}</h1>
          <p className="mt-1 text-white/60">Ask questions about medicinal uses, preparation, and safety.</p>
        </div>
        <Link to={`/plant/${name}`} className="btn-secondary">
          View plant details
        </Link>
      </section>

      <section className="card flex h-[60vh] flex-col">
        <div className="flex-1 space-y-4 overflow-y-auto pr-2">
          {messages.map((message, index) => (
            <div
              key={`${message.role}-${index}`}
              className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm whitespace-pre-wrap ${
                message.role === 'user'
                  ? 'ml-auto bg-purple-600/30 text-white'
                  : 'bg-white/10 text-white/90'
              }`}
            >
              {message.content}
            </div>
          ))}
          {sending && (
            <div className="max-w-[85%] rounded-2xl bg-white/10 px-4 py-3 text-sm text-white/70">
              Thinking...
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {suggestions.length > 0 && (
          <div className="mt-4 flex flex-wrap gap-2">
            {suggestions.map((item) => (
              <button
                key={item}
                type="button"
                onClick={() => sendMessage(item)}
                className="rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-white/80 hover:bg-white/10"
              >
                {item}
              </button>
            ))}
          </div>
        )}

        <form
          className="mt-4 flex gap-3"
          onSubmit={(e) => {
            e.preventDefault();
            sendMessage();
          }}
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about the plant..."
            className="input-field"
          />
          <button type="submit" disabled={sending} className="btn-primary">
            Send
          </button>
        </form>
      </section>
    </div>
  );
}
