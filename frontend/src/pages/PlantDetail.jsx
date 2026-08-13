import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import api, { getErrorMessage } from '../api/client';

export default function PlantDetail() {
  const { name } = useParams();
  const [plant, setPlant] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadPlant() {
      try {
        const response = await api.get(`/plants/${encodeURIComponent(name)}`);
        setPlant(response.data.data);
      } catch (err) {
        setError(getErrorMessage(err));
      }
    }
    loadPlant();
  }, [name]);

  if (error) {
    return <div className="card text-red-300">{error}</div>;
  }

  if (!plant) {
    return (
      <div className="flex justify-center py-20">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-purple-500/30 border-t-purple-400" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <section className="card">
        <h1 className="text-3xl font-bold gradient-text">{plant.name}</h1>
        <p className="mt-2 text-white/70">{plant.scientific_name}</p>
        <p className="mt-4 text-white/80">{plant.overview}</p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link to={`/chat/${plant.name}`} className="btn-primary">
            Chat with AI
          </Link>
          <Link to="/identify" className="btn-secondary">
            Identify another plant
          </Link>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="card">
          <h2 className="text-xl font-semibold">Medicinal uses</h2>
          <ul className="mt-4 space-y-2 text-white/80">
            {plant.medicinal_uses?.map((use) => (
              <li key={use} className="rounded-lg bg-white/5 px-3 py-2 text-sm">
                {use}
              </li>
            ))}
          </ul>
        </section>

        <section className="card">
          <h2 className="text-xl font-semibold">Preparation</h2>
          <div className="mt-4 space-y-3 text-sm text-white/80">
            {Object.entries(plant.preparation || {}).map(([method, details]) => (
              <div key={method} className="rounded-lg bg-white/5 px-3 py-2">
                <p className="font-medium capitalize">{method}</p>
                <p className="mt-1 text-white/70">{details}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="card">
          <h2 className="text-xl font-semibold">Dosage</h2>
          <p className="mt-3 text-white/80">{plant.dosage}</p>
        </section>

        <section className="card">
          <h2 className="text-xl font-semibold">Safety</h2>
          <p className="mt-3 text-white/80">{plant.safety}</p>
        </section>
      </div>

      <section className="card">
        <h2 className="text-xl font-semibold">Did you know?</h2>
        <p className="mt-3 text-white/80">{plant.did_you_know}</p>
      </section>
    </div>
  );
}
