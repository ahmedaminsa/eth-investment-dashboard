// ETH Investment Dashboard - Live Data Integration
// This script fetches real-time ETH data and updates the dashboard

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyA8y0stKPG3jqHNi6555bLLH6oNb4Ko8xs",
  authDomain: "eth-investment-457013.firebaseapp.com",
  projectId: "eth-investment-457013",
  storageBucket: "eth-investment-457013.firebasestorage.app",
  messagingSenderId: "494559261943",
  appId: "1:494559261943:web:0099f6f8f9b4c03e7dcff2",
  measurementId: "G-LFD1F3FM4G"
};

// Initialize Firebase
document.addEventListener('DOMContentLoaded', function() {
  // Initialize Firebase using the compat version for simpler integration
  firebase.initializeApp(firebaseConfig);
  if (firebase.analytics) {
    firebase.analytics();
  }
  
  console.log("ETH Investment Dashboard - Firebase Initialized");
  
  // Fetch ETH price data and update dashboard
  updateDashboard();
  
  // Set up automatic refresh every 5 minutes
  setInterval(updateDashboard, 5 * 60 * 1000);
  
  // Set up event listeners
  document.getElementById('refreshButton')?.addEventListener('click', function() {
    updateDashboard();
  });
});

// Main function to update the dashboard with live data
async function updateDashboard() {
  try {
    // Show loading indicator
    showLoading(true);
    
    // Fetch ETH price data from CoinGecko API
    const ethData = await fetchEthData();
    
    // Update price display
    updatePriceDisplay(ethData);
    
    // Calculate technical indicators
    const technicalData = calculateTechnicalIndicators(ethData);
    
    // Update technical analysis display
    updateTechnicalDisplay(technicalData);
    
    // Generate investment recommendation
    const recommendation = generateRecommendation(technicalData);
    
    // Update recommendation display
    updateRecommendationDisplay(recommendation);
    
    // Calculate risk management parameters
    const riskParams = calculateRiskParameters(ethData, recommendation);
    
    // Update risk management display
    updateRiskDisplay(riskParams);
    
    // Update last updated timestamp
    updateTimestamp();
    
    // Hide loading indicator
    showLoading(false);
    
    console.log("Dashboard updated successfully with live data");
    
  } catch (error) {
    console.error("Error updating dashboard:", error);
    showError("Failed to update dashboard. Please try again later.");
    showLoading(false);
  }
}

// Fetch ETH price data from CoinGecko API
async function fetchEthData() {
  // CoinGecko API endpoint for ETH data
  const url = "https://api.coingecko.com/api/v3/coins/ethereum?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false";
  
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch ETH data: ${response.status}`);
  }
  
  const data = await response.json();
  
  // Extract relevant price data
  return {
    currentPrice: data.market_data.current_price.usd,
    priceChange24h: data.market_data.price_change_percentage_24h,
    priceChange7d: data.market_data.price_change_percentage_7d,
    priceChange30d: data.market_data.price_change_percentage_30d,
    marketCap: data.market_data.market_cap.usd,
    volume24h: data.market_data.total_volume.usd,
    high24h: data.market_data.high_24h.usd,
    low24h: data.market_data.low_24h.usd
  };
}

// Update price display with live data
function updatePriceDisplay(ethData) {
  // Update current price
  const priceElement = document.querySelector('.card:nth-child(1) .card-body h2');
  if (priceElement) {
    priceElement.textContent = `$${ethData.currentPrice.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    
    // Update price color based on 24h change
    if (ethData.priceChange24h >= 0) {
      priceElement.className = 'price-up';
    } else {
      priceElement.className = 'price-down';
    }
  }
  
  // Update 24h change percentage
  const changeElement = document.querySelector('.card:nth-child(1) .card-body p');
  if (changeElement) {
    const changePrefix = ethData.priceChange24h >= 0 ? '+' : '';
    changeElement.textContent = `${changePrefix}${ethData.priceChange24h.toFixed(2)}% (24h)`;
    
    // Update change color
    if (ethData.priceChange24h >= 0) {
      changeElement.className = 'price-up';
    } else {
      changeElement.className = 'price-down';
    }
  }
}

// Calculate technical indicators based on price data
function calculateTechnicalIndicators(ethData) {
  // In a real implementation, we would use historical price data
  // to calculate these indicators. For this demo, we'll use simplified logic.
  
  // RSI (Relative Strength Index)
  // Simplified calculation: RSI based on price change percentages
  let rsi = 50; // Neutral starting point
  if (ethData.priceChange24h > 0) {
    rsi += ethData.priceChange24h * 1.5; // Increase RSI for positive price change
  } else {
    rsi += ethData.priceChange24h * 1.5; // Decrease RSI for negative price change
  }
  
  // Ensure RSI stays within 0-100 range
  rsi = Math.max(0, Math.min(100, rsi));
  
  // MACD (Moving Average Convergence Divergence)
  // Simplified: Determine MACD signal based on short vs long term trends
  const macdSignal = ethData.priceChange24h > ethData.priceChange7d ? "Bullish Crossover" : 
                     ethData.priceChange24h < ethData.priceChange7d ? "Bearish Crossover" : 
                     "Neutral";
  
  // Moving Averages
  // Simplified: Compare current price to hypothetical moving averages
  const ma50Status = ethData.priceChange7d > 0 ? "Above" : "Below";
  
  // Support and Resistance Levels
  // Simplified: Calculate based on recent highs and lows
  const supportLevel = ethData.low24h * 0.98; // 2% below recent low
  const resistanceLevel = ethData.high24h * 1.02; // 2% above recent high
  
  return {
    rsi,
    macdSignal,
    ma50Status,
    supportLevel,
    resistanceLevel
  };
}

// Update technical analysis display
function updateTechnicalDisplay(technicalData) {
  // Update RSI
  const rsiElement = document.querySelector('.card-header:contains("Technical Analysis") + .card-body p:nth-child(1)');
  if (rsiElement) {
    let rsiStatus = "Neutral";
    if (technicalData.rsi > 70) rsiStatus = "Overbought";
    else if (technicalData.rsi < 30) rsiStatus = "Oversold";
    
    rsiElement.innerHTML = `<strong>RSI:</strong> ${technicalData.rsi.toFixed(0)} (${rsiStatus})`;
  }
  
  // Update MACD
  const macdElement = document.querySelector('.card-header:contains("Technical Analysis") + .card-body p:nth-child(2)');
  if (macdElement) {
    macdElement.innerHTML = `<strong>MACD:</strong> ${technicalData.macdSignal}`;
  }
  
  // Update Moving Averages
  const maElement = document.querySelector('.card-header:contains("Technical Analysis") + .card-body p:nth-child(3)');
  if (maElement) {
    maElement.innerHTML = `<strong>Moving Averages:</strong> ${technicalData.ma50Status} 50-day MA`;
  }
  
  // Update Support Level
  const supportElement = document.querySelector('.card-header:contains("Technical Analysis") + .card-body p:nth-child(4)');
  if (supportElement) {
    supportElement.innerHTML = `<strong>Support Level:</strong> $${technicalData.supportLevel.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
  }
  
  // Update Resistance Level
  const resistanceElement = document.querySelector('.card-header:contains("Technical Analysis") + .card-body p:nth-child(5)');
  if (resistanceElement) {
    resistanceElement.innerHTML = `<strong>Resistance Level:</strong> $${technicalData.resistanceLevel.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
  }
}

// Generate investment recommendation based on technical analysis
function generateRecommendation(technicalData) {
  let signal = "HOLD"; // Default recommendation
  let reason = "Technical indicators are neutral";
  
  // RSI-based signals
  if (technicalData.rsi > 70) {
    signal = "SELL";
    reason = "RSI indicates overbought conditions";
  } else if (technicalData.rsi < 30) {
    signal = "BUY";
    reason = "RSI indicates oversold conditions";
  }
  
  // MACD-based signals (override RSI if stronger signal)
  if (technicalData.macdSignal === "Bullish Crossover") {
    signal = "BUY";
    reason = "MACD shows bullish crossover";
  } else if (technicalData.macdSignal === "Bearish Crossover") {
    signal = "SELL";
    reason = "MACD shows bearish crossover";
  }
  
  return {
    signal,
    reason
  };
}

// Update recommendation display
function updateRecommendationDisplay(recommendation) {
  // Update recommendation signal
  const signalElement = document.querySelector('.card:nth-child(2) .card-body h3');
  if (signalElement) {
    signalElement.textContent = recommendation.signal;
    
    // Update signal color
    if (recommendation.signal === "BUY") {
      signalElement.className = 'price-up';
    } else if (recommendation.signal === "SELL") {
      signalElement.className = 'price-down';
    } else {
      signalElement.className = '';
    }
  }
  
  // Update recommendation reason
  const reasonElement = document.querySelector('.card:nth-child(2) .card-body p');
  if (reasonElement) {
    reasonElement.textContent = recommendation.reason;
  }
}

// Calculate risk management parameters
function calculateRiskParameters(ethData, recommendation) {
  // Calculate stop loss (2% below current price for BUY, 2% above for SELL)
  let stopLoss = recommendation.signal === "BUY" ? 
                 ethData.currentPrice * 0.98 : 
                 recommendation.signal === "SELL" ? 
                 ethData.currentPrice * 1.02 : 
                 ethData.currentPrice * 0.95;
  
  // Calculate take profit (3% above current price for BUY, 3% below for SELL)
  let takeProfit = recommendation.signal === "BUY" ? 
                  ethData.currentPrice * 1.03 : 
                  recommendation.signal === "SELL" ? 
                  ethData.currentPrice * 0.97 : 
                  ethData.currentPrice * 1.05;
  
  // Calculate position size (simplified)
  // In a real implementation, this would consider account balance, risk tolerance, etc.
  const positionSize = 0.5; // Fixed at 0.5 ETH for this demo
  
  return {
    stopLoss,
    takeProfit,
    positionSize
  };
}

// Update risk management display
function updateRiskDisplay(riskParams) {
  // Update stop loss
  const stopLossElement = document.querySelector('.card:nth-child(3) .card-body p:nth-child(1)');
  if (stopLossElement) {
    stopLossElement.innerHTML = `<strong>Stop Loss:</strong> $${riskParams.stopLoss.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
  }
  
  // Update take profit
  const takeProfitElement = document.querySelector('.card:nth-child(3) .card-body p:nth-child(2)');
  if (takeProfitElement) {
    takeProfitElement.innerHTML = `<strong>Take Profit:</strong> $${riskParams.takeProfit.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
  }
  
  // Update position size
  const positionSizeElement = document.querySelector('.card:nth-child(3) .card-body p:nth-child(3)');
  if (positionSizeElement) {
    positionSizeElement.innerHTML = `<strong>Position Size:</strong> ${riskParams.positionSize} ETH`;
  }
}

// Update timestamp
function updateTimestamp() {
  const timestampElement = document.querySelector('.text-center.mt-4 p');
  if (timestampElement) {
    const now = new Date();
    const formattedDate = now.toLocaleDateString('en-US', { 
      month: 'long', 
      day: 'numeric', 
      year: 'numeric' 
    });
    
    const formattedTime = now.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
    
    timestampElement.innerHTML = `Last updated: ${formattedDate} ${formattedTime} | <a href="#">View Historical Analysis</a> | <a href="#">Settings</a>`;
  }
}

// Show/hide loading indicator
function showLoading(isLoading) {
  // In a real implementation, you would show/hide a loading spinner
  console.log(isLoading ? "Loading data..." : "Loading complete");
}

// Show error message
function showError(message) {
  // In a real implementation, you would show an error message to the user
  console.error(message);
}

// Helper function to find elements by text content
document.querySelector = (function(originalQuerySelector) {
  return function(selector) {
    if (selector.includes(':contains(')) {
      const matches = selector.match(/:contains\(["'](.+)["']\)/);
      if (matches) {
        const textToFind = matches[1];
        const cleanSelector = selector.replace(/:contains\(["'](.+)["']\)/, '');
        
        const elements = document.querySelectorAll(cleanSelector);
        for (const element of elements) {
          if (element.textContent.includes(textToFind)) {
            return element;
          }
        }
        return null;
      }
    }
    return originalQuerySelector.call(this, selector);
  };
})(document.querySelector);
