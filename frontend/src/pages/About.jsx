export default function About() {
  return (
    <div className="space-y-6">
      <section className="card">
        <h1 className="text-3xl font-bold gradient-text">About this project</h1>
        <p className="mt-4 text-white/80">
          Medicinal Plant Identification uses a convolutional neural network trained on leaf images
          to recognize medicinal plant species and provide structured information about their uses.
        </p>
      </section>

      <section className="card">
        <h2 className="text-xl font-semibold">Features</h2>
        <ul className="mt-4 space-y-2 text-white/80">
          <li>AI-powered leaf image classification</li>
          <li>Medicinal uses, preparation, dosage, and safety information</li>
          <li>Groq-powered chat assistant for follow-up questions</li>
          <li>Secure JWT authentication with email and Google sign-in</li>
          <li>Personal prediction history</li>
        </ul>
      </section>
    </div>
  );
}
