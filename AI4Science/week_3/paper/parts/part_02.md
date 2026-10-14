# Часть 2: с. 4–6

[с. 4]
Input Context
Write a high-quality answer for the given question using only the provided search
results (some of which might be irrelevant).
Document [1](Title: Asian Americans in science and technology) Prize in physics for
discovery of the subatomic particle J/ψ. Subrahmanyan Chandrasekhar shared...
Document [2](Title: List of Nobel laureates in Physics) The first Nobel Prize in
Physics was awarded in 1901 to Wilhelm Conrad Röntgen, of Germany, who received...
Document [3](Title: Scientist) and pursued through a unique method, was essentially
in place. Ramón y Cajal won the Nobel Prize in 1906 for his remarkable...
Question: who got the first nobel prize in physics
Answer:
Desired Answer
Wilhelm Conrad Röntgen

Figure 2: Example of the multi-document question answering task, with an input context and the desired model
answer. The document containing the answer is bolded within the input context here for clarity.
Input Context
Write a high-quality answer for the given question
using only the provided search results (some of
which might be irrelevant).

Input Context
Write a high-quality answer for the given question
using only the provided search results (some of
which might be irrelevant).

Document [1](Title: List of Nobel laureates in
Physics) ...
Document [2](Title: Asian Americans in science and
technology) ...
Document [3](Title: Scientist) ...

Document [1](Title: Asian Americans in science and
technology) ...
Document [2](Title: List of Nobel laureates in
Physics) ...
Document [3](Title: Scientist) ...
Document [4](Title: Norwegian Americans) ...
Document [5](Title: Maria Goeppert Mayer) ...

Question: who got the first nobel prize in physics
Answer:
Desired Answer
Wilhelm Conrad Röntgen

Question: who got the first nobel prize in physics
Answer:
Desired Answer
Wilhelm Conrad Röntgen

Figure 3: Modulating the position of relevant information within the input context for the multi-document
question answering example presented in Figure 2. Reordering the documents in the input context does not
affect the desired output.

Our experimental setup is similar to the needlein-a-haystack experiments of Ivgi et al. (2023), who
compare question answering performance when the
relevant paragraph is placed (i) at the beginning of
the input or (ii) a random position within the input. They find that encoder-decoder models have
significantly higher performance when relevant information is placed at the start of the input context.
In contrast, we study finer-grained changes in the
position of relevant information.
2.2

Models

We analyze several state-of-the-art open and closed
language models. We use greedy decoding when
generating outputs and leave exploration of other
decoding methods to future work. We use a standard set of prompts for each model (Figure 2).

Figure 4: Modulating the input context length of the
multi-document question answering example presented
in Figure 2. Adding documents that do not contain the
answer increases the length of the input context, but
does not affect the desired output.

Open models. We experiment with MPT-30BInstruct, which has a maximum context length of
8192 tokens. The model was initially pre-trained
on 1 trillion tokens using 2048-token sequences,
followed by an additional sequence length adaptation pre-training phase on 50 billion tokens using
8192-token sequences. MPT-30B-Instruct uses ALiBi (Press et al., 2022) to represent positional information. We also evaluate LongChat-13B (16K) (Li
et al., 2023), which extends the LLaMA-13B (Touvron et al., 2023a) context window from 2048 to
16384 tokens by using condensed rotary positional
embeddings before fine-tuning with 16384-token
sequences.
Closed models. We use the OpenAI API to experiment with GPT-3.5-Turbo and GPT-3.5-Turbo

[с. 5]
20 Total Retrieved Documents (~4K tokens)

30 Total Retrieved Documents (~6K tokens)
75

70

70

70

65
60

65
60

55

55

50

50
1st

5th

10th

Position of Document with the Answer
claude-1.3

claude-1.3-100k

Accuracy

75

Accuracy

Accuracy

10 Total Retrieved Documents (~2K tokens)
75

65
60
55
50

1st

5th

10th

15th

20th

Position of Document with the Answer

gpt-3.5-turbo-0613

gpt-3.5-turbo-16k-0613

1st 5th

10th 15th 20th 25th 30th

Position of Document with the Answer

mpt-30b-instruct

longchat-13b-16k

Figure 5: The effect of changing the position of relevant information (document containing the answer) on multidocument question answering performance. Lower positions are closer to the start of the input context. Performance
is highest when relevant information occurs at the very start or end of the context, and rapidly degrades when models
must reason over information in the middle of their input context.

(16K).5 GPT-3.5-Turbo has a maximum context
length of 4K tokens, and GPT-3.5-Turbo (16K) is a
version with an extended maximum context length
of 16K tokens. We evaluate Claude-1.3 and Claude1.3 (100K) with the Anthropic API; Claude-1.3
has a maximum context length of 8K tokens, and
Claude-1.3 (100K) has an extended context length
of 100K tokens. 6
2.3

Model performance is highest when relevant information occurs at the beginning or end of its
input context. As illustrated in Figure 5, changing the position of relevant information in the input context leads to substantial decreases in model
performance. In particular, we see a distinctive UWe use the 0613 OpenAI model versions.
We also evaluate GPT-4 (8K) on a subset of multidocument QA experiments, finding similar results and trends
as other models (though GPT-4 has higher absolute performance). Evaluating GPT-4 on the full multi-document QA
and key-value retrieval experiments would cost upwards of
$6000. See Appendix D for GPT-4 results and discussion.
6

LongChat-13B (16K)
MPT-30B-Instruct
GPT-3.5-Turbo
GPT-3.5-Turbo (16K)
Claude-1.3
Claude-1.3 (100K)

Closed-Book

Oracle

35.0%
31.5%
56.1%
56.0%
48.3%
48.2%

83.4%
81.9%
88.3%
88.6%
76.1%
76.4%

Table 1: Closed-book and oracle accuracy of language
models on the multi-document question answering task.

Results and Discussion

We experiment with input contexts containing 10,
20, and 30 total documents. Figure 5 presents multidocument question answering performance when
varying the position of relevant information within
the input context. To contextualize model performance, we also evaluate on the closed-book and
oracle settings (Table 1). In the closed-book setting,
models are not given any documents in their input
context, and must rely on their parametric memory
to generate the correct answer. On the other hand,
in the oracle setting, language models are given the
single document that contains the answer and must
use it to answer the question.

5

Model

shaped performance curve—models are often much
better at using relevant information that occurs at
the very beginning (primacy bias) and very end of
contexts (recency bias), and suffer degraded performance when forced to use information within the
middle of its input context. For example, GPT-3.5Turbo’s multi-document QA performance can drop
by more than 20%—in the worst case, performance
in 20- and 30-document settings is lower than performance without any input documents (i.e., closedbook performance; 56.1%). These results indicate
that current models cannot effectively reason over
their entire context window when prompted for
downstream tasks.
Extended-context models are not necessarily better at using input context. When the input context fits in the context window of both a model
and its extended-context counterpart, we see that
performance between them is nearly identical. For
example, the 10- and 20-document settings both
fit in the context window of GPT-3.5-Turbo and
GPT-3.5-Turbo (16K), and we observe that their
performance as a function of position of relative
information is nearly superimposed (solid purple
and dashed brown series in Figure 5). These results

[с. 6]
Input Context
Extract the value corresponding to the specified key in the JSON object below.
JSON data:
{"2a8d601d-1d69-4e64-9f90-8ad825a74195": "bb3ba2a5-7de8-434b-a86e-a88bb9fa7289",
"a54e2eed-e625-4570-9f74-3624e77d6684": "d1ff29be-4e2a-4208-a182-0cea716be3d4",
"9f4a92b9-5f69-4725-ba1e-403f08dea695": "703a7ce5-f17f-4e6d-b895-5836ba5ec71c",
"52a9c80c-da51-4fc9-bf70-4a4901bc2ac3": "b2f8ea3d-4b1b-49e0-a141-b9823991ebeb",
"f4eb1c53-af0a-4dc4-a3a5-c2d50851a178": "d733b0d2-6af3-44e1-8592-e5637fdb76fb"}
Key: "9f4a92b9-5f69-4725-ba1e-403f08dea695"
Corresponding value:
Desired Output
703a7ce5-f17f-4e6d-b895-5836ba5ec71c

Figure 6: Example of the key-value retrieval task, with an input context and the desired model output. Given a key,
the goal is to return the associated value. All keys and values are 128-bit UUIDs. The relevant key-value pair for
answering the query is bolded here within the input context for clarity.

indicate that extended-context models are not necessarily better than their non-extended counterparts
at using their input context.

3

How Well Can Language Models
Retrieve From Input Contexts?

Given that language models struggle to retrieve
and use information from the middle of their input
contexts in the multi-document question answering
task, to what extent can they simply retrieve from
input contexts? We study this question with a synthetic key-value retrieval task, which is designed to
provide a minimal testbed for the basic ability to
retrieve matching tokens from an input context.
3.1

Experimental Setup

In our synthetic key-value retrieval task, the inputs
are (i) a string-serialized JSON object with k keyvalue pairs, where each of the keys and values are
unique, randomly-generated UUIDs and (ii) a key
within the aforementioned JSON object. The goal
is to return the value associated with the specified
key. Thus, each JSON object contains one relevant
key-value pair (where the value is to be returned),
and k − 1 irrelevant “distractor” key-value pairs.
Figure 6 provides an example input context and its
corresponding desired output. We again measure
accuracy by evaluating whether the correct value
appears in the predicted output.
Our synthetic key-value retrieval task shares similar goals with the Little Retrieval Test of Papailiopoulos et al. (2023) and the fine-grained line retrieval task of Li et al. (2023), but we explicitly
seek to distill and simplify the task by removing as

much natural language semantics as possible (using
random UUIDs instead), since language features
may present potential confounders. For example,
Transformer language models may have varying
sensitivity to different linguistic features in their
input (O’Connor and Andreas, 2021).
To modulate the position of relevant information
within the input context, we change the position
of the key to retrieve within the serialized JSON
object. To modulate the input context length, we
change the number of input JSON key-value pairs
k by adding or removing random keys, changing
the number of distractor key-value pairs.
3.2

Results and Discussion

We experiment with input contexts containing
75, 140, and 300 key-value pairs (500 examples
each). We use the same set of models as the multidocument question answering experiments, see
§2.2 for more details.
Figure 7 presents key-value retrieval performance. Claude-1.3 and Claude-1.3 (100K) do
nearly perfectly on all evaluated input context
lengths, but other models struggle, especially
when contexts have 140 or 300 key-value pairs—
although the synthetic key-value retrieval task only
requires identifying exact match within the input
context, not all models achieve high performance.
Similar to our multi-document QA results, GPT3.5-Turbo, GPT-3.5-Turbo (16K), and MPT-30BInstruct have the lowest performance when they
must access key-value pairs in the middle of their
input context. LongChat-13B (16K) exhibits a different trend in the 140 key-value setting; we qualitatively observe that when relevant information is

