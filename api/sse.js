export const config = {
    runtime: 'edge', // Ensure this runs in Vercel's Edge runtime
};

// A global variable to store the latest message from POST requests
let latestMessage = "Waiting for new data...";

// A list of active clients to update when a POST request arrives
let activeClients = [];

export default async function handler(req) {
    const encoder = new TextEncoder();

    // Handle POST requests to store incoming data
    if (req.method === "POST") {
        const body = await req.json();
        latestMessage = body.message || "No message provided"; // Update the latest message

        // Notify all active clients
        activeClients.forEach(client => {
            client.controller.enqueue(encoder.encode(`data: ${latestMessage}\n\n`));
            // client.controller.close();  // Close after sending the message
        });

        // Clear the list of active clients after notifying them
        activeClients = [];

        return new Response(JSON.stringify({ status: 'success' }), {
            headers: { 'Content-Type': 'application/json' }
        });
    }

    // Handle GET requests for SSE
    if (req.method === "GET") {
        const stream = new ReadableStream({
            start(controller) {
                // Store the controller for future use (when a POST request arrives)
                activeClients.push({ controller });

                // If the request is aborted, remove the client from the active list
                req.signal.addEventListener('abort', () => {
                    activeClients = activeClients.filter(client => client.controller !== controller);
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
