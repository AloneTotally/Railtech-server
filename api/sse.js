// api/sse.js

export const config = {
    runtime: 'edge', // Ensure this runs in Vercel's Edge runtime
};

// A global variable to store messages from POST requests
let latestMessage = "Waiting for new data...";

export default async function handler(req) {
const encoder = new TextEncoder();

// Handle POST requests to store incoming data
if (req.method === "POST") {
    const body = await req.json();
    latestMessage = body.message || "No message provided"; // weird nullish coalescing
    return new Response(JSON.stringify({ status: 'success' }), {
    headers: { 'Content-Type': 'application/json' }
    });
}

// Handle GET requests for SSE
if (req.method === "GET") {
    const stream = new ReadableStream({
    start(controller) {
        // Send the initial message (latest received from POST)
        controller.enqueue(encoder.encode(`data: ${latestMessage}\n\n`));

        // Set up periodic updates every 2 seconds
        const interval = setInterval(() => {
        controller.enqueue(encoder.encode(`data: ${latestMessage}\n\n`));
        }, 2000);

        req.signal.addEventListener('abort', () => {
        clearInterval(interval);
        controller.close();
        });
    }
    });

    return new Response(stream, {
    headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        Connection: 'keep-alive',
    }
    });
}

// Return a method not allowed response for unsupported methods
return new Response("Method not allowed", { status: 405 });
}
