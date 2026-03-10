import { NextResponse } from 'next/server';

// L'URL de notre backend Python (FastAPI)
const PYTHON_API_URL = process.env.NEXT_PUBLIC_PYTHON_API_URL || 'http://localhost:8000/api/v1';

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();
    
    // On récupère la dernière question posée par l'utilisateur
    const lastMessage = messages[messages.length - 1];

    console.log(`Transmission de la question à Python : "${lastMessage.content}"`);

    // Appel HTTP vers FastAPI (Python)
    const pythonResponse = await fetch(`${PYTHON_API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // On respecte le format attendu par notre ChatRequest en Python
      body: JSON.stringify({ question: lastMessage.content }),
    });

    if (!pythonResponse.ok) {
      throw new Error(`Le backend Python a répondu avec une erreur ${pythonResponse.status}`);
    }

    // On parse le JSON renvoyé par Python ({"answer": "..."})
    const data = await pythonResponse.json();

    // On retourne uniquement le texte de la réponse au composant React
    return new NextResponse(data.answer);

  } catch (error) {
    console.error("Erreur critique dans l'API Chat (Pont Next.js -> Python):", error);
    return new NextResponse(
      "Oups, la connexion avec le cerveau IA (Python) a échoué. Regardez les logs du serveur.", 
      { status: 500 }
    );
  }
}