/**
 * Content Safety Guardrail
 *
 * A chatbot with a two-stage pipeline: every user message passes through
 * a moderation layer before reaching the main chat model. This demonstrates
 * the guardrail pattern:
 *
 * User input -> Moderation model (pass/block) -> Chat model -> Response
 *
 * The moderation model is a separate, stateless call that returns structured
 * JSON ({"is_safe": boolean, "reason": string}). If the input is blocked, the
 * chat model never sees it. If it passes, the chat model responds normally
 * with full conversation history.
 *
 * Key techniques:
 * - Structured JSON output via responseMimeType
 * - Temperature 0.0 for deterministic safety checks
 * - Separate model instances for moderation vs. chat
 */

import readline from 'readline';
import { GoogleGenAI } from '@google/genai';
import 'dotenv/config';

// Initialize the Gemini client. Automatically picks up GEMINI_API_KEY from .env
const ai = new GoogleGenAI({});

// Both the moderation layer and chat use the same model but as separate
// instances -- the moderation call is stateless (one-shot), while the
// chat session maintains conversation history.
const MODERATION_MODEL = 'gemini-2.5-flash';
const CHAT_MODEL = 'gemini-2.5-flash';

// -- Moderation system instruction -----------------------------------------
// Defines what the moderation model should flag and the output format.
// responseMimeType: 'application/json' forces the model to return valid
// JSON, which we parse to get the safety verdict.
const MODERATION_INSTRUCTION = `
You are a content safety shield. Analyze the user's input.
Return a valid JSON object: {"is_safe": boolean, "reason": "string"}.
Rules:
- Block hate speech, violence, illegal acts, and personal insults.
- Allow casual conversation and technical questions.
- If unsafe, provide a short, polite reason.
`;

// The main chat session -- preserves conversation history across turns.
const chat = ai.chats.create({ model: CHAT_MODEL });

console.log("Secure Chatbot ready. Type 'q' or 'e' to exit.");
console.log("-".repeat(50));

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// -- Main loop -------------------------------------------------------------
// Each message goes through two stages:
//   1. Moderation gate -- a one-shot call screens the input.
//   2. Chat response   -- only reached if moderation passes.
const askQuestion = () => {
  rl.question('\nYou: ', async (userInput) => {
    const inputLower = userInput.toLowerCase().trim();

    if (['q', 'e', 'exit', 'quit'].includes(inputLower)) {
      console.log('Goodbye!');
      rl.close();
      return;
    }

    // -- Step 1: Moderation gate -------------------------------------------
    // A stateless generateContent call (not a chat) checks the input.
    // temperature: 0.0 ensures deterministic, consistent safety decisions.
    try {
      const moderationResponse = await ai.models.generateContent({
        model: MODERATION_MODEL,
        contents: `Analyze this text: ${userInput}`,
        config: {
          systemInstruction: MODERATION_INSTRUCTION,
          responseMimeType: 'application/json',
          temperature: 0.0,
        }
      });

      // Parse the JSON string returned by the model
      const safetyResponse = JSON.parse(moderationResponse.text);
      const isSafe = safetyResponse.is_safe ?? false;
      const reason = safetyResponse.reason ?? 'Unknown safety error';

      if (!isSafe) {
        console.log(`\n[Blocked] ${reason}`);
        askQuestion(); // Loop back for the next input
        return;
      }
    } catch (error) {
      console.log(`\n[Moderation error] ${error.message || error}`);
      askQuestion();
      return;
    }

    // -- Step 2: Chat response ---------------------------------------------
    // Only reached if moderation passed. The chat session preserves history
    // so the model has context from earlier turns.
    try {
      const response = await chat.sendMessage({ message: userInput });
      console.log(`\nBot: ${response.text}`);
    } catch (error) {
      console.log(`\nError: ${error.message || error}`);
    }

    // Loop back for the next input
    askQuestion();
  });
};

// Start the loop
askQuestion();