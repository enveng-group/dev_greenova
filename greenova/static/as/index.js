// filepath: /assemblyscript-project/index.js
// This file serves as the entry point for the JavaScript side of the project,
// potentially importing the compiled WebAssembly module and providing an interface for interaction.

import { instantiate } from "./build/optimized.wat";

async function init() {
	const { instance } = await instantiate();
	// You can now use the instance to call exported functions from the WebAssembly module
}

init().catch(console.error);
