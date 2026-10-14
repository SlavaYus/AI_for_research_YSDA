# Часть 3: с. 7–9

[с. 7]
1st

25th

50th

Position of Key to Retrieve

claude-1.3

claude-1.3-100k

75th

140 Key-Value Pairs (~8K tokens)

100
90
80
70
60
50
40

Accuracy

Accuracy

Accuracy

75 Key-Value Pairs (~4K tokens)

100
90
80
70
60
50
40

1st

35th

70th

105th

Position of Key to Retrieve

gpt-3.5-turbo-0613

140th

gpt-3.5-turbo-16k-0613

100
90
80
70
60
50
40

300 Key-Value Pairs (~16K tokens)

1st 50th 100th 150th 200th 250th 300th

Position of Key to Retrieve

mpt-30b-instruct

longchat-13b-16k

Figure 7: The effect of changing the input context length and the position of relevant information on key-value
retrieval performance. Lower positions are closer to the start of the input context. Although some models show
perfect accuracy on this synthetic task (e.g., Claude-1.3 and Claude-1.3 (100K)), we see again that performance is
often highest when relevant information is occurs at the very start or end of the context, and rapidly degrades when
models must retrieve from the middle of the input context.

placed at the start of the input context, LongChat13B (16K) tends to generate code to retrieve the
key, rather than outputting the value directly.

4

Why Are Language Models Not Robust
to Changes in the Position of Relevant
Information?

Our multi-document question answering and keyvalue retrieval results show that language models
struggle to robustly access and use information in
long input contexts, since performance degrades
significantly when changing the position of relevant information. To better understand why, we perform some preliminary investigations into the role
of model architecture (decoder-only vs. encoderdecoder), query-aware contextualization, and instruction fine-tuning.
4.1

Effect of Model Architecture

The open models we evaluated are all decoder-only
models—at each timestep, they may only attend
to prior tokens. To better understand the potential effects of model architecture on how language
model use context, we compare decoder-only and
encoder-decoder language models.
We experiment with Flan-T5-XXL (Raffel et al.,
2020; Chung et al., 2022) and Flan-UL2 (Tay et al.,
2023). Flan-T5-XXL is trained with a sequences
of 512 tokens (encoder and decoder). Flan-UL2 is
initially trained with sequences of 512 tokens (encoder and decoder), but is then pre-trained for an
extra 100K steps with 1024 tokens (encoder and decoder) before instruction fine-tuning on sequences
with 2048 tokens in the encoder and 512 tokens
in the decoder. However, since these models use

relative positional embeddings, they can (in principle) extrapolate beyond these maximum context
lengths; Shaham et al. (2023) find that both models can perform well with sequences of up to 8K
tokens.
Figure 8 compares the performance of decoderonly and encoder-decoder models. When Flan-UL2
is evaluated on sequences within its 2048-token
training-time context window (Figure 8; left subplot), its performance is relatively robust to changes
in the position of relevant information within the
input context (1.9% absolute difference between
best- and worst-case performance). When evaluated on settings with sequences longer than 2048
tokens (Figure 8; center and right), Flan-UL2 performance begins to degrade when relevant information is placed in the middle. Flan-T5-XXL shows
a similar trend, where longer input contexts result
in a greater performance degradation when placing
relevant information in the middle of the input context. We hypothesize that encoder-decoder models
may make better use of their context windows because their bidirectional encoder allows processing
each document in the context of future documents,
potentially improving relative importance estimation between documents.
4.2

Effect of Query-Aware Contextualization

Our multi-document QA and key-value retrieval
experiments place the query (i.e., question to answer or key to retrieve) after the data to process
(i.e., the documents or the key-value pairs). As a
result, decoder-only models cannot attend to query
tokens when contextualizing documents or keyvalue pairs, since the query only appears at the end

[с. 8]
20 Total Retrieved Documents (~4K tokens)

30 Total Retrieved Documents (~6K tokens)

70

70

65

65

65

60
55
50

Accuracy

70

Accuracy

Accuracy

10 Total Retrieved Documents (~2K tokens)

60
55
50

1st

5th

60
55
50

10th

1st

Position of Document with the Answer

5th

10th

15th

20th

1st 5th

flan-t5-xxl

flan-ul2

Position of Document with the Answer

mpt-30b-instruct

longchat-13b-16k

10th 15th 20th 25th 30th

Position of Document with the Answer

Figure 8: When encoder-decoder models (Flan-UL2 and Flan-T5-XXL) evaluated on sequences that are shorter
than their encoder’s training-time maximum sequence length (2048 and 512 tokens, respectively), they are relatively
robust to changes in the position of relevant information within their input context (left subplot). In contrast, when
these models are evaluated on sequences longer than those seen during training (center and right subplots), we
observe a U-shaped performance curve—performance is higher when relevant information occurs at the beginning
or end of the input context, as opposed to the middle of the input context.

20 Total Retrieved Documents
(~4K tokens, query-aware contextualization)

Accuracy

80
70
60
50
1st

5th

10th

15th

20th

Position of Document with the Answer

claude-1.3
claude-1.3-100k
gpt-3.5-turbo-0613

gpt-3.5-turbo-16k-0613
mpt-30b-instruct
longchat-13b-16k

Figure 9: Query-aware contextualization (placing the
query before and after the documents) does not substantially improve robustness of language models to
changing the position of relevant information in multidocument QA; performance slightly increases when
relevant information occurs at the very beginning, but
otherwise slightly decreases.

of the prompt and decoder-only models can only
attend to prior tokens at each timestep. In contrast,
encoder-decoder models (which seem more robust
to changes in the position of relevant information;
§4.1) use a bidirectional encoder to contextualize
input contexts—can we use this observation to improve decoder-only models by placing the query before and after the data, enabling query-aware contextualization of documents (or key-value pairs)?
We find that query-aware contextualization dramatically improves performance on the key-value
retrieval task—all models achieve near-perfect per-

formance on the 75, 140, and 300 key-value pair
settings. For example, GPT-3.5-Turbo (16K) with
query-aware contextualization achieves perfect performance when evaluated with 300 key-value pairs.
In contrast, without query-aware contextualization, the worst-case performance is 45.6% (Figure 7). Despite the significant impact on keyvalue retrieval performance, query-aware contextualization minimally affects performance trends in
the multi-document question answering task (Figure 9); it slightly improves performance when the
relevant information is located at the very beginning of the input context, but slightly decreases
performance in other settings.
4.3

Effect of Instruction Fine-Tuning

The models we evaluated are all instruction finetuned—after their initial pre-training, they undergo
supervised fine-tuning on a dataset of instructions
and responses. The task specification and/or instruction is commonly placed at the beginning of
the input context in supervised instruction finetuning data, which might lead instruction finetuned language models to place more weight on
the start of the input context. To better understand
the potential effects of instruction fine-tuning on
how language models use long input contexts, we
compare the multi-document question answering
performance of MPT-30B-Instruct against its base
model (i.e., before instruction fine-tuning) MPT30B. We use the same experimental setup as §2.
Figure 10 compares the multi-document QA
performance of MPT-30B and MPT-30B-Instruct
as a function of the position of the relevant in-

[с. 9]
Accuracy

20 Total Retrieved Documents (~4K tokens)

56
54
52
50
48
46
44

1st

5th

10th

15th

20th

Position of Document with the Answer
mpt-30b

mpt-30b-instruct

Figure 10: Multi-document QA performance of MPT30B-Instruct compared against its base model (i.e., before instruction fine-tuning) MPT-30B. Both models
have a U-shaped performance curve, where performance
is much higher when relevant information occurs at the
start or end of the input context, indicating that the
instruction fine-tuning process itself is not necessarily
responsible for these performance trends.

formation in the input context. Surprisingly, we
see that both MPT-30B and MPT-30B-Instruct exhibit a U-shaped performance curve, where performance is highest when relevant information occurs
at the very beginning or very end of the context.
Although the absolute performance of MPT-30BInstruct is uniformly higher than that of MPT-30B,
their overall performance trends are similar. We
also observe that instruction fine-tuning slightly reduces the worst-case performance disparity from
nearly 10% between the base model best- and
worst-case performance to around 4%.
These observations complement prior work,
which found that non-instruction fine-tuned language models are biased towards recent tokens (i.e.,
the end of the input context; Khandelwal et al.,
2018; Press et al., 2021). This recency bias has
been observed in past work when evaluating models on next-word prediction of contiguous text, a
setting where language models minimally benefit
from long-range information (Sun et al., 2021). In
contrast, our results show that language models
are capable of using longer-range information (i.e.,
the beginning of the input context) when prompted
with instruction-formatted data. We hypothesize
that non-instruction fine-tuned language models
learn to use these long contexts from similarlyformatted data that may occur in Internet text seen
during pre-training, e.g., StackOverflow questions

and answers.
To better understand the effect of additional finetuning and model scale, we also experimented
with Llama-2 models of varying sizes (7B, 13B,
and 70B) with and without additional supervised
fine-tuning and reinforcement learning from human feedback (Appendix E). We find that the Ushaped performance curve only appears in sufficiently large language models (with or without additional fine-tuning)—the 7B Llama-2 models are
solely recency biased, while the 13B and 70B models exhibit a U-shaped performance curve. In addition, we see that the Llama-2 supervised fine-tuning
and reinforcement learning from human feedback
procedure slightly mitigates the positional bias in
smaller models (13B, akin to trends shown when
comparing MPT-30B and MPT-30B-Instruct), but
minimally affects trends on larger models (70B).

5

Is More Context Is Always Better?
A Case Study With Open-Domain QA

Our results indicate that prompting language models with longer input contexts is a trade-off—
providing the language model with more information may help it perform the downstream task, but
it also increases the amount of content that the
model must reason over, potentially decreasing
accuracy. Even if a language model can take in
16K tokens, is it actually beneficial to provide 16K
tokens of context? The answer to this question
is ultimately downstream task-specific since it depends on the marginal value of the added context
and the model’s ability to effectively use long input
contexts, but we perform a case study with opendomain question answering on NaturalQuestionsOpen to better understand this trade-off in existing
language models.
We use language models in a standard retrieverreader setup. A retrieval system (Contriever, finetuned on MS-MARCO) takes an input query from
NaturalQuestions-Open and returns the k documents from Wikipedia with the highest relevance
score. To condition language models on these retrieved documents, we simply include them in the
prompt. We evaluate retriever recall and reader
accuracy (whether any of the annotated answers
appear in the predicted output) as a function of the
number of retrieved documents k. We use a subset
of NaturalQuestions-Open where the long answer
is a paragraph (as opposed to a table or a list).
Figure 11 presents retriever recall and open-

