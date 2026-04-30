Let's break this down piece by piece. It is a massive project, but when you look at the individual moving parts, it is a highly logical sequence of data processing and graph theory. 

At its core, you are building an economic detective tool to track inflation and market trends. Instead of a social network where nodes are people, your network's nodes are **consumer items** (like a bag of flour, a liter of petrol, or a dozen eggs)[cite: 6]. You want to find out which items secretly "move together" in price across the country.

Here is the slow, step-by-step breakdown of exactly what your python program needs to do.

### Phase 1: The Raw Data (Parsing)
1. **The Source:** You are going to download three years of monthly Consumer Price Index (CPI) data from the PBS website[cite: 11, 12, 14]. 
2. **The Goal:** This data tells you the price of various items in different cities every single month[cite: 11, 12]. You need to parse this data so your program can easily look up: *"What was the price of Milk in Islamabad in March of Year 1?"*

### Phase 2: The Math (Vectors and Similarity)
Now you need to figure out the "price-change pattern" for every item[cite: 21].
1. **Finding the Pattern:** For a specific item in a specific city, calculate how much the price jumped (or dropped) from month to month[cite: 23]. You store these monthly changes as a vector $v_{i,c}^{(y)}=(\Delta p_{i,c}^{(y,2)},\Delta p_{i,c}^{(y,3)},...,\Delta p_{i,c}^{(y,12)})$[cite: 22].
2. **The Matchmaking:** Let's say you want to see if Milk and Petrol are related in a specific city. You take their two price-change vectors and run them through a formula called **Cosine Similarity**[cite: 26, 27]. 
    * If the result is close to 1, their prices rise and fall at the exact same times.
    * If the result is low, they have nothing to do with each other.

### Phase 3: Building the Graph (Nodes and Edges)
You will build three separate undirected graphs, one for each year[cite: 34, 46].
* **The Nodes:** Every item is a node[cite: 20].
* **The Edges:** You only draw an edge (a connection) between Milk and Petrol if their cosine similarity is high enough across a **large number of cities**[cite: 39]. It is not enough if they only match in one city; they need to match nationally based on a user-defined threshold[cite: 38]. 
* **The Weights:** You must also create a weighted version of this graph, where the "thickness" or weight of the edge represents just how perfectly those two items mirror each other[cite: 41, 44].

### Phase 4: Analyzing the Network (Centrality)
Once your C++ algorithms have constructed these graphs, you need to find the "King" of the items—the products that have the biggest ripple effect on the economy. You will use standard graph algorithms for this:
* **Degree Centrality:** Which item is directly connected to the highest number of other items? [cite: 50]
* **Closeness & Betweenness Centrality:** Which items act as bridges between entirely different categories of products? [cite: 51, 52] 
* *(Note: This is where the PageRank PDF comes in. While you are focusing on degree, closeness, and betweenness, understanding Google's PageRank gives you the mathematical foundation for how algorithms score node "importance" using matrices[cite: 148, 154].)*

### Phase 5: Your Deliverables
Based on the specific instructions provided by your instructor, here is what you actually have to hand in:
1. **The Code:** A zipped folder containing all your python source code[cite: 91].
2. **The Presentation:** A slide deck containing the highlights and analysis of your results. The very first slide **must** have your group members' names and roll numbers. 
3. **The Video:** A YouTube link (included in your presentation) to an 8-minute maximum demonstration video. This video needs to visually compare how your graphs change when you tweak the thresholds, and explain how the "central" items shifted over the three years[cite: 81, 83, 86].

Since you will be tackling this entirely in python, how are you currently planning to represent this graph in memory—are you leaning towards an adjacency matrix or an adjacency list for this specific dataset?
