import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
  const { user } = useAuth();
  const [recent, setRecent] = useState([]);
  const [plants, setPlants] = useState([]);

  useEffect(() => {
    async function loadData() {
      const [recentRes, plantsRes] = await Promise.all([
        api.get('/predictions/recent'),
        api.get('/plants'),
      ]);
      setRecent(recentRes.data.data || []);
      setPlants(plantsRes.data.data || []);
    }
    loadData();
  }, []);

  return (
    <div className="space-y-8">
      <section className="card">
        <h1 className="text-3xl font-bold gradient-text">Welcome, {user?.name}</h1>
        <p className="mt-2 max-w-2xl text-white/70">
          Upload a leaf image to identify medicinal plants, explore their uses, and chat with the AI assistant.
        </p>
        <Link to="/identify" className="btn-primary mt-6 inline-flex">
          Identify a plant
        </Link>
      </section>

      <section>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold">Recent identifications</h2>
          <Link to="/history" className="text-sm text-cyan-300 hover:text-cyan-200">
            View all
          </Link>
        </div>
        {recent.length === 0 ? (
          <div className="card text-white/60">No predictions yet. Try identifying your first plant.</div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {recent.map((item) => (
              <div key={item.id} className="card">
                <p className="font-semibold">{item.plant_name || 'Unknown plant'}</p>
                <p className="text-sm text-white/60">
                  Confidence: {Math.round((item.confidence || 0) * 100)}%
                </p>
                {item.plant_name && (
                  <Link to={`/plant/${item.plant_name}`} className="mt-3 inline-block text-sm text-cyan-300">
                    View details
                  </Link>
                )}
              </div>
            ))}
          </div>
        )}
      </section>

      <section>
        <h2 className="mb-4 text-xl font-semibold">Supported plants</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {plants.slice(0, 8).map((plant) => (
            <Link key={plant.name} to={`/plant/${plant.name}`} className="card transition hover:border-purple-400/40">
              <p className="font-semibold">{plant.name}</p>
              <p className="mt-1 text-sm text-white/60">{plant.scientific_name}</p>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
