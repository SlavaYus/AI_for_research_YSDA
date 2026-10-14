# Часть 5: с. 13–16

[с. 13]
Ori Ram, Yoav Levine, Itay Dalmedigos, Dor
Muhlgay, Amnon Shashua, Kevin LeytonBrown, and Yoav Shoham. 2023.
Incontext retrieval-augmented language models.
ArXiv:2302.00083.
Ohad Rubin and Jonathan Berant. 2023. Longrange language modeling with self-retrieval.
ArXiv:2306.13421.
Chinnadhurai Sankar, Sandeep Subramanian, Chris
Pal, Sarath Chandar, and Yoshua Bengio. 2019.
Do neural dialog systems use the conversation
history effectively? an empirical study. In Proc.
of ACL.
Timo Schick, Jane Dwivedi-Yu, Roberto Dessì,
Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom.
2023. Toolformer: Language models can teach
themselves to use tools.
Uri Shaham, Maor Ivgi, Avia Efrat, Jonathan Berant, and Omer Levy. 2023. ZeroSCROLLS: A
zero-shot benchmark for long text understanding.
ArXiv:2305.14196.
Vatsal Sharan, Sham Kakade, Percy Liang, and
Gregory Valiant. 2018. Prediction with a short
memory. In Proc. of STOC.
Weijia Shi, Sewon Min, Michihiro Yasunaga, Minjoon Seo, Rich James, Mike Lewis, Luke Zettlemoyer, and Wen tau Yih. 2023. REPLUG:
Retrieval-augmented black-box language models. ArXiv:2301.12652.
Kurt Shuster, Jing Xu, Mojtaba Komeili, Da Ju,
Eric Michael Smith, Stephen Roller, Megan
Ung, Moya Chen, Kushal Arora, Joshua Lane,
Morteza Behrooz, William Ngan, Spencer Poff,
Naman Goyal, Arthur Szlam, Y-Lan Boureau,
Melanie Kambadur, and Jason Weston. 2022.
BlenderBot 3: a deployed conversational agent
that continually learns to responsibly engage.
ArXiv:2208.03188.
Simeng Sun, Kalpesh Krishna, Andrew MattarellaMicke, and Mohit Iyyer. 2021. Do long-range
language models actually use long-range context? In Proc. of EMNLP.
Yi Tay, Mostafa Dehghani, Vinh Q. Tran, Xavier
Garcia, Jason Wei, Xuezhi Wang, Hyung Won
Chung, Siamak Shakeri, Dara Bahri, Tal

Schuster, Huaixiu Steven Zheng, Denny Zhou,
Neil Houlsby, and Donald Metzler. 2023.
UL2: Unifying language learning paradigms.
ArXiv:2205.05131.
Romal Thoppilan, Daniel De Freitas, Jamie Hall,
Noam Shazeer, Apoorv Kulshreshtha, HengTze Cheng, Alicia Jin, Taylor Bos, Leslie
Baker, Yu Du, YaGuang Li, Hongrae Lee,
Huaixiu Steven Zheng, Amin Ghafouri, Marcelo
Menegali, Yanping Huang, Maxim Krikun,
Dmitry Lepikhin, James Qin, Dehao Chen,
Yuanzhong Xu, Zhifeng Chen, Adam Roberts,
Maarten Bosma, Vincent Zhao, Yanqi Zhou,
Chung-Ching Chang, Igor Krivokon, Will Rusch,
Marc Pickett, Pranesh Srinivasan, Laichee Man,
Kathleen Meier-Hellstern, Meredith Ringel Morris, Tulsee Doshi, Renelito Delos Santos, Toju
Duke, Johnny Soraker, Ben Zevenbergen, Vinodkumar Prabhakaran, Mark Diaz, Ben Hutchinson, Kristen Olson, Alejandra Molina, Erin
Hoffman-John, Josh Lee, Lora Aroyo, Ravi
Rajakumar, Alena Butryna, Matthew Lamm,
Viktoriya Kuzmina, Joe Fenton, Aaron Cohen,
Rachel Bernstein, Ray Kurzweil, Blaise AgueraArcas, Claire Cui, Marian Croak, Ed Chi, and
Quoc Le. 2022. LaMDA: Language models for
dialog applications. ArXiv:2201.08239.
Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux,
Timothée Lacroix, Baptiste Rozière, Naman
Goyal, Eric Hambro, Faisal Azhar, Aurelien
Rodriguez, Armand Joulin, Edouard Grave,
and Guillaume Lample. 2023a.
LLaMA:
Open and efficient foundation language models.
ArXiv:2302.13971.
Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei,
Nikolay Bashlykov, Soumya Batra, Prajjwal
Bhargava, Shruti Bhosale, Dan Bikel, Lukas
Blecher, Cristian Canton Ferrer, Moya Chen,
Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn, Saghar Hosseini, Rui Hou,
Hakan Inan, Marcin Kardas, Viktor Kerkez,
Madian Khabsa, Isabel Kloumann, Artem Korenev, Punit Singh Koura, Marie-Anne Lachaux,
Thibaut Lavril, Jenya Lee, Diana Liskovich,
Yinghai Lu, Yuning Mao, Xavier Martinet, Todor
Mihaylov, Pushkar Mishra, Igor Molybog, Yixin

[с. 14]
Ashish Vaswani, Noam Shazeer, Niki Parmar,
Jakob Uszkoreit, Llion Jones, Aidan N. Gomez,
Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. In Proc. of NeurIPS.
Sinong Wang, Belinda Z. Li, Madian Khabsa,
Han Fang, and Hao Ma. 2020.
Linformer: Self-attention with linear complexity.
ArXiv:2006.04768.
Manzil Zaheer, Guru Guruganesh, Kumar Avinava
Dubey, Joshua Ainslie, Chris Alberti, Santiago
Ontanon, Philip Pham, Anirudh Ravula, Qifan
Wang, Li Yang, and Amr Ahmed. 2020. Big
Bird: Transformers for longer sequences. In
Proc. of NeurIPS.

A

Ambiguity in Multi-Document QA
Distractor Documents

Following past work on NaturalQuestions-Open
(Izacard et al., 2021; Izacard and Grave, 2021, inter
alia), we use a Wikipedia dump from late 2018
as our retrieval corpus. However, this standard
Wikipedia dump has a small amount of temporal
mismatch with the NaturalQuestions annotations.
For example, consider the question “what nfl
team does robert griffin iii play for”. The NaturalQuestions annotated answer is “currently a free
agent”. However, the Wikipedia retrieval corpus
contains the information that he plays for the “Baltimore Ravens”, since he was released from the team
between the Wikipedia dump’s timestamp and the
NaturalQuestions annotation process.
We use the ambiguity annotations of Min et al.
(2020) to create a subset unambiguous questions.
Experiments on this unambiguous subset of the
data show similar results and conclusions as the
experiments on the full questions collection (Figure 12).

20 Total Retrieved Documents
(~4K tokens, unambiguous questions)
75

Accuracy

Nie, Andrew Poulton, Jeremy Reizenstein, Rashi
Rungta, Kalyan Saladi, Alan Schelten, Ruan
Silva, Eric Michael Smith, Ranjan Subramanian,
Xiaoqing Ellen Tan, Binh Tang, Ross Taylor,
Adina Williams, Jian Xiang Kuan, Puxin Xu,
Zheng Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan, Melanie Kambadur, Sharan Narang,
Aurelien Rodriguez, Robert Stojnic, Sergey
Edunov, and Thomas Scialom. 2023b. Llama
2: Open foundation and fine-tuned chat models.
ArXiv:2307.09288.

70
65
60
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

Figure 12: Language model performance on a unambiguous subset of questions.

B

Random Distractors in
Multi-Document QA

We also run multi-document question answering
experiments with random Wikipedia documents as
distractors, which allows us to ablate the impact
of retrieved distractors (hard negatives). Note that
in this setting, the the document containing the answer can often be identified with simple heuristics
(e.g., lexical overlap with the query). Figure 13
presents the results of this experiment. Although
all models have higher absolute accuracy in this
setting, they surprisingly still struggle to reason
over their entire input context, indicating that their
performance degradation is not solely due to an
inability to identify relevant documents.

C

Randomizing Distractor Order in
Multi-Document QA

Our prompt instructs the language model to use
the provided search results to answer the question.
There may be a prior in the pre-training or instruction fine-tuning data to treat search results as sorted
by decreasing relevance (i.e., the documents near
the beginning of the input context are more likely to
be useful than those at the end). To validate that our
conclusions are not simply a byproduct of this bias,
we run experiments with the modified instruction
“Write a high-quality answer for the given question using only the provided search results (some
of which might be irrelevant). The search results
are ordered randomly.” In addition, we randomly
shuffle the k − 1 distractor documents.

[с. 15]
20 Total Retrieved Documents
(~4K tokens, random distractors)

75

75

70

70

Accuracy

Accuracy

80

65
1st

5th

10th

15th

20th

Position of Document with the Answer

claude-1.3
claude-1.3-100k
gpt-3.5-turbo-0613

We evaluate GPT-4 (8K) on a subset of 500 random multi-document QA examples with 20 total
documents in each input context (Figure 15). GPT4 achieves higher absolute performance than any
other language model, but still shows a U-shaped
performance curve—its performance is highest
when relevant information occurs at the very start
or end of the context, and performance degrades
when it must use information in the middle of its
input context.

E

Llama-2 Performance

We evaluate Llama-2 (Touvron et al., 2023b) on
multi-document QA with 20 total documents in
each input context. The Llama tokenizer produces longer sequences than the tokenizers for our
previously-studied models, so we discard 20 exam-

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

Figure 14: Language model performance when randomizing the order of the distractors (rather than presenting
them in order of decreasing relevance) and mentioning
as such in the prompt.

90

20 Total Retrieved Documents
(~4K tokens, 500 question sample)

80

Accuracy

GPT-4 Performance

60

1st

Figure 13: Language model performance on multidocument QA when using random distractors, rather
than retrieved distractors.

D

65

55

gpt-3.5-turbo-16k-0613
mpt-30b-instruct
longchat-13b-16k

Figure 14 presents the results of this experiment.
We continue to see a U-shaped performance curve,
with performance degrading when language models must use information in the middle of their
input contexts. Comparing the results in §2.3 with
those when randomizing the distractor order and
mentioning such in the prompt, we see that randomization slightly decreases performance when
the relevant information is at the very beginning
of the context, and slightly increases performance
when using information in the middle and end of
the context.

20 Total Retrieved Documents
(~4K tokens, randomly ordered)

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
gpt-4-0613

Figure 15: Although GPT-4 has higher absolute performance than other models, its performance still degrades
when relevant information occurs in the middle of the
input context.

[с. 16]
20 Total Retrieved Documents (~4K tokens)

70
60

Accuracy

ples (out of 2655) that exceed Llama-2’s maximum
context length of 4096 tokens. We experiment with
models of varying sizes (7B, 13B, and 70B parameters), with and without additional supervised
fine-tuning and reinforcement learning from human feedback (“-chat-” models). The results are
presented in Figure 16.
Comparing Llama-2 models of varying sizes, we
find that only the larger models (13B and 70B)
exhibit the U-shaped performance curve (i.e., both
primacy and recency bias)—the smallest Llama2 models (7B) are solely recency-biased. Given
these results, we hypothesize that prior work (e.g.,
Khandelwal et al., 2018; Sun et al., 2021) did not
previously observe any primacy bias in language
models because the models they studied were too
small (less than 1B parameters).
Comparing between Llama-2 models with and
without additional supervised fine-tuning and reinforcement learning from human feedback, we
see that additional fine-tuning dramatically improves performance on the multi-document QA
task. The 7B models with and without additional
fine-tuning show minimal primacy bias, and are
largely recency-biased. The 13B base model has
a dramatic primacy and recency bias—there is a
20-point accuracy disparity between the best- and
worst-case performance. Applying additional finetuning to the 13B seems to slightly reduce this
bias (10-point worst-case degradation), but the bias
remains significant. However, the 70B models
with and without additional fine-tuning have largely
similar trends (showing both primacy and recency
bias), and additional fine-tuning minimally changes
the positional bias severity.

50
40
30
20

1st

5th

10th

15th

20th

Position of Document with the Answer
Llama-2-7b-chat-hf
Llama-2-13b-chat-hf
Llama-2-70b-chat-hf

Llama-2-7b-hf
Llama-2-13b-hf
Llama-2-70b-hf

Figure 16: Multi-document QA performance (20 total
documents) of Llama-2 models of varying sizes (7B,
13B, 70B parameters), with and without additional supervised fine-tuning and reinforcement learning from
human feedback (“-chat-” models).

