export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-8 bg-gray-50 text-gray-900">
      <h1 className="text-3xl font-bold mb-8 text-blue-600">🧠 Second Brain</h1>

      {/* Chat Window Area */}
      <div className="grow w-full max-w-2xl bg-white rounded-lg shadow-md p-6 overflow-y-auto mb-4 border border-gray-200">
        <p className="text-gray-400 italic text-center mt-20">
          Ask a question about your documents...
        </p>
      </div>

      {/* Input Area */}
      <div className="w-full max-w-2xl flex gap-2">
        <input
          type="text"
          placeholder="A quoi sert le mot clé 'this' en java ?"
          className="grow border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button className="bg-blue-600 text-white px-6 py-3 font-semibold rounded-lg hover:bg-blue-700 transition-colors">
          Send
        </button>
      </div>
    </main>
  );
}