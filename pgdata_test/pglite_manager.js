const { PGlite } = require('@electric-sql/pglite');
const { PGLiteSocketServer } = require('@electric-sql/pglite-socket');
const fs = require('fs');
const path = require('path');
const { unlink } = require('fs/promises');
const { existsSync } = require('fs');


const SOCKET_PATH = '/var/folders/m4/5zmhmx610sdfvqzr4h627g6w0000gn/T/py-pglite-74288-7e55414e/.s.PGSQL.5432';

async function cleanup() {
    if (existsSync(SOCKET_PATH)) {
        try {
            await unlink(SOCKET_PATH);
            console.log(`Removed old socket at ${SOCKET_PATH}`);
        } catch (err) {
            // Ignore errors during cleanup
        }
    }
}

async function startServer() {
    try {
        // Create a PGlite instance with extensions
        const db = new PGlite({
            extensions: {}
        });

        // Clean up any existing socket
        await cleanup();

        // Create and start a socket server
        const server = new PGLiteSocketServer({
            db,
            path: SOCKET_PATH,
        });
        await server.start();
        console.log(`Server started on socket ${SOCKET_PATH}`);

        // Handle graceful shutdown
        process.on('SIGINT', async () => {
            console.log('Received SIGINT, shutting down gracefully...');
            try {
                await server.stop();
                await db.close();
                console.log('Server stopped and database closed');
            } catch (err) {
                console.error('Error during shutdown:', err);
            }
            process.exit(0);
        });

        process.on('SIGTERM', async () => {
            console.log('Received SIGTERM, shutting down gracefully...');
            try {
                await server.stop();
                await db.close();
                console.log('Server stopped and database closed');
            } catch (err) {
                console.error('Error during shutdown:', err);
            }
            process.exit(0);
        });

        // Keep the process alive
        process.on('exit', () => {
            console.log('Process exiting...');
        });

    } catch (err) {
        console.error('Failed to start PGlite server:', err);
        process.exit(1);
    }
}

startServer();