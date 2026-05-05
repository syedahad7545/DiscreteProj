# Item-Level Price Co-Movement Network using CPI Data
**Course:** Discrete Structures
**Prepared by:** Syed Abdul Ahad(25i-0674)
**Prepared by:** Haider Ali Khan(25i-0886)

## 1. Project Objective and Methodology
The objective of this project is to model and analyze the similarity of consumer items based on their price movement patterns across 17 cities in Pakistan spanning three years (2023–2025). Items are represented as nodes, and edges are formed when distinct items exhibit synchronous price changes across a predefined threshold of cities.

For each item $i$ in city $c$ during year $y$, an 11-month price-change vector was computed:
$$v_{i,c}^{(y)}=(\Delta p_{i,c}^{(y,2)},\Delta p_{i,c}^{(y,3)},...,\Delta p_{i,c}^{(y,12)})$$

The Cosine Similarity between any two items within a city was calculated to measure the alignment of their price trajectories:
$$sim_{c}^{(y)}(i,j)=\frac{v_{i,c}^{(y)}\cdot v_{j,c}^{(y)}}{||v_{i,c}^{(y)}||||v_{j,c}^{(y)}||}$$

To handle missing Q1 data for 2023, Backward Linear Extrapolation was applied. An edge was constructed between two items if their cosine similarity exceeded the threshold ($\tau$) in a minimum number of cities ($K$):
$$N_{y}(i,j)=|\{c\in C|sim_{c}^{(y)}(i,j)\ge\tau\}|$$

## 2. Centrality and Temporal Analysis (Unweighted vs. Weighted)
The baseline network was constructed using $\tau=0.85$ and $K=5$. We analyzed both the unweighted network (where all edges above the threshold are treated equally) and a weighted variant (using the average similarity score across valid cities as edge weights).

### 2023: The Extrapolation Echo
*   **Unweighted Top Degree:** Lawn Printed Gul Ahmed/Al Karam (0.2083), Shirting (0.1667), Gents Sponge Chappal Bata (0.1667).
*   **Weighted Top Degree:** Gents Sponge Chappal Bata (3.3466), Ladies Sandal Bata (3.3466), Rice Basmati Broken (3.2413).
*   *Temporal Note:* 2023 generated a highly dense network (26 edges). The dominance of apparel is a mathematical artifact of the Backward Linear Extrapolation used for Q1. Forcing linear trendlines artificially boosted cosine similarity for items with standard, flat price adjustments, creating a "perfect echo" in the network.

### 2024: The Energy Shock
*   **Unweighted Top Degree:** Gas Charges upto 3.3719 MMBTU (0.1818), Ladies Sandal Bata (0.1818), Vegetable Ghee DALDA/HABIB 2.5 kg (0.1818).
*   **Weighted Top Degree:** Ladies Sandal Bata (1.5077), Vegetable Ghee 2.5 kg (1.4863), Vegetable Ghee Pouch (1.3912).
*   *Temporal Note:* The network density dropped to 8 edges as real, jagged market data replaced the extrapolated vectors. Gas Charges emerged as a critical unweighted central node, acting as a structural bridge connecting distinct economic clusters. However, factoring in edge weights reveals that the correlations within the Ghee/Oil cluster were mathematically stronger.

### 2025: The Localized Food Crisis
*   **Unweighted Top Degree:** Vegetable Ghee 2.5 kg Tin (0.3333), Chilies Powder 200 gm (0.2222), Cooking Oil 5 Litre (0.2222).
*   **Weighted Top Degree:** Vegetable Ghee 2.5 kg Tin (1.7992), Cooking Oil 5 Litre (1.1167), Hi-Speed Diesel (0.8599).
*   *Temporal Note:* The network localized entirely around core food staples. Vegetable Ghee's centrality spiked significantly, indicating that cooking oils and spices became the undisputed, localized center of the economic network.

## 3. Category-Based Extension
A connectivity analysis was performed to determine if price shocks breached categorical boundaries. The data reveals a distinct timeline of economic fragmentation:

| Connection Type | 2023 Edges | 2024 Edges | 2025 Edges |
| :--- | :--- | :--- | :--- |
| **Apparel - Apparel** | 8 | 1 | 1 |
| **Apparel - Food** | 6 | 2 | 0 |
| **Food - Food** | 6 | 3 | 5 |
| **Apparel - Personal Care** | 3 | 0 | 0 |
| **Food - Personal Care** | 2 | 0 | 0 |
| **Household - Energy** | 0 | 2 | 0 |
| **Transport - Transport** | 1 | 0 | 1 |

*Analysis:* In 2023 and 2024, cross-category dependencies were present (e.g., Apparel correlating with Food and Personal Care). By 2025, cross-category edges fell to zero. Inflation became strictly isolated within categorical silos, completely aligning the graph clusters with their respective category boundaries.

## 4. Threshold Sensitivity Analysis
To test the robustness of the graph structure, the network was generated under three distinct parameter constraints:

| Scenario | Threshold ($\tau$) | City Count ($K$) | 2023 Edges | 2024 Edges | 2025 Edges |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Loose** | 0.80 | 3 | 78 | 34 | 25 |
| **Baseline** | 0.85 | 5 | 26 | 8 | 7 |
| **Strict** | 0.90 | 8 | 6 | 0 | 1 |

*Analysis:* 
1. **The Strict Scenario:** Raising the parameters ($\tau=0.90, K=8$) destroyed the 2024 network entirely, proving that the economic volatility of that year lacked uniform geographic synchronization. The 6 surviving edges in 2023 further prove the unbreakable nature of the algorithmically imputed Q1 vectors.
2. **The Loose Scenario:** Lowering the parameters ($\tau=0.80, K=3$) resulted in an exponential explosion of edges (e.g., 78 edges in 2023), confirming that at lower thresholds, background economic noise overwhelms the signal, obscuring the primary drivers of inflation.
