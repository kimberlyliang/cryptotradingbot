## EchoTrade (a Crypto Asset Trading Bot using Twitter Data)

## 📌 Overview  
Predicting crypto markets is challenging—timing is tough, narratives drive speculation, and market sentiment fluctuates rapidly. This project leverages social media data to analyze crypto-related discussions and trends, aiming to improve market timing and trading strategies.  

## 🔍 How It Works  
- **📊 Data Collection**: Aggregates crypto-related tweets to analyze sentiment and emerging narratives.  
- **🤖 Market Analysis**: Uses word analysis to identify trending narratives that may impact crypto prices.  
- **📈 Trading Strategy**: Leverages real-time insights to enhance trading decisions.  

## ⚙️ Trading Strategy Formulation  
This strategy incorporates market data and social sentiment analysis by tracking tweet volume about a given cryptocurrency and comparing it against price movements. The approach is built around three key parameters:

1. **α (Alpha)**: Determines the time lag between a sentiment peak and the corresponding price movement, ensuring trades are executed optimally. It is a constant between 0 and 1, used to optimize the difference between sentiment and price actions.
2. **β (Beta)**: A factor between 0 and 1 that helps determine the optimal early selling time. The goal is to maximize gains by identifying the best exit point before momentum reverses.
3. **γ (Gamma)**: Defines the optimal trade entry point based on cumulative probability functions. The system considers how sentiment builds over time and enters a trade when a sufficient threshold is reached. This is modeled using cumulative distribution functions (CDF) and requires a positive derivative condition for trade execution.

### **Mathematical Formulation:**
1. **Tweet Sentiment Aggregation:**  
   We represent tweet sentiment data as a tensor \( T 	imes 50 \), where each entry consists of ones and zeros indicating whether sentiment is present.
2. **Cumulative Sentiment Calculation:**  
   
   \[
   S(t) = \sum_{i=1}^{N} x_i
   \]
   where \( S(t) \) is the cumulative sentiment at time \( t \), and \( x_i \) represents sentiment scores.

3. **Find Maximum Sentiment and Price Movement:**  
   - Identify the timestamp \( T_s \) corresponding to peak sentiment.
   - Identify the timestamp \( T_p \) corresponding to the maximum price movement.
   - Compute the time difference:

     \[
     \Delta T_o = T_p - T_s
     \]
   - If \( \Delta T_o > 0 \), it indicates that price follows sentiment, allowing for predictive trading.

4. **Trading Execution Condition:**  
   - We define trade execution based on the function:
     \[
     f'(x) = \beta \pm \varepsilon
     \]
     where \( f'(x) \) is the first derivative of price movement, ensuring trades occur during positive price acceleration.

5. **Entry Condition Using Gamma:**  
   - To determine optimal trade entry, we use:
     \[
     \int_{0}^{t} S(t) dt \text{ (cumulative probability function)}
     \]
     ensuring sentiment buildup over time reaches a threshold.
   - The trade is executed when the derivative is positive:
     \[
     \frac{d}{dt} \int S(t) dt > 0
     \]

## 🛠 Getting Started  

### 🔹 Prerequisites  
- AWS CLI installed  
- Python 3.x  
- Required dependencies (to be listed in `requirements.txt`)  

### 🛠 Setup  

1. **Clone the repository:**  
   ```bash  
   git clone https://github.com/your-repo-name.git  
   cd your-repo-name  
   ```  
2. **Download the dataset:**  
   ```bash  
   aws s3 sync s3://user-tweets-991943d5bae2b44ccfb0a711279c8720/ ./local-directory/ --no-sign-request  
   ```  

## 📌 Usage  
1. **Run Find Top 50 Twitter Users**
2. **Run newtweetanalysis.py**
3. **Run cryptodata.py**

## 🌱 Future Work  
- 🔹 Enhance sentiment analysis models  
- 🔹 Integrate real-time trading execution  
- 🔹 Expand data sources to additional social media platforms  

✉️ **Contact:** Feel free to reach out to me at kimliang@seas.upenn.edu for questions!


