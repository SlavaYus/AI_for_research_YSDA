# Часть 4: с. 10–12

[с. 10]
90

Metric

80
70
60
50
5 10

20

30

40

Number of Retrieved Docs

claude-1.3
claude-1.3-100k
gpt-3.5-turbo-0613
gpt-3.5-turbo-16k-0613

50

mpt-30b-instruct
longchat-13b-16k
contriever recall

Figure 11: Retriever recall and model performance as a
function of the number of retrieved documents. Model
performance saturates long before retriever recall, indicating that the models have difficulty making use of the
extra retrieved documents.

domain QA results. We see that reader model
performance saturates long before retriever performance saturates, indicating that readers are not
effectively using the extra context. Using more
than 20 retrieved documents only marginally improves reader performance (∼1.5% for GPT-3.5Turbo and ∼1% for Claude-1.3), while significantly
increasing the input context length (and thus latency and cost). These results, coupled with the
observation that models are often better at retrieving and using information at the start or end of
the input contexts, suggest that effective reranking of retrieved documents (pushing relevant information closer to the start of the input context) or
ranked list truncation (retrieving fewer documents
when appropriate; Arampatzis et al., 2009) may be
promising directions for improving how languagemodel-based readers use retrieved context.

6

Related Work

6.1

Long-Context Language Models

There is much prior work in designing performant
language models with cheaper scaling than Transformers in the context length. Many lines of work
pursue Transformer variants with attention modifications like recurrence (Dai et al., 2019), factorizing attention into computationally less intensive
approximations (Beltagy et al., 2020; Zaheer et al.,
2020), or low-rank approximations (Wang et al.,
2020; Peng et al., 2021). Dao et al. (2022) instead provide a faster exact attention by a carefully-

crafted IO-aware CUDA kernel. Separately, there
are attempts to do away with attention entirely to
remove quadratic sequence length complexity, often through convolution and/or linear RNNs, e.g.,
in RWKV (Peng, 2023), S4 (Gu et al., 2022), or
Hyena (Poli et al., 2023). Many prior efforts evaluate perplexity on a diverse web corpus as a proxy
for the ability to process long contexts; this work
shows that precise knowledge access on long contexts may be an added challenge.
6.2

How Do Language Models Use Context?

The pioneering work of Khandelwal et al. (2018)
showed that small LSTM language models make
increasingly coarse use of longer-term context;
Sankar et al. (2019) found similar results in dialogue models. In a similar vein, Daniluk et al.
(2017) find that attentive LSTM language models tend to mainly use recent history. Petroni
et al. (2020) were among the first to demonstrate
the potential of combining context from an information retrieval system with a pretrained language models for unsupervised question answering.
O’Connor and Andreas (2021) found that many
information-destroying operations had marginal effects on Transformer LMs’ predictions. Krishna
et al. (2022) found that long-context neural generation in modestly-sized Transformer language
models degenerates because models fail to properly condition on long context. Finally, studying
long-context models, Sun et al. (2021) found that
longer contexts improves prediction of only a few
tokens, an empirical finding consistent with the
theory of Sharan et al. (2018), who showed that
sequence distributions with bounded mutual information necessarily lead to marginal average prediction benefits from increasingly long context. Qin
et al. (2023) analyze how efficient Transformers
perform on a variety of long-context downstream
NLP tasks, finding that long-context transformers
are recency-biased and do not effectively use longrange context.
6.3

The Serial-Position Effect

The U-shaped curve we observe in this work has
a connection in psychology known as the serialposition effect (Ebbinghaus, 1913; Murdock Jr,
1962), that states that in free-association recall
of elements from a list, humans tend to best remember the first and last elements of the list. The
serial-position effect plays a role in understanding
how humans develop short- and long-term mem-

[с. 11]
ory. Observing a serial-position-like effect in language models is perhaps surprising, since the selfattention mechanisms underlying Transformer language models is technically equally capable of retrieving any token from their contexts.

7

Conclusion

We empirically study how language models use
long input contexts via a series of controlled experiments. We show that language model performance degrades significantly when changing the
position of relevant information, indicating that
models struggle to robustly access and use information in long input contexts. In particular, performance is often lowest when models must use
information in the middle of long input contexts.
We conduct a preliminary investigation of the role
of (i) model architecture, (ii) query-aware contextualization, and (iii) instruction fine-tuning to better
understand how they affect how language models
use context. Finally, we conclude with a practical case study of open-domain question answering,
finding that the performance of language model
readers saturates far before retriever recall. Our
results and analysis provide a better understanding
of how language models use their input context
and provides new evaluation protocols for future
long-context models.

Acknowledgments
We would like to thank Luke Zettlemoyer, who
served as our TACL action editor, and the the
anonymous reviewers for their comments and feedback. We also thank Claudiu Leoveanu-Condrei,
Megan Leszczynski, Dmytro Okhonko, Maithra
Raghu, Eric Wallace and Sang Michael Xie for
feedback and discussions that helped improve this
work. Further, we are grateful to Sewon Min for
her help with the AmbigQA dataset. This work
was supported by the Stanford Center for Research
on Foundation Models (CRFM), by OpenAI via
an API credits grant to the Stanford CRFM, and
by Anthropic via the Claude academic access program.

References
Avi Arampatzis, Jaap Kamps, and Stephen Robertson. 2009. Where to stop reading a ranked list?
threshold optimization using truncated score distributions. In Proc. of SIGIR.

Iz Beltagy, Matthew E. Peters, and Arman Cohan.
2020. Longformer: The long-document transformer. ArXiv:2004.05150.
Hyung Won Chung, Le Hou, Shayne Longpre, Barret Zoph, Yi Tay, William Fedus, Yunxuan Li,
Xuezhi Wang, Mostafa Dehghani, Siddhartha
Brahma, Albert Webson, Shixiang Shane Gu,
Zhuyun Dai, Mirac Suzgun, Xinyun Chen,
Aakanksha Chowdhery, Alex Castro-Ros, Marie
Pellat, Kevin Robinson, Dasha Valter, Sharan
Narang, Gaurav Mishra, Adams Yu, Vincent
Zhao, Yanping Huang, Andrew Dai, Hongkun
Yu, Slav Petrov, Ed H. Chi, Jeff Dean, Jacob
Devlin, Adam Roberts, Denny Zhou, Quoc V.
Le, and Jason Wei. 2022. Scaling instructionfinetuned language models. ArXiv:2210.11416.
Zihang Dai, Zhilin Yang, Yiming Yang, Jaime
Carbonell, Quoc Le, and Ruslan Salakhutdinov.
2019. Transformer-XL: Attentive language models beyond a fixed-length context. In Proc. of
ACL.
Michał Daniluk, Tim Rocktäschel, Johannes Welbl,
and Sebastian Riedel. 2017. Frustratingly short
attention spans in neural language modeling. In
Proc. of ICLR.
Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra,
and Christopher Ré. 2022. FlashAttention: Fast
and memory-efficient exact attention with IOawareness. ArXiv:2205.14135.
Hermann Ebbinghaus. 1913. Memory: A contribution to experimental psychology. H. A. Ruger &
C. E. Bussenius, Trans.
Albert Gu, Karan Goel, and Christopher Ré. 2022.
Efficiently modeling long sequences with structured state spaces. In Proc. of ICLR.
Maor Ivgi, Uri Shaham, and Jonathan Berant. 2023.
Efficient long-text understanding with short-text
models. Transactions of the Association for
Computational Linguistics, 11:284–299.
Gautier Izacard, Mathilde Caron, Lucas Hosseini,
Sebastian Riedel, Piotr Bojanowski, Armand
Joulin, and Edouard Grave. 2021. Unsupervised
dense information retrieval with contrastive
learning. ArXiv:2112.09118.
Gautier Izacard and Edouard Grave. 2021. Leveraging passage retrieval with generative models

[с. 12]
for open domain question answering. In Proc.
of EACL.
Nikhil Kandpal, Haikang Deng, Adam Roberts,
Eric Wallace, and Colin Raffel. 2022. Large language models struggle to learn long-tail knowledge. ArXiv:2211.08411.
Urvashi Khandelwal, He He, Peng Qi, and Dan
Jurafsky. 2018. Sharp nearby, fuzzy far away:
How neural language models use context. In
Proc. of ACL.
Kalpesh Krishna, Yapei Chang, John Wieting, and
Mohit Iyyer. 2022. RankGen: Improving text
generation with large ranking models. In Proc.
of EMNLP.
Tom Kwiatkowski, Jennimaria Palomaki, Olivia
Redfield, Michael Collins, Ankur Parikh, Chris
Alberti, Danielle Epstein, Illia Polosukhin, Jacob
Devlin, Kenton Lee, Kristina Toutanova, Llion
Jones, Matthew Kelcey, Ming-Wei Chang, Andrew M. Dai, Jakob Uszkoreit, Quoc Le, and
Slav Petrov. 2019. Natural Questions: A benchmark for question answering research. Transactions of the Association for Computational
Linguistics, 7:452–466.
Kenton Lee, Ming-Wei Chang, and Kristina
Toutanova. 2019. Latent retrieval for weakly
supervised open domain question answering. In
Proc. of ACL.
Mina Lee, Percy Liang, and Qian Yang. 2022.
CoAuthor: Designing a human-AI collaborative
writing dataset for exploring language model capabilities. In Proc. of CHI.

Bennet B. Murdock Jr. 1962. The serial position
effect of free recall. Journal of experimental
psychology, 64(5):482.
Joe O’Connor and Jacob Andreas. 2021. What context features can Transformer language models
use? In Proc. of ACL.
Dimitris Papailiopoulos, Kangwook Lee, and Jyyong Sohn. 2023. A little retrieval test for
large language models. https://github.com/
anadim/the-little-retrieval-test.
Bo Peng. 2023. RWKV-LM. https://github.
com/BlinkDL/RWKV-LM.
Hao Peng, Nikolaos Pappas, Dani Yogatama, Roy
Schwartz, Noah Smith, and Lingpeng Kong.
2021. Random feature attention. In Proc. of
ICLR.
Fabio Petroni, Patrick Lewis, Aleksandra Piktus,
Tim Rocktäschel, Yuxiang Wu, Alexander H
Miller, and Sebastian Riedel. 2020. How context
affects language models’ factual predictions. In
Proc. of AKBC.
Michael Poli, Stefano Massaroli, Eric Nguyen,
Daniel Y. Fu, Tri Dao, Stephen Baccus, Yoshua
Bengio, Stefano Ermon, and Christopher Ré.
2023. Hyena hierarchy: Towards larger convolutional language models. In Proc. of ICML.
Ofir Press, Noah A. Smith, and Mike Lewis. 2021.
Shortformer: Better language modeling using
shorter inputs. In Proc. of ACL.

Dacheng Li, Rulin Shao, Anze Xie, Ying Sheng,
Lianmin Zheng, Joseph E. Gonzalez, Ion Stoica,
Xuezhe Ma, , and Hao Zhang. 2023. How long
can open-source LLMs truly promise on context
length?

Ofir Press, Noah A. Smith, and Mike Lewis. 2022.
Train short, test long: Attention with linear biases enables input length extrapolation. In Proc.
of ICLR.

Alex Mallen, Akari Asai, Victor Zhong, Rajarshi
Das, Daniel Khashabi, and Hannaneh Hajishirzi.
2023. When not to trust language models: Investigating effectiveness of parametric and nonparametric memories. In Proc. of ACL.

Guanghui Qin, Yukun Feng, and Benjamin
Van Durme. 2023. The NLP task effectiveness
of long-range transformers. In Proc. of EACL.

Sewon Min, Julian Michael, Hannaneh Hajishirzi,
and Luke Zettlemoyer. 2020. AmbigQA: Answering ambiguous open-domain questions. In
Proc. of EMNLP.

Colin Raffel, Noam Shazeer, Adam Roberts,
Katherine Lee, Sharan Narang, Michael Matena,
Yanqi Zhou, Wei Li, and Peter J. Liu. 2020. Exploring the limits of transfer learning with a unified text-to-text Transformer. Journal of Machine Learning Research, 21(140):1–67.

