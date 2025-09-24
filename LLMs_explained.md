# How Large Language Models (LLMs) Work

Large language models (LLMs) are everywhere these days, but for most people they remain a bit of a mystery. In this guide, we’ll break down how they work in a simple, intuitive way. We’ll start with the big picture and then go step by step into the details, highlighting the key ideas that not only explain what’s going on under the hood but also show you how to get the most out of them.

## LLMs are fancy autocomplete systems

LLMs such as OpenAI’s ChatGPT and Anthropic’s Claude are AI-powered assistants. When you give them a query or instruction — called a `prompt` — they generate a response tailored to that input.
 
<img src="images/chatgpt_ui.png" width="600"/><br>

Here’s how LLM works: when you give an LLM a prompt, it generates text - one word at a time. After predicting a word, it adds that word to the prompt and uses the updated prompt to predict the next word. This process repeats again and again until it produces a full response.

![LLM predicting one word at a time](images/next_token_llm.gif)

This basically means that LLMs are just autocomplete systems trained to predict the next word in a sequence based on the words that came before it. This is similar to how your phone's keyboard suggests the next word as you type a message.

<img src="images/keyboard.png" width="400"/><br>

So why do LLMs seem so smart while your phone’s autocomplete can feel… well, silly? The difference comes down to training. LLMs are trained on massive datasets containing trillions of words -- allowing them to learn complex patterns and relationships between words. This enables them to generate coherent and contextually relevant responses.

## LLMs operate on tokens, not words

Saying that LLMs predict the next `word` is not actually accurate. LLMs don’t see words. They have never seen a word. What they see are called `tokens`. A token is the smallest unit of text that a LLM can understand, read, process and respond.

A token could be:
* A full word (`apple`)
* Part of a word (`ing` in `running`)
* Punctuation (`.` or `,`)
* Even a single character in some cases

For example, the sentence:
```
I love pizza!
```
might be broken into tokens like:
```
["I", " love", " pizza", "!"]
```

<img src="images/tokenization_example.png" width="600"/><br>

or in other tokenization schemes:
```
["I", " lov", "e", " pi", "zza", "!"]
```
How the input text will be divided into tokens depends on the LLMs `vocabulary`.

## Building the Vocabulary

During the time of training, the LLM builds a `vocabulary` - a dictionary of all unique tokens it will recognize and use.

- Initially, the vocabulary consists of individual characters (like letters and punctuation).
- The training data is then scanned to find the most frequently occurring pairs of characters. For example, if ‘th’ appears often, it becomes a candidate to be added to the vocabulary.
- These common pairs are then merged to form new tokens. The process continues iteratively, each time identifying and merging the next most frequent pair. The vocabulary grows from individual characters to common pairings and eventually to larger structures like common words or parts of words.
- There’s a limit to the vocabulary size (e.g., 50,000 tokens in GPT-2). Once this limit is reached, the process stops, resulting in a fixed-size collection of tokens.

Once the vocabulary is built, each token is assigned a unique numerical ID called `token ID`. Even special characters like `!` are assigned token IDs.

**Note:** Some people refer to `vocabulary` as `model dictionary`.

## Token ids are what’s actually sent to the LLM

- When you provide a prompt, the input is first broken down into a sequence of tokens based on the model's `vocabulary`. This process is called `tokenization`. The tokens are then converted from strings to their corresponding `token IDs`.

    For example:
    ```
    "I love pizza!" -> ["I", " love", " pizza", "!"] -> [40, 3047, 27941, 0]
    ```
    
    <img src="images/ilovepizza_token.png" width="600"/><br>
    <img src="images/ilovepizza_token_id.png" width="600"/><br>
- If a word in prompt is found not present in the vocabulary, it’s broken down into smaller tokens that are in the vocabulary.

**The token ids are what’s actually sent to the LLM.**

## From Tokens to Embeddings: Turning Numbers into Meaning

Imagine that in a certain model's vocabulary, the following tokens are assigned these token IDs:

| Token   | Token ID |
|---------|----------|
| cat     | 17       |
| dog     | 42       |
| banana  | 99       |

Notice that the token IDs like "42" for "dog" and "17" for "cat" are just unique labels — they don’t tell the computer anything about how the words are related. Token IDs are like jersey numbers: useful for identification, but meaningless for understanding.

To help the model understand relationships between tokens, each token ID is mapped to a list of numbers called an **embedding vector**. These vectors capture the meaning and context of each token.

For example (using made-up numbers):

| Token   | Token ID | Embedding Vector      |
|---------|----------|----------------------|
| cat     | 17       | [0.8, 0.2, 0.1]      |
| dog     | 42       | [0.7, 0.3, 0.2]      |
| banana  | 99       | [0.1, 0.9, 0.5]      |

Here’s why this matters:
- The vectors for "cat" and "dog" are similar, so the model knows they’re related (both are animals).
- The vector for "banana" is different, so the model knows it’s not related to "cat" or "dog" (it’s food).

The first block of the LLM - The embedding block -  does this. It takes the token IDs and converts them into embedding vectors that the model can work with. 

<em>Embeddings are the secret sauce that makes the LLMs work so well. If you find ways to create better embeddings, you will likely create a better model. </em>

## LLMs generate probabilities, not words

When you ask an LLM a question, it doesn’t actually “know” the answer in the way a human does. Instead, it generates a list of possible next words along with their probabilities based on the context of your prompt. It then selects the word with the highest probability and adds it to the response.

## References
- https://amgadhasan.substack.com/p/explaining-how-llms-work-in-7-levels
- https://medium.com/the-research-nest/explained-tokens-and-embeddings-in-llms-69a16ba5db33
- https://medium.com/data-science-at-microsoft/how-large-language-models-work-91c362f5b78f
- https://old.reddit.com/r/artificial/comments/1bh38a0/why_do_llms_give_different_responses_to_the_same/kvb4rl8/
- https://gist.github.com/kalomaze/4473f3f975ff5e5fade06e632498f73e
- https://cobusgreyling.medium.com/openai-seeding-model-fingerprints-log-probabilities-cedf094e8b02