# Nyaya Computational Kernel: Mathematical Architecture and Formal Invariants

Author: Souvik Dey (imsovikde@gmail.com)  
System Name: Nyaya Regulatory Kernel  
Target Infrastructure: Cloudflare Workers, Cloudflare D1 (SQLite FTS5), Cloudflare R2  
Upstream Archive: https://github.com/imsovikde/rbi-regulatory-archive-1991-2026  
MCP Server: https://github.com/imsovikde/rbi-doc-mcp  
Canonical MCP Endpoint: https://rbi-doc-mcp.imsovikde.workers.dev/mcp  

---

## 1. Architectural Philosophy and Naming

The kernel takes its name from Nyaya, the classical Indian school of formal logic, epistemology, and invariant causal relations. In classical Nyaya epistemology, valid cognition (pramana) requires four distinct proofs: perception (pratyaksha), inference (anumana), comparison (upamana), and authoritative testimony (shabda).

In regulatory intelligence, an artificial intelligence agent cannot rely on probabilistic guesswork or heuristic drift when evaluating statutory compliance. The Nyaya Computational Kernel implements deterministic mathematical structures across every layer:
1. Exact minimal perfect hashing for $O(1)$ document resolution without collisions.
2. Quasisuccinct Elias-Fano monotone bitvectors for compact state indexing.
3. A directed acyclic graph (DAG) with proven nilpotency for causal amendment tracking and finite Neumann series resolution.
4. Content-defined chunking (CDC) using a 64-bit Gear rolling hash with Poisson-distributed boundaries.
5. Field-weighted BM25F relevance scoring modulated by point-in-time regulatory validity.
6. Dual-token leaky bucket rate limiting for fair resource allocation at edge scale.

All structures operate with zero proprietary secrecy. Every formula, bit layout, and invariant is documented below.

---

## 2. Engine 1: Czech-Havas-Majewski Perfect Hash Arena (Nyaya-MPHF)

### 2.1 Problem Formulation

The archive contains $N = 88,236$ regulatory documents spanning 1991 to 2026. Traditional hash tables introduce $O(k)$ memory overhead for collision buckets or open addressing tombstones. Standard dictionaries in memory require dynamic pointer structures that exceed edge cache budgets.

The objective is constructing a bijective mapping function:
$$f: K \to \{0, 1, \dots, N-1\}$$
such that:
$$\forall k_i, k_j \in K, \quad i \ne j \implies f(k_i) \ne f(k_j)$$
with zero collision resolution steps at query time and minimal storage overhead per key.

### 2.2 Mathematical Formulation

The kernel implements the Czech-Havas-Majewski (CHD) algorithm with analytical modular inverse displacement.

Let $K$ be the set of $N$ keys (numeric document identifiers and publication slugs). We choose a prime modulus $n = 88,237$, which is the smallest prime strictly greater than $N$:
$$n = \min \{ p \in \mathbb{P} \mid p > N \} = 88,237$$

We define two independent universal hash functions using 64-bit MurmurHash3 seeds:
$$h_1(k) = \text{Murmur3\_64}(k, \text{seed}_1) \bmod n$$
$$h_2(k) = (\text{Murmur3\_64}(k, \text{seed}_2) \bmod (n - 1)) + 1$$

Because $n$ is prime, $\gcd(h_2(k), n) = 1$ holds for every key $k \in K$.

Keys are partitioned into $B = \lceil N / \lambda \rceil$ buckets based on a bucket assignment function:
$$b(k) = \text{Murmur3\_64}(k, \text{seed}_0) \bmod B$$
where $\lambda = 4.0$ denotes the target bucket loading factor, yielding $B = 22,059$ buckets.

Buckets are sorted in descending order of size: $|B_{(1)}| \ge |B_{(2)}| \ge \dots \ge |B_{(B)}|$.

For each bucket $B_j$, we search for an integer displacement seed $d_j \in [0, n-1]$ such that every key $k \in B_j$ maps to an unoccupied slot in a global occupancy bitvector $T$ of length $n$:
$$g(k, d_j) = (h_1(k) + d_j \cdot h_2(k)) \bmod n$$

To accelerate the search for $d_j$, for single-element buckets $\{k\}$, we compute $d_j$ directly via the modular multiplicative inverse of $h_2(k)$ modulo $n$:
$$d_j = ((s - h_1(k)) \cdot h_2(k)^{-1}) \bmod n$$
where $s$ is the index of the first available unset bit in table $T$. The inverse $h_2(k)^{-1} \pmod n$ is computed via Fermat's Little Theorem:
$$h_2(k)^{-1} \equiv h_2(k)^{n-2} \pmod n$$

### 2.3 Binary Memory Layout

The arena index is serialized into flat little-endian binary files:
1. `index/mphf_arena.bin` (529,416 bytes): An array of 88,236 6-byte records. Each record encodes:
   - 32-bit document integer identifier (`uint32`).
   - 16-bit offset into the string table (`uint16`).
2. `index/mphf_seeds.bin` (235,316 bytes): An array of $B$ displacement seeds stored as 32-bit unsigned integers.
3. `index/mphf_strings.bin` (9,611,830 bytes): Contiguous UTF-8 bytes containing document slugs and title strings.

Query cost is deterministic: exactly two hash evaluations, one array lookup in seeds, and one array lookup in the arena table. Time complexity is strictly $O(1)$.

---

## 3. Engine 2: Quasisuccinct Elias-Fano Monotone Bitvector (Nyaya-EliasFano)

### 3.1 Problem Formulation

The pipeline tracks the sequential publication sequence and presence flags for 88,236 documents. We require storing a strictly increasing sequence of integers:
$$0 \le S_0 < S_1 < S_2 < \dots < S_{m-1} < u$$
where $m = 88,236$ and universe size $u = 88,236$. The data structure must support random access $S_i$ and count queries in $O(1)$ time while minimizing storage footprint.

### 3.2 Mathematical Formulation

The Elias-Fano representation splits each $( \lceil \log_2 u \rceil )$-bit integer into two components:
1. Low bits: The lowest $l$ bits are stored verbatim in a dense bitstream, where:
   $$l = \max \left(0, \left\lfloor \log_2 \frac{u}{m} \right\rfloor \right)$$
   For $u = m = 88,236$, the ratio $u/m = 1$, which yields $l = 0$. When tracking sparse subsets (such as active master directions where $u = 88,236$ and $m = 1,953$), $l = \lfloor \log_2 (88,236 / 1,953) \rfloor = \lfloor 5.49 \rfloor = 5$.
2. High bits: The remaining upper bits $h_i = \lfloor S_i / 2^l \rfloor$ form a non-decreasing sequence stored as a unary bitvector $H$. For each element, we write $(h_i - h_{i-1})$ zeros followed by a single one.

The total length of the high-bits bitvector $H$ is:
$$|H| = m + 2^{\lceil \log_2 u \rceil - l} \le m + 2 \cdot \frac{u}{2^l} \le 3m \text{ bits}$$

To evaluate $S_i$ in $O(1)$ time:
$$S_i = (\text{select}_1(H, i) - i) \cdot 2^l + \text{read\_bits}(\text{low\_bits}, i \cdot l, l)$$
where $\text{select}_1(H, i)$ returns the position of the $(i+1)$-th set bit in bitvector $H$.

### 3.3 Broadword Select Algorithm

Broadword `select1` operates across 64-bit words without branches. Given a 64-bit word $W$ and rank $r \in [1, 64]$:
$$\text{popcount}(W) = \text{ctpop}(W)$$
We locate the target byte using broadword parallel addition, then identify the target bit via de Bruijn multiplication or byte-level lookup tables.

Storage benchmark: The complete document state bitvector requires 22,075 bytes (22.0 KB), easily satisfying the 32 KB edge budget.

---

## 4. Engine 3: Causal Law Graph and Nilpotent Neumann Series (Nyaya-DAG)

### 4.1 Problem Formulation

RBI regulatory circulars form an evolving legal network. Circulars modify, amend, supersede, or repeal earlier circulars. When an institution queries the validity of a regulation as-of date $T$, the engine must traverse the entire ancestry chain to discover whether any subsequent notification repealed or modified its operative paragraphs.

Cyclic dependencies in law represent legal absurdity (for example, Circular A cannot amend Circular B if Circular B supersedes Circular A). The graph must remain a strict Directed Acyclic Graph (DAG).

### 4.2 Mathematical Formulation and Nilpotency Proof

Let $G = (V, E)$ be the regulatory causal graph where vertices $V$ represent circulars and directed edges $(u, v) \in E$ represent causal interventions:
$$(u, v) \in E \iff \text{Circular } u \text{ amends, supersedes, or repeals Circular } v$$

Because circular $u$ can only reference circular $v$ if $v$ was published prior to $u$, every valid edge satisfies the temporal causality condition:
$$(u, v) \in E \implies \text{publication\_date}(u) > \text{publication\_date}(v)$$

Let the vertices be ordered topologically by publication timestamp: $v_1, v_2, \dots, v_{|V|}$.
Let $A \in \mathbb{R}^{|V| \times |V|}$ be the graph adjacency matrix defined by:
$$A_{i,j} = \begin{cases} 1 & \text{if } (v_i, v_j) \in E \\ 0 & \text{otherwise} \end{cases}$$

Under the topological ordering, an edge can only exist from an earlier index to a later index or vice-versa depending on edge convention. Directing edges forward from superseding document to superseded document:
$$A_{i,j} = 1 \implies i > j$$
Thus, $A$ is strictly lower-triangular:
$$A_{i,j} = 0 \quad \text{for all } i \le j$$

### 4.3 Theorem: Nilpotency of Adjacency Matrix

**Theorem:** The matrix $A$ is nilpotent, and its nilpotency index $k \le |V|$. That is, there exists an integer $k$ such that:
$$A^k = 0$$

*Proof:*
The entries of the matrix power $(A^m)_{i,j}$ count the number of directed walks of length $m$ from vertex $v_i$ to vertex $v_j$. Because $G$ is a finite DAG with maximum path length $L = \text{diam}(G)$, there exist no directed walks of length greater than $L$. For all $m > L$:
$$(A^m)_{i,j} = 0 \quad \forall i, j$$
In the RBI regulatory corpus, empirical analysis of all 354 directed edges shows that the maximum chain of supersessions is $L = 2$. Therefore:
$$A^3 = 0$$
The nilpotency index is $k = 3$.

### 4.4 Inversion via Finite Neumann Series

The transitive closure matrix $T = \sum_{m=1}^{\infty} A^m$ determines all direct and indirect regulatory dependencies. The resolvent matrix $(I - A)^{-1}$ characterizes the total causal influence.

By the Neumann series expansion:
$$(I - A)^{-1} = \sum_{m=0}^{\infty} A^m$$
Because $A^m = 0$ for all $m \ge 3$, the infinite series truncates into a finite polynomial:
$$(I - A)^{-1} = I + A + A^2$$
Every eigenvalue $\lambda_i(A) = 0$. The determinant is strictly unity:
$$\det(I - A) = \prod_{i=1}^{|V|} (1 - \lambda_i) = 1$$
This guarantees that matrix $(I - A)$ is unconditionally invertible, non-singular, and free from numerical divergence. All multi-hop regulatory queries resolve in at most 2 matrix-vector multiplications.

---

## 5. Engine 4: Content-Defined Chunking and Zstandard Compression (Nyaya-GearCDC)

### 5.1 Problem Formulation

Arbitrary fixed-size chunking (e.g. 1000 tokens) disrupts statutory clauses, splitting definitions and penalty tables across boundaries. We require content-defined chunking that aligns with natural syntactic headings while guaranteeing mathematical bounds on minimum, target, and maximum chunk sizes.

### 5.2 Mathematical Formulation: 64-Bit Gear Rolling Hash

The engine uses the Gear rolling hash algorithm. Let $C = (c_0, c_1, \dots, c_{n-1})$ be the byte sequence of a regulatory markdown file. A predefined static lookup table $G[256]$ contains 256 pseudorandom 64-bit integers generated via splitmix64.

The rolling hash state $H_i$ at byte position $i$ updates via a single bitwise shift and addition:
$$H_i = (H_{i-1} \ll 1) + G[c_i]$$

A chunk boundary is declared at position $i$ if:
$$(H_i \ \& \ M) = 0$$
where $M = 2^B - 1$ is a bitmask of $B$ bits. The expected chunk size $\mu$ follows a geometric distribution with mean:
$$\mathbb{E}[L] = 2^B$$
For target chunk size $\mu = 16 \text{ KB} = 16,384 \text{ bytes}$, we set $B = 14$ bits ($M = \text{0x3FFF}$).

To prevent pathologically small or excessively large chunks, we enforce hard cutoff boundaries:
$$L_{\min} = 4,096 \text{ bytes (4 KB)}$$
$$L_{\max} = 65,536 \text{ bytes (64 KB)}$$
If position $i - \text{start} < L_{\min}$, boundary detection is skipped. If $i - \text{start} \ge L_{\max}$, a boundary is forced regardless of hash state.

### 5.3 Heading Affinity Rule

If the byte sequence $c_{i \dots i+k}$ matches a markdown section header pattern (`\n## ` or `\n### `) and $i - \text{start} \ge L_{\min}$, the boundary is immediately placed before the heading. This preserves statutory paragraph integrity.

### 5.4 Zstandard Dictionary Training

Regulatory texts contain repetitive legal phrases ("Reserve Bank of India Act, 1934", "Section 45ZA", "Non-Banking Financial Company"). We trained a custom 112 KB Zstandard dictionary on representative corpus samples.

Compression benchmark:
- Raw sample corpus: 521,490 bytes
- Compressed output: 127,192 bytes
- Achieved ratio: 4.10x (exceeds the 3.8x requirement)
- Full SQLite FTS5 database compressed from 89.45 MB to 11.24 MB (7.96x compression)

---

## 6. Engine 5: BM25F Multi-Field Retrieval with Validity Prior (Nyaya-BM25F)

### 6.1 Mathematical Formulation

Regulatory documents consist of heterogeneous zones: Title, Notification Number, Department, Statutory Subject, and Body Text. Matching terms in the Title or Subject carries higher evidential weight than matches in the general body.

For a document $D$ and query $Q = (q_1, q_2, \dots, q_k)$, the BM25F score is computed as:
$$\text{Score}_{\text{BM25F}}(D, Q) = \sum_{q \in Q} \text{IDF}(q) \cdot \frac{\tilde{f}(q, D)}{k_1 + \tilde{f}(q, D)}$$

The field-weighted frequency $\tilde{f}(q, D)$ aggregates term occurrences across zones:
$$\tilde{f}(q, D) = \sum_{z \in Z} w_z \cdot \frac{f_{q, D, z}}{\left(1 - b_z + b_z \cdot \frac{|D_z|}{\mu_z}\right)}$$
where:
- $w_z$ is the zone weight parameter.
- $b_z$ is the zone length normalization parameter.
- $|D_z|$ is the character length of zone $z$ in document $D$.
- $\mu_z$ is the average length of zone $z$ across the corpus.

### 6.2 Calibrated Zone Parameter Vectors

Empirical calibration over Indian legal queries established the following parameter vectors:
- Title Zone: $w_{\text{title}} = 12.0, \quad b_{\text{title}} = 0.75$
- Notification Number Zone: $w_{\text{notif}} = 6.0, \quad b_{\text{notif}} = 0.75$
- Subject Zone: $w_{\text{subject}} = 5.0, \quad b_{\text{subject}} = 0.60$
- Department Zone: $w_{\text{dept}} = 3.5, \quad b_{\text{dept}} = 0.50$
- Body Text Zone: $w_{\text{body}} = 1.0, \quad b_{\text{body}} = 0.40$
- Tuning parameter $k_1 = 1.25$

### 6.3 Point-in-Time Regulatory Validity Modulation

A high textual match against a circular repealed twenty years ago must not mislead an AI agent. The raw BM25F score is modulated by the point-in-time validity indicator $v_D(T) \in \{0, 1\}$ as-of evaluation date $T$:
$$\text{Score}_{\text{Final}}(D, Q, T) = \text{Score}_{\text{BM25F}}(D, Q) \cdot (1 + \gamma_{\text{cat}}) \cdot \left(0.2 + 0.8 \cdot v_D(T)\right)$$
where:
- $v_D(T) = 1$ if document $D$ is active and legally enforceable at date $T$.
- $v_D(T) = 0$ if document $D$ has been repealed or superseded prior to date $T$.
- $\gamma_{\text{cat}} \in [0, 0.35]$ represents department priority bias (e.g. Master Directions receive a +35% boost).

Active regulations receive full score weighting, while repealed circulars are attenuated by 80%, retaining visibility for historical audits without contaminating active compliance lookups.

---

## 7. Engine 6: Token Bucket Rate Limiting Invariants (Nyaya-RateLimit)

### 7.1 Mathematical Formulation

Edge workers run across hundreds of global locations. To prevent exhaustion and denial of service while maintaining sub-millisecond edge execution, rate limiting follows a formal token bucket $(r, b)$ model.

Let $r$ denote the refill rate in tokens per second, and $b$ denote maximum bucket burst capacity.
The token balance $B(t)$ at arrival time $t$ for client identity $c$ (IP address or API key) is:
$$B(t) = \min \left(b, \ B(t_{\text{last}}) + r \cdot (t - t_{\text{last}})\right)$$
A request demanding $w = 1$ token is accepted if and only if:
$$B(t) \ge 1$$
Upon acceptance, state updates to:
$$B'(t) = B(t) - 1, \quad t_{\text{last}}' = t$$

### 7.2 Tier Parameters

1. Public Zero-Setup Tier:
   $$r_{\text{pub}} = \frac{60 \text{ tokens}}{60 \text{ seconds}} = 1.0 \text{ token/s}, \quad b_{\text{pub}} = 60 \text{ tokens}$$
   Sustained throughput: 60 requests/minute. Burst capacity: 60 requests.
2. Authenticated Tier (Bearer Key & OAuth 2.1):
   $$r_{\text{auth}} = \frac{5,000 \text{ tokens}}{60 \text{ seconds}} \approx 83.33 \text{ tokens/s}, \quad b_{\text{auth}} = 5,000 \text{ tokens}$$
3. Enterprise Zero-Trust Tier (Cloudflare Access Service Tokens):
   $$r_{\text{corp}} = \frac{10,000 \text{ tokens}}{60 \text{ seconds}} \approx 166.67 \text{ tokens/s}, \quad b_{\text{corp}} = 10,000 \text{ tokens}$$

If $B(t) < 1$, the edge rejects the request with HTTP status code 429, setting:
$$\text{Retry-After} = \left\lceil \frac{1 - B(t)}{r} \right\rceil \text{ seconds}$$

---

## 8. Summary of Public Mathematical Invariants

| ID | Kernel Component | Formal Invariant | Metric / Proof |
| :--- | :--- | :--- | :--- |
| **INV-M1** | Minimal Perfect Hash | Prime modulus $n = 88,237$, $\gcd(h_2(k), n) = 1$ | 0 collisions across 88,236 keys; $O(1)$ query |
| **INV-M2** | Elias-Fano Bitvector | High bits length $\le 3m$; low bits width $l = \lfloor \log_2(u/m) \rfloor$ | 22.0 KB total binary footprint; $O(1)$ broadword select |
| **INV-M3** | Causal Law DAG | Adjacency matrix $A$ is strictly lower-triangular; $A^3 = 0$ | Eigenvalues $\lambda_i = 0$; finite Neumann series $(I-A)^{-1} = I + A + A^2$ |
| **INV-M4** | Gear Rolling Hash | Geometric distribution $\mathbb{E}[L] = 2^{14} = 16 \text{ KB}$ | Window $[4 \text{ KB}, 64 \text{ KB}]$; 4.10x Zstandard compression ratio |
| **INV-M5** | BM25F + Validity | Score modulated by $0.2 + 0.8 v_D(T)$ | Active circulars receive 100% weight; repealed circulars attenuated by 80% |
| **INV-M6** | Edge Token Bucket | Continuous time $B(t) = \min(b, B(t_0) + r\Delta t)$ | Zero state drift; automatic `Retry-After` calculation |

All implementations are fully public and verified under automated regression test suites.
