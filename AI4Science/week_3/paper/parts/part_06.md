# Часть 6: с. 17–18

[с. 17]
F

Token Counts

Table 2, Table 3, and Table 4 present the average and maximum number of tokens in each of the input
contexts for all experimental settings. Note that MPT-30B and MPT-30B-Instruct use the same tokenizer,
GPT-3.5-Turbo and GPT-3.5-Turbo (16K) use the same tokenizer, and Claude-1.3 and Claude-1.3 (100K)
use the same tokenizer. Furthermore, the Claude-1.3 tokenizer is the same as the GPT-3.5-Turbo tokenizer,
modulo some additional special tokens that do not appear in our data. As a result, the token counts for
these two model families is the same in our experimental settings.
Closed-Book

LongChat-13B (16K)
MPT-30B
GPT-3.5-Turbo
Claude-1.3

Oracle

avg ± stdev

max

avg ± stdev

max

55.6 ± 2.7
43.5 ± 2.2
15.3 ± 2.2
15.3 ± 2.2

70
58
29
29

219.7 ± 48.5
187.9 ± 41.8
156.0 ± 41.8
156.0 ± 41.8

588
482
449
449

Table 2: Token count statistics for each of the evaluated models on the closed-book and oracle multi-document
question answering settings.

10 docs

LongChat-13B (16K)
MPT-30B
GPT-3.5-Turbo
Claude-1.3

20 docs

30 docs

avg ± stdev

max

avg ± stdev

max

avg ± stdev

max

1749.9 ± 112.4
1499.7 ± 88.5
1475.6 ± 86.5
1475.6 ± 86.5

2511
1907
1960
1960

3464.6 ± 202.3
2962.4 ± 158.4
2946.2 ± 155.1
2946.2 ± 155.1

4955
3730
3920
3920

5181.9 ± 294.7
4426.9 ± 230.5
4419.2 ± 226.5
4419.2 ± 226.5

7729
5475
6101
6101

Table 3: Token count statistics for each of the evaluated models on each of the document question answering
settings.

75 KV pairs

LongChat-13B (16K)
MPT-30B
GPT-3.5-Turbo
Claude-1.3

140 KV pairs

300 KV pairs

avg ± stdev

max

avg ± stdev

max

avg ± stdev

max

5444.5 ± 19.1
4110.5 ± 23.8
3768.7 ± 25.6
3768.7 ± 25.6

5500
4187
3844
3844

10072.4 ± 24.1
7600.9 ± 31.1
6992.8 ± 34.1
6992.8 ± 34.1

10139
7687
7088
7088

21467.3 ± 35.9
16192.4 ± 46.6
14929.4 ± 50.7
14929.4 ± 50.7

21582
16319
15048
15048

Table 4: Token count statistics for each of the evaluated models on each of the key-value (KV) retrieval settings.

[с. 18]
G

Full Multi-Document Question Answering Results

This section tabulates model performance when evaluated on the multi-document QA task with varying
numbers of documents (Figure 5). “Index n” indicates performance when the document with the answer
occurs at position n + 1, where lower indices are closer to the start of the input context. For example,
index 0 refers to performance when the document with the answer is placed at the very start of the context
(i.e., first amongst all documents).
G.1

10 Total Retrieved Documents
Model

Index 0

Index 4

Index 9

Claude-1.3
Claude-1.3 (100K)
GPT-3.5-Turbo
GPT-3.5-Turbo (16K)
MPT-30B-Instruct
LongChat-13B (16K)

62.9%
63.1%
76.8%
76.9%
60.2%
72.1%

58.3%
58.3%
61.2%
61.0%
56.2%
58.9%

59.7%
59.7%
62.4%
62.5%
59.7%
58.5%

Table 5: Model performance when evaluated on the multi-document QA task with 10 total retrieved documents.

G.2

20 Total Retrieved Documents
Model

Index 0

Index 4

Index 9

Index 14

Index 19

Claude-1.3
Claude-1.3 (100K)
GPT-3.5-Turbo
GPT-3.5-Turbo (16K)
MPT-30B-Instruct
LongChat-13B (16K)

59.9%
59.8%
75.8%
75.7%
53.7%
68.6%

55.9%
55.9%
57.2%
57.3%
51.8%
57.4%

56.8%
57.0%
53.8%
54.1%
52.2%
55.3%

57.2%
57.4%
55.4%
55.4%
52.7%
52.5%

60.1%
60.0%
63.2%
63.1%
56.3%
55.0%

Table 6: Model performance when evaluated on the multi-document QA task with 20 total retrieved documents.

G.3

30 Total Retrieved Documents

Model

Index 0

Index 4

Index 9

Index 14

Index 19

Index 24

Index 29

Claude-1.3
Claude-1.3 (100K)
GPT-3.5-Turbo (16K)
MPT-30B-Instruct
LongChat-13B (16K)

59.1%
59.1%
73.4%
51.6%
66.9%

55.1%
55.1%
55.1%
51.3%
54.8%

54.8%
54.9%
50.5%
51.2%
52.5%

55.7%
55.7%
50.9%
49.0%
52.9%

56.4%
56.6%
51.8%
49.6%
52.2%

56.2%
56.1%
54.9%
51.3%
51.3%

59.9%
60.0%
63.7%
54.1%
55.1%

Table 7: Model performance when evaluated on the multi-document QA task with 30 total retrieved documents.

