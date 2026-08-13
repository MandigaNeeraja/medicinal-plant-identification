import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api, { getErrorMessage } from '../api/client';

export default function History() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadHistory() {
      try {
        const response = await api.get('/predictions/history');
        setItems(response.data.data?.items || []);
      } catch (err) {
        setError(getErrorMessage(err));
      }
    }
    loadHistory();
  }, []);

  if (error) {
    return <div className="card text-red-300">{error}</div>;
  }

  return (
    <div className="space-y-6">
      <section className="card">
        <h1 className="text-3xl font-bold gradient-text">Prediction history</h1>
        <p className="mt-2 text-white/70">Review your previous plant identifications.</p>
      </section>

      {items.length === 0 ? (
        <div className="card text-white/60">No history yet.</div>
      ) : (
        <div className="grid gap-4">
          {items.map((item) => (
            <div key={item.id} className="card flex flex-wrap items-center justify-between gap-4">
              <div>
                <p className="text-lg font-semibold">{item.plant_name || 'Unknown plant'}</p>
                <p className="text-sm text-white/60">
                  {new Date(item.created_at).toLocaleString()} · Confidence {Math.round((item.confidence || 0) * 100)}%
                </p>
              </div>
              {item.plant_name && (
                <Link to={`/plant/${item.plant_name}`} className="btn-secondary">
                  View details
                </Link>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
