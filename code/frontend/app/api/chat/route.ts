import { NextResponse } from 'next/server';

const PYTHON_API_URL = process.env.NEXT_PUBLIC_PYTHON_API_URL || 'http://localhost:8000/api/v1';

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();
    
    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return new NextResponse("Invalid request: No messages provided.", { status: 400 });
    }

    const lastMessage = messages[messages.length - 1];

    console.log(`Forwarding user query to AI service: "${lastMessage.content}"`);

    const pythonResponse = await fetch(`${PYTHON_API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question: lastMessage.content }),
    });

    if (!pythonResponse.ok) {
      throw new Error(`Python backend responded with status: ${pythonResponse.status}`);
    }

    const data = await pythonResponse.json();

    return new NextResponse(data.answer);

  } catch (error) {
    console.error("Critical error in Chat API routing:", error);
    return new NextResponse(
      "An error occurred while communicating with the AI service. Please check the server logs.", 
      { status: 500 }
    );
  }
}