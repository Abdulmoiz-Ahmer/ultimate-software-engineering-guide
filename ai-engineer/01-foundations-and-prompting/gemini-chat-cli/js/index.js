/**
 * Gemini Chat CLI -- JavaScript
 *
 * A minimal terminal chatbot using Google's Gemini 2.5 Flash model.
 * The @google/genai SDK's chat session handles conversation history
 * automatically, so follow-up questions retain context from earlier
 * in the conversation.
 *
 * This is the JS equivalent of the Python version. The main difference
 * is the input loop: Node.js uses readline with a recursive callback
 * pattern instead of Python's synchronous while/input loop.
 */

import readline from 'readline';
import { GoogleGenAI } from '@google/genai';
import 'dotenv/config'; // Loads GEMINI_API_KEY from .env into process.env

// Initialize the Gemini client. The SDK automatically picks up
// GEMINI_API_KEY from environment variables (loaded by dotenv above).
const ai = new GoogleGenAI({});

// Create a stateful chat session. Like the Python version, this object
// tracks the full conversation history internally, so the model
// remembers prior messages without manual history management.
const chat = ai.chats.create({ model: 'gemini-2.5-flash' });

console.log("Chat ready. Type 'q' or 'e' to exit.");
console.log('-'.repeat(50));

// Set up readline for terminal input/output. This is Node.js's built-in
// way to read interactive line-by-line input from the terminal.
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

// -- Main conversation loop ------------------------------------------------
// Node.js doesn't have a synchronous input() like Python, so we use a
// recursive callback pattern: askQuestion calls itself after each response
// to wait for the next input.

const askQuestion = () => {
  rl.question('You: ', async (userInput) => {
    const inputLower = userInput.toLowerCase().trim();

    if (['q', 'e', 'exit', 'quit'].includes(inputLower)) {
      console.log('Shutting down...');
      rl.close();
      return;
    }

    try {
      // Send the message to the stateful chat session. The session
      // appends this exchange to its internal history automatically.
      const response = await chat.sendMessage({ message: userInput });
      console.log(`\nBot: ${response.text}\n`);
    } catch (error) {
      console.log(`\nError: ${error.message || error}\n`);
    }

    // Recurse to wait for the next input.
    askQuestion();
  });
};

askQuestion();
